#Fichier contenant les fonctions du serveur d'acquisition

#Le serveur d'acquisition consiste en une boucle sans fin qui consulte le fichier de logs  et traite les transactions en attente


#Importation des modules nécessaires

import json


#Fonction de lecture du fichier json de la banque correspondante
def lireFichierJson(nomBanque):
    with open("logs/logsTPE/fichierLogsTPE" + str(nomBanque.capitalize()) + ".json", 'r') as fichier:
        donnees = json.load(fichier)
    return donnees