from random import randint


class Grille:
    """Représentation du plateau de jeu"""

    def __init__(self, grille_initiale=None):
        """Créer une grille vide, ou copier une grille existante"""
        self.width = 7
        self.heigth = 6
        self.sep_ligne = '\n'
        self.sep_colonne = ';'
        self.grid = [['.'] * self.width for _ in range(self.heigth)]
        if grille_initiale is not None:
            self.set(grille_initiale.get_name())

    def get_name(self):
        """Renvoyer un texte représentant la grille de façon unique"""
        return self.sep_ligne.join([self.sep_colonne.join(liste) for liste in self.grid])

    def set(self, name):
        """Créer la grille représentée par le texte"""
        listes = name.split(self.sep_ligne)
        self.grid = [l.split(self.sep_colonne) for l in listes]

    def wipe(self):
        """Effacer la grille"""
        self.__init__()

    def show_grid(self):
        """Afficher la grille"""
        sep = ' '
        print()
        for row_no, row in enumerate(self.grid):
            print(str(self.heigth - row_no) + '|' + sep.join(row))
        print('  ' + sep.join('-' for _ in range(self.width)))
        print('  ' + sep.join(chr(i + 65) for i in range(self.width)))
        print()
        return

    def drop(self, disc, col):
        """Placer un jeton dans la colonne"""
        ce_coup_est_possible = False
        for row in reversed(self.grid):
            if row[col - 1] == '.':
                row[col - 1] = disc
                ce_coup_est_possible = True
                break
        return ce_coup_est_possible

    def check_victory(self):
        """Vérifier si quatre jetons consécutifs du même joueur sont alignés"""
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if self.grid[y][x] != '.':
                    # Alignement horizontal, le noeud (x,y) étant le plus à gauche
                    if x < self.width - 3:
                        if all(self.grid[y][x] == self.grid[y][x + i + 1] for i in range(3)):
                            return True
                    # Alignement vertical, le noeud (x,y) étant le plus haut
                    if y < self.heigth - 3:
                        if all(self.grid[y][x] == self.grid[y + i + 1][x] for i in range(3)):
                            return True
                    # Alignement diagonal, le noeud (x,y) étant le plus haut et à gauche
                    if y < self.heigth - 3 and x < self.width - 3:
                        if all(self.grid[y][x] == self.grid[y + i + 1][x + i + 1] for i in range(3)):
                            return True
                    # Alignement diagonal, le noeud (x,y) étant le plus haut et à droite
                    if y < self.heigth - 3 and x > 2:
                        if all(self.grid[y][x] == self.grid[y + i + 1][x - i - 1] for i in range(3)):
                            return True
        return False

    def look_for_allowed_steps(self):
        """Renvoyer la liste des coups autorisés"""
        return [(x + 1) for x in range(self.width) if self.grid[0][x] == '.']

    def get_random_allowed_step(self):
        """Renvoyer un coups au hasard parmi ceux autorisés"""
        mes_coups_possibles = self.look_for_allowed_steps()
        tirage_aleatoire = randint(0, len(mes_coups_possibles) - 1)
        return mes_coups_possibles[tirage_aleatoire]
