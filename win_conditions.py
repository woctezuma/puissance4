# Objective: check whether win conditions can be achieved in one step


def check_horizontale(grille, x, y):
    symbole = grille.grid[y][x]
    # Alignement horizontal de trois jetons consécutifs, le noeud (x,y) étant le plus à gauche
    if grille.is_far_from_right(x):
        if all(symbole == grille.grid[y][x + i + 1] for i in range(2)):
            my_play = grille.play_if_possible(x + 3, y)
            if my_play is not None:
                return my_play
    # Alignement horizontal de trois jetons non consécutifs, le noeud (x,y) étant le plus à gauche
    if grille.is_far_from_right(x):
        if symbole == grille.grid[y][x + 3]:
            # Alignement horizontal de la forme X.XX
            if symbole == grille.grid[y][x + 2]:
                my_play = grille.play_if_possible(x + 1, y)
                if my_play is not None:
                    return my_play
            # Alignement horizontal de la forme XX.X
            if symbole == grille.grid[y][x + 1]:
                my_play = grille.play_if_possible(x + 2, y)
                if my_play is not None:
                    return my_play
    # Alignement horizontal de trois jetons consécutifs, le noeud (x,y) étant le plus à droite
    if grille.is_far_from_left(x):
        if all(symbole == grille.grid[y][x - i - 1] for i in range(2)):
            my_play = grille.play_if_possible(x - 3, y)
            if my_play is not None:
                return my_play

    return None


def check_verticale(grille, x, y):
    symbole = grille.grid[y][x]
    # Alignement vertical de trois jetons consécutifs, le noeud (x,y) étant le plus haut
    if grille.height - 2 > y >= 1:
        if all(symbole == grille.grid[y + i + 1][x] for i in range(2)):
            if grille.grid[y - 1][x] == grille.empty_space:
                return x + 1
    return None


def check_oblique_montante(grille, x, y):
    symbole = grille.grid[y][x]
    # Alignement diagonal montant : allant du coin bas gauche au coin haut droit
    if grille.is_far_from_bottom(y) and grille.is_far_from_left(x):
        if symbole == grille.grid[y + 3][x - 3]:
            # Alignement diagonal de la forme X.XX
            if symbole == grille.grid[y + 2][x - 2]:
                my_play = grille.play_if_possible(x - 1, y + 1)
                if my_play is not None:
                    return my_play
            # Alignement diagonal de la forme XX.X
            if symbole == grille.grid[y + 1][x - 1]:
                my_play = grille.play_if_possible(x - 2, y + 2)
                if my_play is not None:
                    return my_play
        # Alignement diagonal, le noeud (x,y) étant le plus haut et à droite
        if all(symbole == grille.grid[y + i + 1][x - i - 1] for i in range(2)):
            if grille.is_very_far_from_bottom(y):
                my_play = grille.play_if_possible(x - 3, y + 3)
                if my_play is not None:
                    return my_play
    # Alignement diagonal montant de la forme XXX., le noeud (x,y) étant le plus bas et à gauche
    if grille.is_far_from_top(y) and grille.is_far_from_right(x):
        if all(symbole == grille.grid[y - i - 1][x + i + 1] for i in range(2)):
            my_play = grille.play_if_possible(x + 3, y - 2)
            if my_play is not None:
                return my_play

    return None


def check_oblique_descendante(grille, x, y):
    symbole = grille.grid[y][x]
    # Alignement diagonal descendant : allant du coin haut gauche au coin bas droit
    if grille.is_far_from_bottom(y) and grille.is_far_from_right(x):
        if symbole == grille.grid[y + 3][x + 3]:
            # Alignement diagonal de la forme X.XX
            if symbole == grille.grid[y + 2][x + 2]:
                my_play = grille.play_if_possible(x + 1, y + 1)
                if my_play is not None:
                    return my_play

            # Alignement diagonal de la forme XX.X
            if symbole == grille.grid[y + 1][x + 1]:
                my_play = grille.play_if_possible(x + 2, y + 2)
                if my_play is not None:
                    return my_play

        # Alignement diagonal, le noeud (x,y) étant le plus haut et à gauche
        if all(symbole == grille.grid[y + i + 1][x + i + 1] for i in range(2)):
            if grille.is_very_far_from_bottom(y):
                my_play = grille.play_if_possible(x + 3, y + 3)
                if my_play is not None:
                    return my_play

    # Alignement diagonal descendant de la forme .XXX, le noeud (x,y) étant le plus bas et à droite
    if grille.is_far_from_top(y) and grille.is_far_from_left(x):
        if all(symbole == grille.grid[y - i - 1][x - i - 1] for i in range(2)):
            my_play = grille.play_if_possible(x - 2, y - 3)
            if my_play is not None:
                return my_play

    return None


def look_for_obvious_steps(grille):
    """Vérifier s'il est possible de gagner pour l'un ou l'autre joueur.
    Si oui, renvoyer le numéro de la colonne à jouer, sinon None"""
    for y in range(0, len(grille.grid)):
        for x in range(0, len(grille.grid[y])):
            # Rechercher un coup qui permette ou empêche un alignement de quatre jetons
            if grille.grid[y][x] != grille.empty_space:

                my_play = check_horizontale(grille, x, y)
                if my_play is not None:
                    return my_play

                my_play = check_verticale(grille, x, y)
                if my_play is not None:
                    return my_play

                my_play = check_oblique_montante(grille, x, y)
                if my_play is not None:
                    return my_play

                my_play = check_oblique_descendante(grille, x, y)
                if my_play is not None:
                    return my_play

    # Aucun coup urgent, alors renvoyer -1
    return None
