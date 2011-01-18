# -*- coding: utf-8 -*-

# Source d'inspiration :
# http://www.cs.helsinki.fi/u/vpeltoni/

from time import sleep
from ai import AI
from mc import MC
from grille import Grille

def menu():
    '''Menu principal'''
    input = []
    while(input not in ['q']):
        input = raw_input("0) No player game.\n1) Single player game.\n2) Player vs player game.\nq) Quit.\ninput:")
        if(input == '0'):
            choix_ai_basique = False
            np(choix_ai_basique)
        if(input == '1'):
            sp()
        if(input == '2'):
            pvp()

def np(choix_ai_basique, show_grid = False):
    '''Une partie entre intelligences artificielles'''
    grid = Grille()
    ai1 = MC('X')
    if choix_ai_basique:
        ai1 = AI('X')
    ai2 = AI('O')
    le_joueur1_gagne = False
    mes_coups_possibles = grid.lookForAllowedSteps()
    while(grid.checkVictory() is False and len(mes_coups_possibles)>0):
        MonCoup = ai1.ai(grid)
        grid.drop(ai1.player, MonCoup)
        le_joueur1_gagne = True
        mes_coups_possibles = grid.lookForAllowedSteps()
        if show_grid:
            grid.showGrid()
            sleep(1)
        if(grid.checkVictory() is False and len(mes_coups_possibles)>0):
            VotreCoup = ai2.ai(grid)
            grid.drop(ai2.player, VotreCoup)
            le_joueur1_gagne = False
            mes_coups_possibles = grid.lookForAllowedSteps()
            if show_grid:
                grid.showGrid()
    il_y_a_un_vainqueur = grid.checkVictory()
    print "The game ended in the following state:"
    grid.showGrid()
    print("Y a-t-il un gagnant ?", il_y_a_un_vainqueur)
    print("Si oui, est-ce le joueur n°1 (X) ?", le_joueur1_gagne)
    return (il_y_a_un_vainqueur, le_joueur1_gagne)

def sp(choix_ai_basique = False):
    '''Une partie opposant un joueur humain à une intelligence artificielle'''
    grid = Grille()
    ai = MC('O')
    if choix_ai_basique:
        ai = AI('O')
    le_joueur1_gagne = False
    mes_coups_possibles = grid.lookForAllowedSteps()
    input = []
    player = 'X'
    while(input != 'q' and grid.checkVictory() is False and len(mes_coups_possibles)>0):
        grid.showGrid()
        input = raw_input("Number 1 through 7  = drop disc, q = quit. \nYour move:")
        if (input in ['1','2','3','4','5','6','7']):
            MonCoup = int(input)
            if grid.drop(player, MonCoup):
                le_joueur1_gagne = True
                mes_coups_possibles = grid.lookForAllowedSteps()
                if(grid.checkVictory() is False and len(mes_coups_possibles)>0):
                    VotreCoup = ai.ai(grid)
                    grid.drop(ai.player, VotreCoup)
                    le_joueur1_gagne = False
                    mes_coups_possibles = grid.lookForAllowedSteps()
    il_y_a_un_vainqueur = grid.checkVictory()
    print "The game ended in the following state:"
    grid.showGrid()
    print("Y a-t-il un gagnant ?", il_y_a_un_vainqueur)
    print("Si oui, est-ce le joueur n°1 (X) ?", le_joueur1_gagne)

def pvp():
    '''Une partie entre joueurs humains'''
    grid = Grille()
    input = []
    player = 'X'
    while(input != 'q' and grid.checkVictory() is False):
        grid.showGrid()
        input = raw_input("1 2 3 4 5 6 7  = drop disc, q = quit. \nPlayer " +player+" to move:")
        if (input in ['1','2','3','4','5','6','7']):
            if grid.drop(player, int(input)):
                if(player == 'X'):
                    player = 'O'
                else:
                    player = 'X'
    print "The game ended in the following state:"
    grid.showGrid()

def obtenirStatistiquesDeVictoires():
    return

def getStatsVictory(numParties, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor):
    numPartiesAvecVainqueur = 0
    numVictoiresDesCroix = 0
    for i in range(numParties):
        (il_y_a_un_vainqueur, LesCroixGagnent) = auto(MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)
        numPartiesAvecVainqueur += int(il_y_a_un_vainqueur)
        numVictoiresDesCroix += int(LesCroixGagnent)
    return round(numVictoiresDesCroix*100.0/numPartiesAvecVainqueur)/100.0


if __name__ == "__main__":
    menu()

    ## pour les statistiques de victoire
    numParties = 50
    ## paramètres possibles
    MonteCarloOnly = False
    numDescentesDansArbre = 30
    numMCSimulations = 100
    uct_factor = 5.0

    ## statistiques

    #print("Monte-Carlo biaisé")
    #MonteCarloOnly = True
    #for numMCSimulations in range(50,201,50):
        #numVictoires = getStatsVictory(numParties, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)
        #print(numVictoires, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)

    #print("UCT")
    #MonteCarloOnly = False
    #numMCSimulations = 50
    #for uct_factor in range(0,16,5):
        #for numDescentesDansArbre in range(10,51,20):
            #numVictoires = getStatsVictory(numParties, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)
            #print(numVictoires, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)

    #print("UCT bis")
    #MonteCarloOnly = False
    #numDescentesDansArbre = 15
    #numMCSimulations = 50
    #for uct_factor in range(0,101,10):
            #numVictoires = getStatsVictory(numParties, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)
            #print(numVictoires, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)

    #print("UCT ter")
    #MonteCarloOnly = False
    #numMCSimulations = 30
    #for uct_factor in range(0,16,5):
        #for numDescentesDansArbre in range(2,16,4):
            #numVictoires = getStatsVictory(numParties, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)
            #print(numVictoires, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)

    #print("Monte-Carlo biaisé bis")
    #MonteCarloOnly = True
    #for numMCSimulations in range(1, 7):
        #numVictoires = getStatsVictory(numParties, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)
        #print(numVictoires, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)

    print("Post-soutenance")
    numDescentesDansArbre = 7
    numMCSimulations = 2
    uct_factor = 0.0
    numVictoires = getStatsVictory(numParties, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)
    print(numVictoires, MonteCarloOnly, numDescentesDansArbre, numMCSimulations, uct_factor)

    print("Done.")
