# Objective: check whether win conditions can be achieved in one step


def check_horizontale(grille, x, y):
    # Alignement horizontal de trois jetons consécutifs, le noeud (x,y) étant le plus à gauche
    if x < grille.width - 3:
        if all(grille.grid[y][x] == grille.grid[y][x + i + 1] for i in range(2)):
            if y < grille.heigth - 1:
                if grille.grid[y + 1][x + 3] != '.' and grille.grid[y][x + 3] == '.':
                    return x + 4
            elif grille.grid[y][x + 3] == '.':
                return x + 4
    # Alignement horizontal de trois jetons non consécutifs, le noeud (x,y) étant le plus à gauche
    if x < grille.width - 3:
        if grille.grid[y][x] == grille.grid[y][x + 3]:
            # Alignement horizontal de la forme X.XX
            if grille.grid[y][x] == grille.grid[y][x + 2]:
                if y < grille.heigth - 1:
                    if grille.grid[y + 1][x + 1] != '.' and grille.grid[y][x + 1] == '.':
                        return x + 2
                elif grille.grid[y][x + 1] == '.':
                    return x + 2
            # Alignement horizontal de la forme XX.X
            if grille.grid[y][x] == grille.grid[y][x + 1]:
                if y < grille.heigth - 1:
                    if grille.grid[y + 1][x + 2] != '.' and grille.grid[y][x + 2] == '.':
                        return x + 3
                elif grille.grid[y][x + 2] == '.':
                    return x + 3
    # Alignement horizontal de trois jetons consécutifs, le noeud (x,y) étant le plus à droite
    if x > 2:
        if all(grille.grid[y][x] == grille.grid[y][x - i - 1] for i in range(2)):
            if y < grille.heigth - 1:
                if grille.grid[y + 1][x - 3] != '.' and grille.grid[y][x - 3] == '.':
                    return x - 2
            elif grille.grid[y][x - 3] == '.':
                return x - 2
    return None


def check_verticale(grille, x, y):
    # Alignement vertical de trois jetons consécutifs, le noeud (x,y) étant le plus haut
    if grille.heigth - 2 > y >= 1:
        if all(grille.grid[y][x] == grille.grid[y + i + 1][x] for i in range(2)):
            if grille.grid[y - 1][x] == '.':
                return x + 1
    return None


def check_oblique_montante(grille, x, y):
    # Alignement diagonal montant : allant du coin bas gauche au coin haut droit
    if y < grille.heigth - 3 and x > 2:
        if grille.grid[y][x] == grille.grid[y + 3][x - 3]:
            # Alignement diagonal de la forme X.XX
            if grille.grid[y][x] == grille.grid[y + 2][x - 2]:
                if grille.grid[y + 2][x - 1] != '.' and grille.grid[y + 1][x - 1] == '.':
                    return x
            # Alignement diagonal de la forme XX.X
            if grille.grid[y][x] == grille.grid[y + 1][x - 1]:
                if grille.grid[y + 3][x - 2] != '.' and grille.grid[y + 2][x - 2] == '.':
                    return x - 1
        # Alignement diagonal, le noeud (x,y) étant le plus haut et à droite
        if all(grille.grid[y][x] == grille.grid[y + i + 1][x - i - 1] for i in range(2)):
            if y < grille.heigth - 4:
                if grille.grid[y + 4][x - 3] != '.' and grille.grid[y + 3][x - 3] == '.':
                    return x - 2
            elif grille.grid[y + 3][x - 3] == '.':
                return x - 2
    # Alignement diagonal montant de la forme XXX., le noeud (x,y) étant le plus bas et à gauche
    if y > 3 and x < grille.width - 3:
        if all(grille.grid[y][x] == grille.grid[y - i - 1][x + i + 1] for i in range(2)):
            if grille.grid[y - 2][x + 3] != '.' and grille.grid[y - 3][x + 3] == '.':
                return x + 4

    return None


def check_oblique_descendante(grille, x, y):
    """Alignement diagonal descendant : allant du coin haut gauche au coin bas droit"""
    if y < grille.heigth - 3 and x < grille.width - 3:
        if grille.grid[y][x] == grille.grid[y + 3][x + 3]:
            # Alignement diagonal de la forme X.XX
            if grille.grid[y][x] == grille.grid[y + 2][x + 2]:
                if grille.grid[y + 2][x + 1] != '.' and grille.grid[y + 1][x + 1] == '.':
                    return x + 2
            # Alignement diagonal de la forme XX.X
            if grille.grid[y][x] == grille.grid[y + 1][x + 1]:
                if grille.grid[y + 3][x + 2] != '.' and grille.grid[y + 2][x + 2] == '.':
                    return x + 3
        # Alignement diagonal, le noeud (x,y) étant le plus haut et à gauche
        if all(grille.grid[y][x] == grille.grid[y + i + 1][x + i + 1] for i in range(2)):
            if y < grille.heigth - 4:
                if grille.grid[y + 4][x + 3] != '.' and grille.grid[y + 3][x + 3] == '.':
                    return x + 4
            elif grille.grid[y + 3][x + 3] == '.':
                return x + 4
    # Alignement diagonal descendant de la forme .XXX, le noeud (x,y) étant le plus bas et à droite
    if y > 3 and x > 2:
        if all(grille.grid[y][x] == grille.grid[y - i - 1][x - i - 1] for i in range(2)):
            if grille.grid[y - 2][x - 3] != '.' and grille.grid[y - 3][x - 3] == '.':
                return x - 2

    return None


def look_for_obvious_steps(grille):
    """Vérifier s'il est possible de gagner pour l'un ou l'autre joueur.
    Si oui, renvoyer le numéro de la colonne à jouer, sinon None"""
    for y in range(0, len(grille.grid)):
        for x in range(0, len(grille.grid[y])):
            # Rechercher un coup qui permette ou empêche un alignement de quatre jetons
            if grille.grid[y][x] != '.':

                pos = check_horizontale(grille, x, y)
                if pos is not None:
                    return pos

                pos = check_verticale(grille, x, y)
                if pos is not None:
                    return pos

                pos = check_oblique_montante(grille, x, y)
                if pos is not None:
                    return pos

                pos = check_oblique_descendante(grille, x, y)
                if pos is not None:
                    return pos

    # Aucun coup urgent, alors renvoyer -1
    return None
