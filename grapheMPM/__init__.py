from numpy import matrix, prod, float_, round, floor
from graphviz import Digraph
from lxml import etree

class noeud():
    def __init__(self,titre,presentation=1,**kwargs):
        """initialisation d'un nœud dans un graphe MPM (potentiels Metra)
        les kwargs contiennent:
        ed: earliest date, la date au plus tôt
        ld: latest date, la date au plus tard
        ml: marge libre
        mt: marge totale

        :param presentation: in [1,2] choisir 1: ml sur mt, 2: ml-mt côte
             à côte
        :type presentation: int
        """
        self.data = {"ed": "    ", "ld": "    ",
                     "ml": "    ", "mt": "    "}
        self.data.update(kwargs)
        self.titre = titre
        self.presentation = presentation
        self.setdata(**kwargs)

    def setdata(self,**kwargs):
        """mettre à jour les données du noeud
        les paramètres doivent être de type str
        """
        self.data.update(kwargs)
        E = etree.Element("TABLE")
        D = {"BORDER":"0", "CELLBORDER":"1",
             "CELLSPACING":"0", "CELLPADDING":"4"}
        E.attrib.update(D)

        T1 = etree.SubElement(E, "TR")
        ti = etree.SubElement(T1, "TD")
        ti.text = self.titre
        ti.attrib["COLSPAN"]= str(2)
        ti.attrib["PORT"]="here"

        T2 = etree.SubElement(E,"TR")
        t21 = etree.SubElement(T2, "TD")
        t21.text=self.data["ed"]
        t22 = etree.SubElement(T2, "TD")
        t22.text=self.data["ld"]
        if self.presentation==1:
            T3 = etree.SubElement(E,"TR")
            t31 = etree.SubElement(T3, "TD")
            t31.text=self.data["ml"]
            t31.attrib["COLSPAN"]= str(2)
            T4 = etree.SubElement(E,"TR")
            t41 = etree.SubElement(T4, "TD")
            t41.text=self.data["mt"]
            t41.attrib["COLSPAN"]= str(2)
        elif self.presentation==2:
            T3 = etree.SubElement(E,"TR")
            t31 = etree.SubElement(T3, "TD")
            t31.text=self.data["ml"]
            t32 = etree.SubElement(T3, "TD")
            t32.text=self.data["mt"]
        self.noeud = str(etree.tostring(E),'utf-8')


