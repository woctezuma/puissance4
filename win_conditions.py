# Objective: check whether win conditions can be achieved in one step


def check_horizontale(grille, x, y):
    """Alignements horizontaux"""
    symbole = grille.grid[y][x]
    # Alignement horizontal de trois jetons consécutifs, le noeud (x,y) étant le plus à droite
    if grille.is_far_from_left(x):
        if all(symbole == grille.grid[y][x - i - 1] for i in range(2)):
            my_play = grille.play_if_possible(x - 3, y)
            if my_play is not None:
                return my_play
    # Alignements horizontaux, le noeud (x,y) étant le plus à gauche
    if grille.is_far_from_right(x):
        # Alignement horizontal de trois jetons consécutifs
        if all(symbole == grille.grid[y][x + i + 1] for i in range(2)):
            my_play = grille.play_if_possible(x + 3, y)
            if my_play is not None:
                return my_play
        # Alignement horizontal de trois jetons non consécutifs
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

    return None


def check_verticale(grille, x, y):
    """Alignement vertical"""
    symbole = grille.grid[y][x]
    # Alignement vertical de trois jetons consécutifs, le noeud (x,y) étant le plus haut
    if grille.is_quite_far_from_bottom(y) and not (grille.is_at_top(y)):
        if all(symbole == grille.grid[y + i + 1][x] for i in range(2)):
            my_play = grille.play_if_possible(x, y - 1)
            if my_play is not None:
                return my_play
    return None


def check_oblique_montante(grille, x, y):
    """Alignements diagonaux montants (/) : allant du coin bas gauche au coin haut droit"""
    symbole = grille.grid[y][x]
    # Alignement diagonal montant de la forme XXX., le noeud (x,y) étant le plus bas et à gauche
    if grille.is_far_from_top(y) and grille.is_far_from_right(x):
        if all(symbole == grille.grid[y - i - 1][x + i + 1] for i in range(2)):
            my_play = grille.play_if_possible(x + 3, y - 2)
            if my_play is not None:
                return my_play
    # Alignements diagonaux montants, le noeud (x,y) étant le plus haut et à droite
    if grille.is_far_from_bottom(y) and grille.is_far_from_left(x):
        # Alignement diagonal de la forme .XXX
        if all(symbole == grille.grid[y + i + 1][x - i - 1] for i in range(2)):
            if grille.is_very_far_from_bottom(y):
                my_play = grille.play_if_possible(x - 3, y + 3)
                if my_play is not None:
                    return my_play
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

    return None


def check_oblique_descendante(grille, x, y):
    """Alignements diagonaux descendants (\) : allant du coin haut gauche au coin bas droit"""
    symbole = grille.grid[y][x]

    # Alignement diagonal descendant de la forme .XXX, le noeud (x,y) étant le plus bas et à droite
    if grille.is_far_from_top(y) and grille.is_far_from_left(x):
        if all(symbole == grille.grid[y - i - 1][x - i - 1] for i in range(2)):
            my_play = grille.play_if_possible(x - 2, y - 3)
            if my_play is not None:
                return my_play

    # Alignements diagonaux descendants, le noeud (x,y) étant le plus haut et à gauche

    if grille.is_far_from_bottom(y) and grille.is_far_from_right(x):
        # Alignement diagonal de la forme XXX.
        if all(symbole == grille.grid[y + i + 1][x + i + 1] for i in range(2)):
            if grille.is_very_far_from_bottom(y):
                my_play = grille.play_if_possible(x + 3, y + 3)
                if my_play is not None:
                    return my_play

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

    return None


def look_for_obvious_steps(grille):
    """Vérifier s'il est possible de gagner pour l'un ou l'autre joueur.
    Si oui, renvoyer le numéro de la colonne à jouer, sinon None"""
    for x in range(grille.width):

        # Rechercher parmi les cases non vides
        search_start = 1 + grille.column_levels[x]

        if search_start < grille.height:
            my_play = check_verticale(grille, x, search_start)
            if my_play is not None:
                return my_play

        for y in range(search_start, grille.height):
            # Rechercher un coup qui permette ou empêche un alignement de quatre jetons

            my_play = check_horizontale(grille, x, y)
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
