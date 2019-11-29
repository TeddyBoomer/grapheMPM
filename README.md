grapheMPM
=========

* [page Github](https://github.com/TeddyBoomer/grapheMPM)

* [Téléchargement](https://github.com/TeddyBoomer/grapheMPM/releases)

Un objet python pour implémenter la méthode des potentiels Métra MPM
d'ordonnancement.
La classe `GrapheMPM` comporte:

* le dictionnaire des `successeurs`
* celui des `predecesseurs`,
* celui des `niveaux` (à créer avec la méthode `setlevel`),
* la matrice d'adjacence `mat_adj`,
* le dictionnaire des `sommets` pour lier leur nom à leur emplacement dans la matrice d'adjacence,
* l'objet `gv` qui est sa traduction Graphviz (à créer et recharger par la méthode `makeGraphviz`)

On y a implémenté les méthodes pour les dates au plus tôt, au plus tard.
 
dépendances:
============

* modules python: Graphviz, lxml, numpy
* logiciel Graphviz

Illustration de principe:
=========================

On créée un objet `GrapheMPM` à l'aide d'un dictionnaire des successeurs ou des prédecesseurs et un dictionnaire des pondérations.

```python
from grapheMPM import GrapheMPM

# dico des prédecesseurs
p = {"déb":"", "A":['déb'], "B":['déb'], "C": "A", "D": "AB", "E":"B",
"F":"DE", "G": "E", "H":"CF", "I":"FG", "J": "HI", "fin": "J"}
# dico des pondérations
w = {"déb": 0, "fin": 0,"A": 7, "B": 3, "C": 4, "D": 2, "E": 8,
"F": 6, "G": 5, "H": 7, "I": 5, "J": 3}
G = GrapheMPM(pred=p, pond=w)
G.setlevel()
G.earliestdate()
G.makeGraphviz()
G.gv.render("ex-ed")
```
<img src="ex-ed.png" width="500">

```python
G.latestdate()
G.makeGraphviz()
G.gv.render("ex1-full")
```
<img src="ex-full.png" width="500">

**Nouveau (version >=0.3.3)**: un nouveau paramètre `presentation` (à 1 par défaut) permet de régler la répartition des marges (l'une sur l'autre ou côte à côte). Voici le graphe complet avec `presentation=2`:

```python
G = GrapheMPM(pred=p, pond=w, presentation=2)
# […]
```
<img src="ex-full-2.png" width="500">

**Attention**: depuis la version v0.3, on initialise l'objet avec des éléments
nommés:

* au choix `pred` ou `succ` dictionnaire des prédécesseurs (resp. des successeurs)
* `pond` dictionnaire des pondérations.

La méthode `setlevel` applique l'algorithme de recherche des niveaux à partir
de l'observation des colonnes nulles de la matrice d'adjacence `mat_adj`.

Les méthodes `earliestdate, latestdate` mettent à jour les dates des nœuds et
doivent être appliquées dans le bon ordre.

Installation
============

Module en Python3. Il vous est conseillé d'utiliser une
version de Python >=3.4. En effet, à partir de là, l'installateur pip
standardise l'installation des modules (et utilise le plus récent format
d'archive **wheel**)

L'installateur pip veillera à installer les dépendances.

Pour windows::

```
py -3 -m pip install \chemin\vers\grapheMPM-xxx-py3-none-any.whl
```

Pour linux::

```
sudo pip3 install  /chemin/vers/grapheMPM-xxx-py3-none-any.whl
```
