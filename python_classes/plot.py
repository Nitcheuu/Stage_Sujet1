import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats


class Plot:

    # Dataframe qui permet de lire et traiter les données upload par l'utilisateur
    df: pd.DataFrame
    # Liste qui contient le nom des variables étudiées (CO2, dCO2, ...)
    nom_variables: list[str]
    # Liste de dataframes qui contiennent les infos de chaque variable
    dataframe_variables: list[pd.DataFrame]
    # Dimensions du plot (car il se présente sous forme de matrice)
    dimensions: (int, int)

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.nom_variables = []
        self.dataframe_variables = []
        self.__extraction()
        self.dimensions = (1, 1) # Valeur par défaut
        self.trouver_dimension_plot()



    def __extraction(self):
        """
        VA : Permet d'extraire les données qui contiennent les informations sur les variables
        :return: None
        """
        # Les indices permettent de séparer les informations
        indice_debut: int = 0
        indice_fin: int = 0
        for i in range(len(self.df)):
            # SI on rencontre le séparateur, alors on passe à une nouvelle variable
            if self.df[self.df.columns[0]][i] == "//":
                # Extraction du nom de la variable
                self.nom_variables.append(self.df[self.df.columns[1]][i])
                # Extraction des moyenens et variances pour la variable
                self.dataframe_variables.append(self.df[indice_debut:indice_fin])
                indice_debut = indice_fin + 1
            indice_fin += 1

    def trouver_dimension_plot(self):
        """
        VA : Le rendu du plot se présente sous forme de matrice de dimension (n/2, 2) ou (n/2+1,2) il faut donc calculer
        les dimensions du plot
        :return: None
        """
        # Quand le nombre de variable est pair => (n/2, 2)
        if len(self.nom_variables) % 2 == 0:
            self.dimensions = int(len(self.nom_variables) / 2), 2
        # Quand le nombre de variable est impair => (n/2+1, 2)
        else:
            self.dimensions = int(len(self.nom_variables) // 2 + 1), 2

    def enregistrer(self, format: str):
        fig, axes = plt.subplots(self.dimensions[0], self.dimensions[1], figsize=(20, 6 * self.dimensions[0]))
        compteur = 1
        for i in range(len(axes)):
            for y in range(len(axes[i])):
                if compteur <= len(self.nom_variables):
                    legend = []
                    data = np.array(self.dataframe_variables[compteur - 1])
                    print(data)

                    for z in range(len(data)):
                        moyenne = float(data[z][0])
                        variance = float(data[z][1])
                        sigma = math.sqrt(variance)
                        x = np.linspace(moyenne - 3 * sigma, moyenne + 3 * sigma, 100000)
                        axes[i][y].plot(x, stats.norm.pdf(x, moyenne, sigma))
                        legend.append(f"Etat {z + 1}")

                    axes[i][y].legend(legend)
                    axes[i][y].set_title(self.nom_variables[compteur - 1])
                    compteur += 1

        fig.savefig(f"static/images/plot.{format}")

