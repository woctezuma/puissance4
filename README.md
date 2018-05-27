# Recherche arborescente Monte-Carlo pour le Puissance 4

[![PyPI status][PyPI image]][PyPI] [![Build status][Build image]][Build] [![Updates][Dependency image]][PyUp] [![Python 3][Python3 image]][PyUp] [![Code coverage][Coveralls image]][Coveralls] [![Code coverage BIS][Codecov image]][Codecov]

  [PyPI]: https://pypi.python.org/pypi/puissance4
  [PyPI image]: https://badge.fury.io/py/puissance4.svg

  [Build]: https://travis-ci.org/woctezuma/puissance4
  [Build image]: https://travis-ci.org/woctezuma/puissance4.svg?branch=master

  [PyUp]: https://pyup.io/repos/github/woctezuma/puissance4/
  [Dependency image]: https://pyup.io/repos/github/woctezuma/puissance4/shield.svg
  [Python3 image]: https://pyup.io/repos/github/woctezuma/puissance4/python-3-shield.svg

  [Coveralls]: https://coveralls.io/github/woctezuma/puissance4?branch=master
  [Coveralls image]: https://coveralls.io/repos/github/woctezuma/puissance4/badge.svg?branch=master

  [Codecov]: https://codecov.io/gh/woctezuma/puissance4
  [Codecov image]: https://codecov.io/gh/woctezuma/puissance4/branch/master/graph/badge.svg

## Résumé

Ce projet consiste à développer une intelligence artificielle (IA)
pour le jeu "Puissance 4" ("Connect 4" en anglais). Nous 
présentons une application de la recherche arborescente Monte-Carlo.

### Installation

- Installez la dernière version de [Python 3.X](https://www.python.org/downloads/).

Puis, au choix :

i) téléchargez ce dépôt Github et installez les modules requis :

```bash
git clone https://github.com/woctezuma/puissance4.git
pip install -r puissance4/requirements.txt
```

ii) Installez le paquet que j'ai déposé sur [PyPI](https://pypi.org/project/puissance4/):

```bash
pip install puissance4
```

### Utilisation

#### Une partie contre l'IA

- Pour jouer vous-même contre une intelligence artificielle UCT d'un bon niveau, importez le paquet PyPI depuis Python :

```python
import puissance4

# Play an interactive game versus UCT AI
puissance4.play_now() 
```

#### Des parties IA contre IA

- (facultatif) Pour calibrer les paramètres de l'IA, importez le paquet PyPI depuis Python :

```python
import puissance4

# Either 'Random', 'MC', or 'UCT'
trainer_choice = 'MC' 

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

## Recherche Monte-Carlo

Nous présentons trois types de « joueur » par ordre croissant de complexité.

###	1. Aléatoire biaisé

Le joueur « aléatoire » tire selon une loi uniforme son prochain coup
parmi l'ensemble des coups admissibles (toutes les colonnes qui ne sont pas complètes).

Nous améliorons le joueur « aléatoire » en utilisant une connaissance propre au jeu du Puissance 4 : si trois jetons d'une même couleur sont alignés et s'il existe dans l'alignement une case vide dont la case inférieure est occupée, c'est-à-dire permettant d'obtenir un alignement de quatre jetons, alors ce coup est joué. Cela permet ou bien de gagner par cet alignement (si les jetons sont de la couleur du joueur), ou bien d'empêcher l'adversaire de gagner au coup suivant en réalisant cet alignement-ci (si les jetons sont de la couleur de l'adversaire). Nous jouons de même s'il existe une case vide sur l'alignement de deux jetons et d'un troisième de couleur identique, et que la case inférieure à la case vide est occupée. Cela permet d'accélérer les fins de partie lors de l'affrontement de deux joueurs faisant des choix aléatoires.

###	2. Monte-Carlo biaisé

Le joueur « Monte-Carlo biaisé » repose sur l'utilisation de simulations Monte-Carlo utilisant le joueur « aléatoire biaisé » : une grille étant donnée, le joueur répertorie l'ensemble des coups admissibles, puis, après avoir virtuellement joué chacun de ces coups possibles, simule un nombre fixé de fins de partie obtenues par l'affrontement de deux joueurs de type « aléatoire biaisé ». Le score associé à chacun des coups admissibles correspond au nombre de victoires suivant ce coup lors des simulations. Le joueur choisit alors le coup qui rend maximal ce score. C'est donc un joueur qui évalue un couple (position, action)

###	3. Upper Confidence bounds for Trees

L'algorithme « Upper Confidence bounds for Trees » (UCT) est une adaptation de l'algorithme « Upper Confidence Bound » (UCB) aux problèmes faisant intervenir des arbres, comme c'est le cas du jeu de Puissance 4.

Une position étant donnée, nous effectuons le choix entre exploration et exploitation à l'aide de la formule intervenant dans UCB. Pour un noeud (hors racine) donné :
> $$\mu+C\sqrt{\frac{\log\left(n\right)}{s}}$$

avec :
- $\mu$ : moyenne des scores obtenus
- C : constante UCT, d'autant plus grande que l'on est prêt à explorer plutôt qu'exploiter.
- n : nombre de simulations effectuées dans le père du noeud
- s : nombre de simulations passant par ce noeud

En pratique, pour un noeud donné :
- si l'un des fils du noeud considéré n'est pas exploré, alors nous l'évaluons.
- sinon, nous considérons un nouveau noeud : le fils de plus grande valeur UCT.

Nous aboutissons donc à une position non encore explorée en suivant un chemin qui rend la valeur de l'UCT maximale. Nous évaluons cette position par un nombre fixé de simulations Monte-Carlo biaisées. Nous mettons enfin à jour le score de chacun des noeuds par lesquels nous sommes passés en suivant le chemin qui rend la valeur de l'UCT maximale.

Le noeud de départ correspond à la position actuelle, nous mettons donc à jour, pour chaque descente, évaluation et remontée dans l'arbre, la valeur UCT des fils de la racine. Au terme d'un nombre fixé de descentes dans l'arbre, nous effectuons l'action qui conduit au fils de la racine qui a la meilleure valeur UCT.

## Bibliographie

[1] T. Cazenave, A. Saffidine,
	**Utilisation de la recherche arborescente Monte-Carlo au Hex**,
	*Revue d'Intelligence Artificielle*, vol. 23, no. 2-3, pp. 183-202, 2009.

[2] F. Teytaud, O. Teytaud,
	**Creating an Upper-Condence-Tree program for Havannah**,
	*Advances in Computer Games* 12, in Pamplona, Spain, 2009.
