import pandas as pd
import numpy as np
from django.http import HttpResponse, HttpRequest
import random
import graphviz as g
import pydot
import os


# Ajout du dossier bin aux variables d'environnemen
os.environ["PATH"] += "bin"
os.environ["PATH"] += ".."
from python_classes.graphe import DiGraphe
from python_classes.plot import Plot


def sauvegarder_graphe(A_file, format):
    if format == "xlsx":
        A_df = pd.read_excel(A_file)
    else:
        A_df = pd.read_csv(A_file)
    graphe = DiGraphe(A_df, proba_mini=0.000001, proba_faible=0.1)
    graphe.enregistrer_PNG("", "static/images/")


def sauvegarder_plot(B_file, format):
    if format == "xlsx":
        B_df = pd.read_excel(B_file)
    else:
        B_df = pd.read_csv(B_file)
    plot = Plot(B_df)
    plot.enregistrer("png")


def verifier_uploads(requete: HttpRequest, liste_cles: list[str]):
    """
    VA : Fonction qui permet de vérifier les fihciers renseignés ou non par l'utilisateur, ne sont concernés que les
         fichiers passés en paramètres de cette fonction
    :param requete: Requete HTTP déclenchée par l'utilisateur du site
    :param liste_cles: Liste des champs de type "fichier" à vérifier
    :return: Liste de booléen, chaque indice indique si oui ou non le fichier est présent
    """
    # Liste qui inidique si un fichier est uploadé ou non
    uploads: list[bool] = []

    if requete.method == "POST":
        for clee in liste_cles:
            # Si dans l'array FILES il y a la clée recherchée
            if clee in requete.FILES.keys() and (str(requete.FILES[clee]).endswith("xlsx") or str(requete.FILES[clee]).endswith("csv")):
                uploads.append(True)
            else:
                uploads.append(False)
    return uploads



def verifier_formats(requete: HttpRequest, liste_cles: list[str]):
    """
    VA : Fonction qui permet de vérifier les fihciers renseignés ou non par l'utilisateur, ne sont concernés que les
         fichiers passés en paramètres de cette fonction
    :param requete: Requete HTTP déclenchée par l'utilisateur du site
    :param liste_cles: Liste des champs de type "fichier" à vérifier
    :return: Liste de booléen, chaque indice indique si oui ou non le fichier est présent
    """
    # Liste qui inidique si un fichier est uploadé ou non
    formats: list[str] = []

    if requete.method == "POST":
        for clee in liste_cles:
            # Si dans l'array FILES il y a la clée recherchée
            if clee in requete.FILES.keys():
                formats.append(str(requete.FILES[clee]).split(".")[1])

    return formats


"""def verifier_format_uploads(requete: HttpRequest, liste_extensions: list[str]):
    format_valide: list[bool] ="""
