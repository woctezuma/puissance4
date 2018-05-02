# -*- coding: utf-8 -*-

# Source d'inspiration :
# http://www.cs.helsinki.fi/u/vpeltoni/

class Grille:
	"""Représentation du plateau de jeu"""

	def __init__(self, grille_initiale = None):
		"""Créer une grille vide, ou copier une grille existante"""
		self.width = 7
		self.heigth = 6
		self.sep_ligne = '\n'
		self.sep_colonne = ';'
		self.grid = [['.'] * self.width for i in range(self.heigth)]
		if grille_initiale is not None:
			self.set(grille_initiale.getName())

	def getName(self):
		"""Renvoyer un texte représentant la grille de façon unique"""
		return self.sep_ligne.join([self.sep_colonne.join(liste) for liste in self.grid])

	def set(self, name):
		"""Créer la grille représentée par le texte"""
		listes = name.split(self.sep_ligne)
		self.grid = [l.split(self.sep_colonne) for l in listes]

	def wipe(self):
		"""Effacer la grille"""
		self.__init__()

	def showGrid(self):
		"""Afficher la grille"""
		for row in self.grid:
			for node in row:
				print(node + "  ")
			print('\n')
		for i in range(self.width):
			print(str(i+1) + "  ")
		print('\n\n')

	def drop(self, disc, col):
		"""Placer un jeton dans la colonne"""
		ce_coup_est_possible = False
		for row in reversed(self.grid):
			if row[col - 1] == '.':
				row[col-1] = disc
				ce_coup_est_possible = True
				break
		return ce_coup_est_possible

	def checkVictory(self):
		"""Vérifier si quatre jetons consécutifs du même joueur sont alignés"""
		for y in range (0,len(self.grid)):
			for x in range (0,len(self.grid[y])):
				if self.grid[y][x] != '.':
					'''Alignement horizontal, le noeud (x,y) étant le plus à gauche'''
					if x < self.width-3:
						if self.grid[y][x] == self.grid[y][x + 1] and self.grid[y][x] == self.grid[y][x + 2] and self.grid[y][x] == self.grid[y][x + 3]:
							return True
					'''Alignement vertical, le noeud (x,y) étant le plus haut'''
					if y < self.heigth-3:
						if self.grid[y][x] == self.grid[y + 1][x] and self.grid[y][x] == self.grid[y + 2][x] and self.grid[y][x] == self.grid[y + 3][x]:
							return True
					'''Alignement diagonal, le noeud (x,y) étant le plus haut et à gauche'''
					if y < self.heigth-3 and x < self.width-3:
						if self.grid[y][x] == self.grid[y + 1][x + 1] and self.grid[y][x] == self.grid[y + 2][x + 2] and self.grid[y][x] == self.grid[y + 3][x + 3]:
							return True
					'''Alignement diagonal, le noeud (x,y) étant le plus haut et à droite'''
					if y < self.heigth-3 and x > 2:
						if self.grid[y][x] == self.grid[y + 1][x - 1] and self.grid[y][x] == self.grid[y + 2][x - 2] and self.grid[y][x] == self.grid[y + 3][x - 3]:
							return True
		return False

	def lookForAllowedSteps(self):
		"""Renvoyer la liste des coups autorisés"""
		return [(x+1) for x in range(self.width) if self.grid[0][x]=='.']
