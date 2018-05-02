# -*- coding: utf-8 -*-

from math import sqrt, log
from random import randint
from mc import MC, get_other_symbol
from grille import Grille
from node import Node

# Articles de référence :
# [1] T. Cazenave, A. Saffidine,
#     Utilisation de la recherche arborescente Monte-Carlo au Hex,
#     Revue d'Intelligence Artificielle, vol. 23, no. 2-3, pp. 183-202, 2009.
# [2] F. Teytaud, O. Teytaud,
#     Creating an Upper-Condence-Tree program for Havannah,
#     Advances in Computer Games 12, in Pamplona, Spain, 2009.

class UCT(MC):
	"""Intelligence artificielle reposant sur l'algorithme Upper-Confidence-Tree"""

	def __init__(self, symbole='O', num_tirages_mc=3, num_descentes_dans_arbre=7, facteur_uct=0.0):
		"""Créer un joueur du symbole indiqué"""
		MC.__init__(self, symbole, num_tirages_mc)
		self.num_descentes_dans_arbre = num_descentes_dans_arbre
		self.facteur_uct = facteur_uct

	def aiUCT(self, grille):
		"""Déterminer la meilleure action en fonction des résultats de l'exploration UCT"""
		# recevoir une position p
		etat_initial = grille.get_name()
		symbole_dont_c_est_le_tour = self.player
		# soit A l'arbre UCT vide à la racine près
		self.tree = Node(etat_initial)
		self.compteur_visite_etat = {}
		self.score_choix_action_dans_etat = {}
		self.compteur_choix_action_dans_etat = {}
		# boucle : plusieurs descentes dans l'arbre
		for i in range(self.num_descentes_dans_arbre):
			# soit p' une copie de p
			grille_copiee = Grille()
			grille_copiee.set(etat_initial)
			# soit N le noeud résultat d'une descente dans l'arbre (A, p')
			(N, symbole_dont_c_est_le_tour_pour_N) = self.TreeDown(grille_copiee, symbole_dont_c_est_le_tour)
			# soit R l'évaluation de p'
			grille_pour_N = N.name
			grille_simulee = Grille()
			grille_simulee.set(grille_pour_N)
			R = self.simuler_monte_carlo(grille_simulee, symbole_dont_c_est_le_tour_pour_N)
			# nous effectuons une remontée de l'arbre (A, N, R)
			self.TreeUp(N, R, symbole_dont_c_est_le_tour, symbole_dont_c_est_le_tour_pour_N)
		# renvoyer le coup fils (de la racine de A) qui a la meilleure valeur UCT
		meilleure_action = self.choisirActionUCT(grille)
		return meilleure_action

	def ai(self, grille):
		"""Jouer en fonction des résultats de l'exploration UCT"""
		mon_coup_urgent = self.look_for_obvious_steps(grille)
		if mon_coup_urgent == -1:
			mon_coup = self.aiUCT(grille)
			return mon_coup
		else:
			return mon_coup_urgent

	def TreeDown(self, position_courante, symbole_dont_c_est_le_tour):
		"""Descendre dans l'arbre UCT"""
		# soit N la racine de l'arbre
		N = self.tree
		joueur = symbole_dont_c_est_le_tour
		# boucle : fils non explorés de N
		grille = Grille()
		grille.set(N.name)
		mes_coups_possibles = grille.lookForAllowedSteps()
		while all([self.compteur_choix_action_dans_etat.has_key((N.name, i)) for i in mes_coups_possibles]):
			# soit F le fils de N ayant la plus grande valeur UCT
			if len(mes_coups_possibles)>0:
				action = self.choisirActionUCT(grille)
				nouvel_etat = changerEtatApresTransition(N.name, action, joueur)
				F = Node(nouvel_etat, N)
				F.code = action
				N = F
				joueur = get_other_symbol(joueur)
				grille.set(N.name)
				mes_coups_possibles = grille.lookForAllowedSteps()
			else:
				break
		# soir F un fils de N tiré au hasard parmi les fils non explorés
		grille.set(N.name)
		mes_coups_possibles = grille.lookForAllowedSteps()
		if len(mes_coups_possibles)>0:
			actions_inexplorees = [i for i in mes_coups_possibles if not self.compteur_choix_action_dans_etat.has_key((N.name, i))]
			tirage = randint(0, len(actions_inexplorees)-1)
			action = actions_inexplorees[tirage]
			etat_inexplore = changerEtatApresTransition(N.name, action, joueur)
			F = Node(etat_inexplore, N)
			F.code = action
			joueur = get_other_symbol(joueur)
		else:
			F = N
		return F, joueur

	def TreeUp(self, noeud_N, evaluation_R, symbole_racine, symbole_noeud_N):
		"""Remonter dans l'arbre UCT"""
		symbole_courant = symbole_noeud_N
		while noeud_N is not self.tree:
			nom_N = noeud_N.name
			nom_parent_N = noeud_N.parent.name
			action_pour_arriver_en_N = noeud_N.code
			try:
				self.compteur_visite_etat[nom_N] += 1
			except KeyError:
				self.compteur_visite_etat[nom_N] = 1
			try:
				self.compteur_choix_action_dans_etat[(nom_parent_N, action_pour_arriver_en_N)] += 1
			except KeyError:
				self.compteur_choix_action_dans_etat[(nom_parent_N, action_pour_arriver_en_N)] = 1
			q = evaluation_R
			# Pour information, la ligne ci-dessous est juste, ne pas mettre de signe "!=" au lieu de "==".
			if symbole_courant == symbole_noeud_N: # <- La ligne qui m'a fait perdre beaucoup de temps.
				q *= -1.0
			try:
				# En effet, nous nous intéressons au parent de N, et non à N lui-même.
				mu_avant = self.score_choix_action_dans_etat[(nom_parent_N, action_pour_arriver_en_N)]
			except KeyError:
				mu_avant = 0
			n = self.compteur_choix_action_dans_etat[(nom_parent_N, action_pour_arriver_en_N)]
			mu = mu_avant + (1.0/n)*(q - mu_avant)
			self.score_choix_action_dans_etat[(nom_parent_N, action_pour_arriver_en_N)] = mu
			noeud_N = noeud_N.parent
			symbole_courant = get_other_symbol(symbole_courant)
		# Enfin, visite de la racine.
		try:
			self.compteur_visite_etat[noeud_N.name] += 1
		except KeyError:
			self.compteur_visite_etat[noeud_N.name] = 1
		return

	def choisirActionUCT(self, grille):
		"""Choisir une action en utilisant le critère UCB"""
		etat = grille.get_name()
		mes_coups_possibles = grille.lookForAllowedSteps()
		meilleure_action = None
		meilleure_evaluation = None
		for action in mes_coups_possibles:
			if not self.score_choix_action_dans_etat.has_key((etat, action)):
				continue
			recompense_moyenne = self.score_choix_action_dans_etat[(etat, action)]
			num_etat_action = self.compteur_choix_action_dans_etat[(etat, action)]
			num_etat = self.compteur_visite_etat[etat]
			evaluation = recompense_moyenne+self.facteur_uct*sqrt(1.0*log(num_etat)/num_etat_action)
			if evaluation > meilleure_evaluation:
				meilleure_evaluation = evaluation
				meilleure_action = action
		if meilleure_action is None:
			print("Aucun coup admissible.")
		return meilleure_action

def changerEtatApresTransition(etat, action, joueur):
	"""Déterminer l'état obtenu lorsque le joueur effectue l'action dans l'état donné"""
	grille_copiee = Grille()
	grille_copiee.set(etat)
	grille_copiee.drop(joueur, action)
	nouvel_etat = grille_copiee.get_name()
	return nouvel_etat