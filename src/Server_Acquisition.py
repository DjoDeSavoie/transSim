#Fichier contenant les fonctions du serveur d'acquisition

#Le serveur d'acquisition consiste en une boucle sans fin qui consulte le fichier de logs  et traite les transactions en attente


#Importation des modules nécessaires

import json

valeurIndiceLecture = 0

# Fonction de lecture du fichier json de la banque correspondante
def lireFichierJson():
    try:
        with open("logs/logsTPE/logsTPE.json", 'r') as fichier:
            donnees = json.load(fichier)
        return donnees
    except json.JSONDecodeError:
        print("Erreur : Le fichier JSON est vide ou mal formaté.")
        return None

#effectue une lecture en boucle pour accéder à la derniere transaction en attente (non traitée)
def lireTransactionEnAttente():
    donnees = lireFichierJson()
    
    #verification si fichier vide
    if donnees is None:
        print("Le fichier est vide")
        return False
    
    #si fichier non vide
    while True:
        for transaction in donnees:
            if transaction["isTraite"] == False:
                print(transaction)
                transaction["isTraite"] = True
                with open("logs/logsTPE/logsTPE.json", 'w') as fichier:
                    json.dump(donnees, fichier, indent=4)
                return transaction
        print(donnees)
        return
        
        
lireTransactionEnAttente()

