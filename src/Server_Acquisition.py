#Fichier contenant les fonctions du serveur d'acquisition

#Le serveur d'acquisition consiste en une boucle sans fin qui consulte le fichier de logs  et traite les transactions en attente


#Importation des modules nécessaires

import json


#Fonction de lecture du fichier json de la banque correspondante
def lireFichierJson():
    with open("logs/logsTPE/logsTPE.json", 'r') as fichier:
        donnees = json.load(fichier)
    return donnees

#effectue une lecture en boucle pour accéder à la dernier transaction en attente
def lireTransactionEnAttente():
    donnees = lireFichierJson()
    while True:
        for transaction in donnees:
            if transaction["isTraite"] == False:
                print(transaction)
                transaction["isTraite"] = True
                with open("logs/logsTPE/logsTPE.json", 'w') as fichier:
                    json.dump(donnees, fichier, indent=4)
                return transaction
        print(donnees)
        
        
lireTransactionEnAttente()
