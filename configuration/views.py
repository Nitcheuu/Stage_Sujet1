from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .utils import *
import pandas as pd
# Create your views here.


def home(request : HttpRequest):
    data = {
        "uploads": verifier_uploads(request, ["input_A", "input_B"]),
        "formats": verifier_formats(request, ["input_A", "input_B"]),
        "methode_requete": request.method
    }
    print(type(data["methode_requete"]))
    if request.method == "GET":
        return render(request, 'configuration/configuration.html', data)
    elif not data["uploads"][0] or not data["uploads"][1]:
        return render(request, 'configuration/configuration.html', data)
    elif request.method == "POST":
        sauvegarder_graphe(request.FILES["input_A"], data["formats"][0])
        sauvegarder_plot(request.FILES["input_B"], data["formats"][1])
        return render(request, 'configuration/resultat.html', data)
