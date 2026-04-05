grapheMPM
=========

* [page Github](https://github.com/TeddyBoomer/grapheMPM)

* [Téléchargement (page des releases)](https://github.com/TeddyBoomer/grapheMPM/releases)

* **commandes d'installation**: voir tout en bas de cette page.

Des objets python pour implémenter la méthode des potentiels Métra MPM
d'ordonnancement.

## La classe `GrapheSimple` comporte:

* le dictionnaire `GrapheSimple.successeurs`
* le dictionnaire `GrapheSimple.predecesseurs`,
* matrices liées au graphe de type `numpy.ndarray`:
  - la matrice d'adjacence `GrapheSimple.mat_adj`,
  - la matrice de fermeture transitive `GrapheSimple.mat_ferm_transitive`,
  - la liste des puissances de la matrice d'adjacence `GrapheSimple.Matrices`. La 1ere est celle de la matrice de fermeture transitive.
  - la liste de leur export latex `GrapheSimple.Matrices_latex`
* export latex du tableau des prédecesseurs `GrapheSimple.tab_latex_pred`
* export latex du tableau des successeurs `GrapheSimple.tab_latex_succ`
* une fonction de test booléen `has_no_circuit` (simple commodité: on regarde si il y a des 0 sur la diagonale de la matrice de fermeture transitive),
* le dictionnaire `num_sommets` pour lier leur nom à leur emplacement dans la matrice d'adjacence,
* l'objet `gv` qui est sa traduction Graphviz (à créer et recharger par la méthode `makeGraphviz`)
(on peut générer le graphe normal ou complété avec la fermeture transitive)

## La classe `GrapheSimpleNoCircuit`: 

Dans celle-ci, vous subodorez qu'il n'y a pas de circuit (c'est testé à
l'initialisation) et dans ce cas, les sommets sont organisés par niveaux comme
on l'attendrait. Si par malheur il y a un circuit, le tracé est alors celui
d'un `GrapheSimple`.

Elle comporte donc la méthode `setlevel` de calcul des niveaux.

## La classe `GrapheMPM` hérite des attributs et méthodes de `GrapheSimple` avec en plus:

* le dictionnaire des `niveaux`,
* les méthodes `earliestdate`, `latestdate` pour remplir les dates
* une méthode `setlevel` pour calculer les niveaux des sommets (utilisée en interne dans la classe)

deux fonctions techniques sont présentes dans le module:

* fonction `mat2tex` pour afficher l'export LaTeX d'une matrice (objet pmatrix)
* fonction `tab_latex` pour convertir les dictionnaires des prédecesseurs et successeurs en latex.

**Astuce**: pour récupérer la durée minimale du projet après tous les calculs:

```
[…]
G = GrapheMPM(…)
[…]
G.makeGraphviz()
# le sommet fin contient l'information de durée minimale du projet
print(G.sommets['fin'].data['ed'])
```

chaque nœud de tâche contient en effet un dictionnaire `data` avec ses dates
respectivement au plus tôt `ed` (earliest date), au plus tard `ld` (latest
date), la marge totale `mt`, la marge libre `ml`.

dépendances:
============

* modules python: Graphviz, lxml, numpy, pandas — installés automatiquement
* logiciel [Graphviz](https://graphviz.org/) — à installer vous-même.

Illustration de principe:
=========================

**Nouveau (v>=0.7)**: méthode de commodité `GrapheSimple.has_no_circuit()`. De
  plus l'organisation par niveaux est améliorée

**Nouveau (v>=0.6)**: puissances de la matrice d'adjacence (en numpy et en latex) disponibles
  par défaut, les marges ne sont plus affichées.

**Nouveau (v>=0.5.3)**: un paramètre booléen `marges` (`True`/`False`) pour indiquer d'afficher les cases des marges.

**Nouveau (v>=0.5)**: plus besoin de renseigner des sommets 'début' et 'fin'

**Nouveau (v>=0.4)**: Les poids peuvent être des décimaux.

objet GrapheMPM
----------------

On créée un objet `GrapheMPM` à l'aide d'un dictionnaire des successeurs ou des prédecesseurs et un dictionnaire des pondérations.

```python
from grapheMPM import GrapheMPM

# dico des prédecesseurs
p = {"A": "", "B": "", "C": "A", "D": "AB", "E":"B",
     "F":"DE", "G": "E", "H":"CF", "I":"FG", "J": "HI", "K": "I"}
# dico des pondérations
w = {"A": 7, "B": 3, "C": 4.1, "D": 2.3, "E": 8,
     "F": 6, "G": 5, "H": 7, "I": 5, "J": 3, "K": 3.5}

G = GrapheMPM(pred=p, pond=w, marges=False) # par défaut marges=False
G.earliestdate()
G.makeGraphviz()
G.gv.render("ex-ed-nomarge")
G.gv.format = "svg"
G.gv.render("ex-ed-nomarge")
```
L'avant dernière ligne permet de changer le format d'image à svg plutôt que png.

<img src="illustrations/ex-ed-nomarge.png" width="600">

```python
G.latestdate()
G.makeGraphviz()
G.gv.render("ex-full-nomarge")
```
<img src="illustrations/ex-full-nomarge.png" width="600">

observation du paramètre `presentation` 

* 1: (par défaut) présenter les marges l'une sur l'autre 
* 2: marges côte à côte
* 3: dates et marges au-dessus du nom du nœud et côte à côte

```python
G1 = GrapheMPM(pred=p, pond=w, marges=True, presentation=1)
G2 = GrapheMPM(pred=p, pond=w, marges=True, presentation=2)
G3 = GrapheMPM(pred=p, pond=w, marges=True, presentation=3)
# […]
```

| `presentation=1` | `presentation=2` | `presentation=3` |
|------------------|------------------|------------------|
| <img src="illustrations/ex-full.png" width="250"> | <img src="illustrations/ex-full-2.png" width="250"> | <img src="illustrations/ex-full-3.png" width="250"> |


**Attention**: depuis la version v0.3, on initialise l'objet avec des éléments
nommés:

* au choix `pred` ou `succ` dictionnaire des prédécesseurs (resp. des successeurs)
* `pond` dictionnaire des pondérations.

Les méthodes `earliestdate, latestdate` mettent à jour les dates des nœuds et
doivent être appliquées dans le bon ordre.


**show_level** (opérationnel): ce paramètre `show_level` (`True/False`) est disponible pour
l'initialisation:

```python
G1 = GrapheMPM(pred=p, pond=w, marges=False, presentation=1, show_level=False)
G2 = GrapheMPM(pred=p, pond=w, marges=False, presentation=1, show_level=True)
# […]
```
| `show_level=False` (par défaut) | `show_level=True` |
|------------------|------------------|
| <img src="illustrations/test_sl_off.png" width="350"> | <img src="illustrations/test_sl_on.png" width="350"> |


**Astuce d'orientation**: pour les plus téméraires, vous pouvez choisir
l'orientation du graphe au moment du rendu. Il suffit de préciser la valeur de
l'attribut `rankdir` pour `.gv` qui vaut `LR` (left-right) par défaut:

```
G.gv.attr(rankdir="TB") # top-bottom
G.gv.attr(rankdir="BT") # bottom-top
G.gv.attr(rankdir="RL") # right-left
G.gv.render("image")
```
<table>
 <tbody><tr>
  <td><img src="illustrations/ex-ed-nomarge-TB.png" width="300"></td>
  <td><img src="illustrations/ex-ed-nomarge-BT.png" width="300"></td>
  <td><img src="illustrations/ex-ed-nomarge-RL.png" width="400"></td>
</tr></tbody>
</table>

objet `GrapheSimple`
---------------------

C'est une classe plus simple à charger simplement avec un dictionnaire des
prédecesseurs ou des successeurs.

On peut générer le graphe simple, ou sa version complète avec fermeture transitive.

```python
from grapheMPM import GrapheSimple, mat2tex

# dico des prédecesseurs

p = {"A": "", "B": "", "C": "A", "D": "AB", "E":"B",
     "F":"DE", "G": "E", "H":"CF", "I":"FG", "J": "HI", "K": "I"}

G = GrapheSimple(pred=p)
G.makeGraphviz()
G.gv.render("ex-simple")

G.makeGraphviz(fermeture=True)
G.gv.render("ex-simple-full")

print(mat2tex(G.mat_adj))
print(G.Matrices_latex[1]) # équivalent, la num 0 est celle de fermeture transitive

print(G.tab_latex_pred)
print(G.tab_latex_succ)
```

<table><tbody><tr>
<td>

```latex
\begin{pmatrix}
  0 & 0 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
  0 & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0\\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\\
  0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0\\
  0 & 0 & 0 & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 0\\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & 0 & 0\\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0\\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0\\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1\\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
  0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
\end{pmatrix}
```

</td>
<td>

```latex
\begin{tabular}{|c|c|}
\toprule
Sommet & Prédécesseur(s) \\
\midrule
     A &                 \\
     B &                 \\
     C &               A \\
     D &             A,B \\
     E &               B \\
     F &             D,E \\
     G &               E \\
     H &             C,F \\
     I &             F,G \\
     J &             H,I \\
     K &               I \\
\bottomrule
\end{tabular}
```

</td>
<td>

```latex
\begin{tabular}{|c|c|}
\toprule
Sommet & Successeur(s) \\
\midrule
     A &           C,D \\
     B &           D,E \\
     C &             H \\
     D &             F \\
     E &           F,G \\
     F &           H,I \\
     G &             I \\
     H &             J \\
     I &           J,K \\
     J &               \\
     K &               \\
\bottomrule
\end{tabular}
```
</td></tr></tbody></table>

**Astuce**: quand on oublie le nom des attributs disponibles, on peut lister le
contenu de l'objet en tapant `dir(G)`.


Vous pourrez observer que graphviz ne met pas forcément les sommets sur le
niveau attendu si on ne le force pas (sommet C):

<img src="illustrations/ex-simple.png" width="300"> <img src="illustrations/ex-simple-full.png" height="500">

C'est pourquoi vous pouvez désormais utiliser une class `GrapheSimpleNoCircuit`
si vous voulez insistez sur l'organisation par niveau.

<img src="illustrations/ex-simple-levels.png" width="300">

Installation ou mise à jour
===========================

Module en Python3. Il vous est conseillé d'utiliser une
version de Python >=3.4. En effet, à partir de là, l'installateur pip
standardise l'installation des modules (et utilise le plus récent format
d'archive **wheel**)

L'installateur pip veillera à installer les dépendances.

Pour Windows:

```bat
python.exe -m pip install \chemin\vers\grapheMPM-xxx-py3-none-any.whl
```

Pour GNU/Linux:

```bash
pip install  /chemin/vers/grapheMPM-xxx-py3-none-any.whl
```

Pour mettre à jour quand on a déjà le module, on peut ajouter un paramètre `-U`
ou `--upgrade` pour accepter la version la plus récente. exemple GNU/Linux:

```bash
pip install -U  /chemin/vers/grapheMPM-xxx-py3-none-any.whl
```

