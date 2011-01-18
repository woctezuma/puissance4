# -*- coding: utf-8 -*-

from random import randint
from mc import MC, getOtherSymbol
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
	'''Intelligence artificielle reposant sur l'algorithme Upper-Confidence-Tree'''

	def __init__(self, symbole = 'O', num_tirages_MC = 3, num_descentes_dans_arbre = 7, facteur_uct = 0.0):
		'''Créer un joueur du symbole indiqué'''
		MC.__init__(self, symbole, num_tirages_MC)
		self.num_descentes_dans_arbre = num_descentes_dans_arbre
		self.facteur_uct = facteur_uct

	def aiUCT(self, grille):
		'''Déterminer la meilleure action en fonction des résultats de l'exploration UCT'''
		# recevoir une position p
		etat_initial = grille.getName()
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
			R = self.simulerMonteCarlo(grille_simulee, symbole_dont_c_est_le_tour_pour_N)
			# nous effectuons une remontée de l'arbre (A, N, R)
			self.TreeUp(N, R, symbole_dont_c_est_le_tour, symbole_dont_c_est_le_tour_pour_N)
		# renvoyer le coup fils (de la racine de A) qui a la meilleure valeur UCT
		meilleure_action = self.choisirActionUCT(grille)
		return meilleure_action

	def ai(self, grille):
		'''Jouer en fonction des résultats de l'exploration UCT'''
		mon_coup_urgent = self.lookForObviousSteps(grille)
		if mon_coup_urgent == -1:
			mon_coup = self.aiUCT(grille)
			return mon_coup
		else:
			return mon_coup_urgent

	def TreeDown(self, position_courante, symbole_dont_c_est_le_tour):
		'''Descendre dans l'arbre UCT'''
		# soit N la racine de l'arbre
		N = self.tree
		joueur = symbole_dont_c_est_le_tour
		# boucle : fils non explorés de N
		grille = Grille()
		grille.set(N.name)
		while all([self.score_choix_action_dans_etat.has_key((N.name, i)) for i in grille.lookForAllowedSteps()]):
			# soit F le fils de N ayant la plus grande valeur UCT
			grille.set(N.name)
			try:
				self.compteur_visite_etat[N.name] += 1
			except KeyError:
				self.compteur_visite_etat[N.name] = 0
			action = self.choisirActionUCT(grille)
			try:
				self.compteur_choix_action_dans_etat[(N.name, action)] += 1
			except KeyError:
				self.compteur_choix_action_dans_etat[(N.name, action)] = 0
			nouvel_etat = changerEtatApresTransition(N.name, action, joueur)
			F = Node(nouvel_etat, N)
			F.code = action
			N = F
			joueur = getOtherSymbol(joueur)
		# soir F un fils de N tiré au hasard parmi les fils non explorés
		grille.set(N.name)
		mes_coups_possibles = grille.lookForAllowedSteps()
		actions_inexplorees = [i for i in mes_coups_possibles if not self.score_choix_action_dans_etat.has_key((N.name, i))]
		tirage = randint(0, len(actions_inexplorees)-1)
		action = actions_inexplorees[tirage]
		etat_inexplore = changerEtatApresTransition(N.name, action, joueur)
		F = Node(etat_inexplore, N)
		F.code = action
		joueur = getOtherSymbol(joueur)
		try:
			self.compteur_choix_action_dans_etat[(N.name, action)] += 1
		except KeyError:
			self.compteur_choix_action_dans_etat[(N.name, action)] = 0
		try:
			self.compteur_visite_etat[(F.name)] += 1
		except KeyError:
			self.compteur_visite_etat[(F.name)] = 0
		return (F,joueur)

	def TreeUp(self, noeud_N, evaluation_R, symbole_racine, symbole_noeud_N):
		'''Remonter dans l'arbre UCT'''
		pass

	def choisirActionUCT(self, grille):
		'''Choisir une action en utilisant le critère UCB'''
		etat = grille.getName()
		mes_coups_possibles = grille.lookForAllowedSteps()
		meilleure_action = None
		meilleure_evaluation = None
		for action in mes_coups_possibles:
			if not self.score_choix_action_dans_etat.has_key((state, action)):
				continue
			recompense_moyenne = self.score_choix_action_dans_etat[(etat, action)]
			num_etat_action = self.compteur_choix_action_dans_etat[(etat, action)]
			num_etat = self.compteur_visite_etat[(etat)]
			evaluation = recompense_moyenne+self.facteur_uct*sqrt(1.0*log(num_etat)/num_etat_action)
			if(evaluation > meilleure_evaluation):
				meilleure_evaluation = evaluation
				meilleure_action = action
		if meilleure_action == None:
			print("Erreur")
			raise
		return meilleure_action

def changerEtatApresTransition(self, etat, action, joueur):
	'''Déterminer l'état obtenu lorsque le joueur effectue l'action dans l'état donné'''
	grille_copiee = Grille()
	grille_copiee.set(etat)
	grille_copiee.drop(joueur, action)
	nouvel_etat = grille_copiee.getName()
	return nouvel_etat