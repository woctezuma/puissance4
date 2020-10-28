# Recherche arborescente Monte-Carlo pour le Puissance 4

[![PyPI status][pypi-image]][pypi]
[![Build status][build-image]][build]
[![Updates][dependency-image]][pyup]
[![Python 3][python3-image]][pyup]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

Ce projet présente une intelligence artificielle (IA) pour le jeu « Puissance 4 ».

## Utilisation

### Installation

-   Installez la dernière version de [Python 3.X](https://www.python.org/downloads/).
-   Installez le paquet [PyPI](https://pypi.org/project/puissance4/) :

```bash
pip install puissance4
```

### Une partie contre une IA UCT

Pour jouer contre une intelligence artificielle UCT, exécutez :

```python
import puissance4

# Play an interactive game versus UCT AI
puissance4.play_now() 
```

### Des parties entre IA

Pour tester des paramètres de l'IA, faites jouer une IA UCT contre l'IA de votre choix :

```python
import puissance4

# Either 'Random', 'MC' for Monte Carlo, or 'UCT' for Upper-Confidence bounds for Trees
trainer_choice = 'Random'

# Play 200 games in a setting UCT AI vs. trainer AI
puissance4.prepare_and_train(trainer_choice=trainer_choice, num_parties_jouees=200) 
```

## Introduction

Le jeu de Puissance 4 est un jeu de stratégie à deux joueurs 
dans lequel le plateau est composé de sept colonnes (verticales), 
chacune disposant de six emplacements. Chaque joueur dispose de jetons 
d'une couleur donnée. Lors d'une partie, les joueurs placent successivement 
un pion de leur couleur dans l'une des colonnes. La partie s'arrête 
dès que l'un des joueurs a réussi à aligner (horizontalement, verticalement 
ou en diagonale) quatre pions de sa couleur, ce joueur est alors le gagnant.

## Recherche arborescente Monte-Carlo

Nous présentons trois types de « joueur » par ordre croissant de complexité.

###	1. Aléatoire biaisé

Le joueur « aléatoire » tire selon une loi uniforme son prochain coup
parmi l'ensemble des coups admissibles (toutes les colonnes qui ne sont pas complètes).

Nous améliorons le joueur « aléatoire » en utilisant une connaissance propre au jeu du Puissance 4 : si trois jetons d'une même couleur sont alignés et s'il existe dans l'alignement une case vide dont la case inférieure est occupée, c'est-à-dire permettant d'obtenir un alignement de quatre jetons, alors ce coup est joué. Cela permet ou bien de gagner par cet alignement (si les jetons sont de la couleur du joueur), ou bien d'empêcher l'adversaire de gagner au coup suivant en réalisant cet alignement-ci (si les jetons sont de la couleur de l'adversaire). Nous jouons de même s'il existe une case vide sur l'alignement de deux jetons et d'un troisième de couleur identique, et que la case inférieure à la case vide est occupée. Cela permet d'accélérer les fins de partie lors de l'affrontement de deux joueurs faisant des choix aléatoires.

###	2. Monte-Carlo biaisé

Le joueur « Monte-Carlo biaisé » repose sur l'utilisation de [simulations Monte-Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search#Pure_Monte_Carlo_game_search) utilisant le joueur « aléatoire biaisé » : une grille étant donnée, le joueur répertorie l'ensemble des coups admissibles, puis, après avoir virtuellement joué chacun de ces coups possibles, simule un nombre fixé de fins de partie obtenues par l'affrontement de deux joueurs de type « aléatoire biaisé ». Le score associé à chacun des coups admissibles correspond au nombre de victoires suivant ce coup lors des simulations. Le joueur choisit alors le coup qui rend maximal ce score. C'est donc un joueur qui évalue un couple (position, action).

###	3. Upper Confidence bounds for Trees

L'algorithme « Upper Confidence bounds for Trees » (UCT) est une adaptation de l'algorithme « Upper Confidence Bound » (UCB) aux problèmes faisant intervenir des arbres, comme c'est le cas du jeu de Puissance 4.

Une position étant donnée, nous effectuons le choix entre exploration et exploitation à l'aide de la formule intervenant dans UCB. Pour un noeud (hors racine) donné :

<img alt="UCT score" src="https://github.com/woctezuma/puissance4/wiki/eqn.png" width="300">

avec :
-   $\mu$ : moyenne des scores obtenus
-   C : constante UCT, d'autant plus grande que l'on est prêt à explorer plutôt qu'exploiter.
-   n : nombre de simulations effectuées dans le père du noeud
-   s : nombre de simulations passant par ce noeud

En pratique, pour un noeud donné :
-   si l'un des fils du noeud considéré n'est pas exploré, alors nous l'évaluons.
-   sinon, nous considérons un nouveau noeud : le fils de plus grande valeur UCT.

Nous aboutissons donc à une position non encore explorée en suivant un chemin qui rend la valeur de l'UCT maximale. Nous évaluons cette position par un nombre fixé de simulations Monte-Carlo biaisées. Nous mettons enfin à jour le score de chacun des noeuds par lesquels nous sommes passés en suivant le chemin qui rend la valeur de l'UCT maximale.

Le noeud de départ correspond à la position actuelle, nous mettons donc à jour, pour chaque descente, évaluation et remontée dans l'arbre, la valeur UCT des fils de la racine. Au terme d'un nombre fixé de descentes dans l'arbre, nous effectuons l'action qui conduit au fils de la racine qui a la meilleure valeur UCT.

## Bibliographie

\[1] T. Cazenave, A. Saffidine,
	**Utilisation de la recherche arborescente Monte-Carlo au Hex**,
	*Revue d'Intelligence Artificielle*, vol. 23, no. 2-3, pp. 183-202, 2009.

\[2] F. Teytaud, O. Teytaud,
	**Creating an Upper-Condence-Tree program for Havannah**,
	*Advances in Computer Games* 12, in Pamplona, Spain, 2009.

<!-- Definitions for badges -->

[pypi]: <https://pypi.python.org/pypi/puissance4>
[pypi-image]: <https://badge.fury.io/py/puissance4.svg>

[build]: <https://github.com/woctezuma/puissance4/actions>
[build-image]: <https://github.com/woctezuma/puissance4/workflows/Python package/badge.svg?branch=master>
[publish-image]: <https://github.com/woctezuma/puissance4/workflows/Upload Python Package/badge.svg?branch=master>

[pyup]: <https://pyup.io/repos/github/woctezuma/puissance4/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/puissance4/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/puissance4/python-3-shield.svg>

[codecov]: <https://codecov.io/gh/woctezuma/puissance4>
[codecov-image]: <https://codecov.io/gh/woctezuma/puissance4/branch/master/graph/badge.svg>

[codacy]: <https://www.codacy.com/app/woctezuma/puissance4>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/fc278be88ea24bf79f8e8ceac1b3c305>
