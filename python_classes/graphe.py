import random
import graphviz as g
import pydot
import os
import pandas as pd
import numpy as np

os.environ["PATH"] += "bin"


class DiGraphe():

    # Matrice de transition
    A: np.array
    # Ensemble des sommets
    E: list
    # Nombre de sommets
    nb_sommets: int
    # Graphe
    graph: g.Digraph
    # Seuil à partir duquel on considère qu'il est inutile de représenter un arc
    proba_mini: float

    def __init__(self, A_df: pd.DataFrame, proba_mini: float = 0, proba_faible: float = 0.1):
        self.A = np.array(A_df.transpose())
        self.E = [col for col in A_df.columns]
        self.nb_sommets = len(self.E)
        self.graph = g.Digraph(format="png")
        # Permet de générer des couleurs de façon aléatoire pour chaque sommet
        self.r = lambda: random.randint(0, 150)
        self.proba_mini = proba_mini
        self.proba_faible = proba_faible
        # Initialisation du graphe
        self.__initialiser()

    def __initialiser(self):
        """
        VA : Permet de définir les attributs du graphe à partir de la matrice de transition
        :return: None
        """
        # Ajout des sommets
        for i in range(len(self.E)):
            self.graph.node(self.E[i], self.E[i], color="black", fillcolor='#%02X%02X%02X' % (self.r(), self.r(),
                                                                        self.r()), style="filled", fontcolor="white")
        # Ajouter les arcs
        for y in range(self.nb_sommets):
            for i in range(self.nb_sommets):
                # On ne réprésente pas les chemins impossibles ou presque
                if self.A[y][i] > self.proba_mini:
                    # On met une couleur plus fable pour
                    if self.A[y][i] < self.proba_faible:
                        self.graph.edge(self.E[y], self.E[i], label=f"{self.A[y][i]}", color="orange")
                    else:
                        self.graph.edge(self.E[y], self.E[i], label=f"{self.A[y][i]}", color="red")

    def enregistrer_PNG(self, chemin_dot: str, chemin_png):
        """
        VA : Permet d'enrehistrer le graphe au format PNG à partir d'un dot file
        :param chemin_dot: Chemin où le dot file doit être enregistré
        :param chemin_png: Chemin où le graphe doit être enregistré au format png
        :return: None
        """
        # Sauvegarde du fichier .dot
        self.graph.save(chemin_dot + "graphe.dot")
        # Lecture du dot file qui contient le graphe
        (graphe,) = pydot.graph_from_dot_file(chemin_dot + "graphe.dot")
        #"static/images/graphe.png"
        # Enregistrement au format png du graphe
        graphe.write_png(chemin_png + "graphe.png")
        # Suppression du dot file qui est désormais inutile
        os.remove(chemin_dot + "graphe.dot")



