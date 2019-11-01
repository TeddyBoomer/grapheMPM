from numpy import matrix, prod
from graphviz import Digraph
from lxml import etree

class noeud():
    def __init__(self,titre,**kwargs):
        """initialisation d'un nœud dans un graphe MPM (potentiels Metra)
        les kwargs contiennent:
        ed: earliest date, la date au plus tôt
        ld: latest date, la date au plus tard
        ml: marge libre
        mt: marge totale
        """
        self.data = {"ed": "    ", "ld": "    ",
                     "ml": "    ", "mt": "    "}
        self.data.update(kwargs)
        self.titre = titre
        self.setdata(**kwargs)

    def setdata(self,**kwargs):
        """mettre à jour les données du noeud
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

        T2 = etree.SubElement(E,"TR")
        t21 = etree.SubElement(T2, "TD")
        t21.text=self.data["ed"]
        t21.attrib["PORT"]="to"
        t22 = etree.SubElement(T2, "TD")
        t22.text=self.data["ld"]
        t22.attrib["PORT"]="from"
        T3 = etree.SubElement(E,"TR")
        t31 = etree.SubElement(T3, "TD")
        t31.text=self.data["ml"]
        t31.attrib["COLSPAN"]= str(2)
        T4 = etree.SubElement(E,"TR")
        t41 = etree.SubElement(T4, "TD")
        t41.text=self.data["mt"]
        t41.attrib["COLSPAN"]= str(2)
        self.noeud = str(etree.tostring(E),'utf-8')


class GrapheMPM():
    def __init__(self, S, L):
        """instanciation d'un graphe MPM
        S: dico des successeurs
        L: dico des poids des arcs (durées des tâches)
        """
        self.successeurs = S
        # sommets: set(S.keys())
        self.ponderation = L
        self.sommets = {}
        for k in S.keys():
            self.sommets[k] = noeud(k)
        s = list(S.keys()) # list des sommets
        ssort = sorted(s)
        N = len(ssort)
        d = dict(zip(range(1,N+1),ssort))
        self.num_sommets = d
        self.mat_adj = matrix([[ (1 if (d[j] in S[d[i]]) else 0)
                                 for j in range(1,N+1)] for i in range(1,N+1)])
        # dico des prédecesseurs
        P = {}
        for i in range(1,N+1):
            pi = [d[j+1] for j in range(N) if self.mat_adj[j,i-1] != 0]
            P[d[i]] = pi
        self.predecesseurs = P

    def makeGraphviz(self):
        """générer l'objet graphviz
        :rtype: None
        """
        dot = Digraph(comment="graphe MPM",
                      node_attr={"rank":"same", "shape":"plaintext"})
        dot.attr("graph",rankdir="LR")
        dot.format ="png"
        for k,n in self.sommets.items(): # key, noeud
            dot.node(str(k), "<{}>".format(n.noeud))
            # la str html doit être encadrée de <>

        for k,L in self.successeurs.items():
            for i in list(L):
                dot.edge(k, i, label=str(self.ponderation[k]),
                         tailport="from", headport="to")
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
        
    def col_is_null(self,M, i):
        """la colonne i de M est-elle nulle?"""
        return sum(M[:,i])==0

    def earliestdate(self):
        """màj des données de ed des nœuds"""
        Ltmp = list(self.niveaux.items())
        L = sorted(Ltmp, key=lambda e:e[1]) # tri sur niveau
        for s,n in L:
            # on ajoute le poids de la tâche précédente e
            poids_pred = [int(self.sommets[e].data["ed"])+self.ponderation[e]
                          for e in self.predecesseurs[s]]
            m = (max(poids_pred) if len(poids_pred)>0 else 0)
            self.sommets[s].setdata(ed=str(m))

    def latestdate(self):
        """màj des données de ld des nœuds, à faire après earliestdate()
        """
        Ltmp = list(self.niveaux.items())
        L = sorted(Ltmp, key=lambda e:e[1]) # tri sur niveau
        L.reverse() # en ordre décroissant
        for s,n in L:
            # on soustrait le poids de la tâche actuelle s
            poids_suc = [int(self.sommets[e].data["ld"])-self.ponderation[s]
                         for e in self.successeurs[s]]
            ld = (min(poids_suc) if len(poids_suc)>0 else
                  self.sommets[s].data["ed"])
            self.sommets[s].setdata(ld=str(ld))
            # on en profite pour faire la marge libre
            tmp =[int(self.sommets[e].data["ed"])-self.ponderation[s]\
                  -int(self.sommets[s].data["ed"])
                      for e in self.successeurs[s]]
            ml = (min(tmp) if len(tmp)>0 else self.sommets[s].data["ed"])
            #marge totale
            mt = int(self.sommets[s].data["ld"])-int(self.sommets[s].data["ed"])
            self.sommets[s].setdata(mt=str(mt), ml=str(ml))