class GrapheMPM():
    """Classe de génération d'un graphe d'ordonnancement par les potentiels
    Métra.

    Initialisation possible via (successeurs ou prédécesseur ) et pondérations.

    Exemple::

    >>>p = {"déb":"", "A":['déb'], "B":['déb'], "C": "A", "D": "AB", "E":"B",
       "F":"DE", "G": "E", "H":"CF", "I":"FG", "J": "HI", "fin": "J"}
    >>>w = {"déb": 0, "fin": 0,"A": 7, "B": 3, "C": 4, "D": 2, "E": 8,
       "F": 6, "G": 5, "H": 7, "I": 5, "J": 3}
    >>>G = GrapheMPM(pred=p, pond=w)
    >>>G.setlevel()
    >>>G.earliestdate()
    >>>G.makeGraphviz()
    >>>G.gv.render("ex-ed")
    >>>G.latestdate()
    >>>G.makeGraphviz()
    >>>G.gv.render("ex-full")
    """
    
    def __init__(self, succ=None, pred=None, pond=None, presentation=1):
        """instanciation d'un graphe MPM
        2 possibilités d'initialisation avec l'un des dictionnaires
        succ: dico des successeurs
        pred: dico des prédecesseurs

        pond: dico des poids des arcs (durées des tâches)
        :param presentation: in [1,2] choisir 1: ml sur mt, 2: ml -mt côte
             à côte
        :type presentation: int
        """
        # calcul du nombre de chiffres max après la virgule pour arrondir
        # ensuite
        self.prec=max([len(str(v).partition(".")[2]) for v in pond.values()])
        self.ponderation = dict([(k, self._nb(str(e))) for k,e in pond.items()])
        
        if succ:
            self.successeurs = succ
            # sommets: set(succ.keys())
            self.sommets = {}
            for k in succ.keys():
                self.sommets[k] = noeud(k,presentation=presentation)
            s = list(succ.keys()) # list des sommets
            ssort = sorted(s)
            N = len(ssort)
            d = dict(zip(range(1,N+1),ssort))
            self.num_sommets = d
            self.mat_adj = matrix([[ (1 if (d[j] in succ[d[i]]) else 0)
                                     for j in range(1,N+1)]
                                   for i in range(1,N+1)])
            # dico des prédecesseurs
            P = {}
            for i in range(1,N+1):
                pi = [d[j+1] for j in range(N) if self.mat_adj[j,i-1] != 0]
                P[d[i]] = pi
            self.predecesseurs = P
        elif pred:
            self.predecesseurs = pred
            # sommets: set(succ.keys())
            self.sommets = {}
            for k in pred.keys():
                self.sommets[k] = noeud(k,presentation=presentation)
            s = list(pred.keys()) # list des sommets
            ssort = sorted(s)
            N = len(ssort)
            d = dict(zip(range(1,N+1),ssort))
            self.num_sommets = d
            self.mat_adj = matrix([[ (1 if (d[i] in pred[d[j]]) else 0)
                                     for j in range(1,N+1)]
                                   for i in range(1,N+1)])
            # dico des successeurs
            S = {}
            for i in range(1,N+1):
                pi = [d[j+1] for j in range(N) if self.mat_adj[i-1,j] != 0]
                S[d[i]] = pi
            self.successeurs = S

    def makeGraphviz(self):
        """générer l'objet graphviz
        :rtype: None
        """
        dot = Digraph(comment="graphe MPM",
                      node_attr={"shape":"plaintext"})
        dot.attr("graph",rankdir="LR")
        dot.format ="png"
        # création des sous-graphes par niveau
        NIVtmp = list(set(self.niveaux.values()))
        NIV = sorted(NIVtmp)
        for N in NIV:
            with dot.subgraph(name="cluster_{}".format(N),
                              node_attr={'rank': 'same'}) as c:
                c.attr(style="invis") # désactivation du cadre de cluster
                for k,n in self.sommets.items(): # key, noeud
                    if self.niveaux[k] == N:
                        c.node(str(k), "<{}>".format(n.noeud))
            # la str html doit être encadrée de <>

        for k,L in self.successeurs.items():
            for i in list(L):
                dot.edge(k, i, label=str(self.ponderation[k]),
                         tailport="here", headport="here")
        self.gv = dot

    def setlevel(self):
        """calculer les niveaux des sommets
        créer un attribut niveaux de type dict.
        :rtype: None
        """
        A = self.mat_adj.copy()
        L = [(i+1) for i in range(len(A)) if self.col_is_null(A,i)]
        c=0 # compteur de niveau
        D ={} # dico des niveaux
        for e in L: # mise à jour niveau 0
            D[e]=c
        while len(D)<len(A):
            c+=1
            A *= self.mat_adj
            M = L
            L = [(i+1) for i in range(len(A)) if self.col_is_null(A,i)]
            delta = set(L).difference(set(M)) # calcul des nv sommets sans pred
            for e in delta: # mise à jour niveau c
                D[e]=c
        D1 = [ (self.num_sommets[k], v) for k,v in D.items()]
        self.niveaux = dict(D1)
        
    def col_is_null(self, M, i):
        """la colonne i de M est-elle nulle?"""
        return sum(M[:,i])==0

    def _nb(self, s):
        """convertir la chaîne de caractère s en nombre int ou float
        si s contient un . on renvoie un numpy.float_ sinon un int
        """
        return (float_(s) if "." in s else int(s))

    def _pretty(self, n):
        """convertir un nombre n en string selon qu'il soit int ou float_
        en tenant compte de la précision calculée dans self.prec dans __init__
        """
        if n==floor(n): # n est int
            return str(n)
        else:
            return str(round(n, self.prec))
    
    def earliestdate(self):
        """màj des données de ed des nœuds"""
        Ltmp = list(self.niveaux.items())
        L = sorted(Ltmp, key=lambda e:e[1]) # tri sur niveau
        for s,n in L:
            # on ajoute le poids de la tâche précédente e
            poids_pred = [self._nb(self.sommets[e].data["ed"])
                          +self.ponderation[e]
                          for e in self.predecesseurs[s]]
            m = (max(poids_pred) if len(poids_pred)>0 else 0)
            self.sommets[s].setdata(ed=self._pretty(m))

    def latestdate(self):
        """màj des données de ld des nœuds, à faire après earliestdate()
        """
        Ltmp = list(self.niveaux.items())
        L = sorted(Ltmp, key=lambda e:e[1]) # tri sur niveau
        L.reverse() # en ordre décroissant
        for s,n in L:
            # on soustrait le poids de la tâche actuelle s
            poids_suc = [self._nb(self.sommets[e].data["ld"])
                         -self.ponderation[s]
                         for e in self.successeurs[s]]
            ld = (min(poids_suc) if len(poids_suc)>0 else
                  self._nb(self.sommets[s].data["ed"]))
            self.sommets[s].setdata(ld=self._pretty(ld))
            # on en profite pour faire la marge libre
            tmp =[self._nb(self.sommets[e].data["ed"])-self.ponderation[s]\
                  -self._nb(self.sommets[s].data["ed"])
                      for e in self.successeurs[s]]
            ml = (min(tmp) if len(tmp)>0 else 0) #self.sommets[s].data["ed"]
            #marge totale
            mt = self._nb(self.sommets[s].data["ld"])\
                 -self._nb(self.sommets[s].data["ed"])
            self.sommets[s].setdata(mt=self._pretty(mt), ml=self._pretty(ml))

