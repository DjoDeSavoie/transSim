import json
import time
import os
from Server_Autorisation import traiterTransaction
from Server_Interbancaire import routageTransaction
from colorama import init, Fore

from utilz import lireFichierJson, ecrireFichierJson

# Initialiser colorama
init(autoreset=True)

dossier_logs = "logs/logsTPE/"

def traiterDemande(demande, chemin_fichier):
    if not demande["isTraite"]:
        # Convertir les valeurs en listes en une seule valeur si nécessaire
        idTPE = demande["idTPE"]
        idBanqueEmetteur = demande["idBanqueEmetteur"][0] if isinstance(demande["idBanqueEmetteur"], list) else demande["idBanqueEmetteur"]
        
        #si les deux banques participant à la transaction sont les mêmes
        if idTPE == idBanqueEmetteur:
            print(f"{Fore.CYAN}Traitement de la demande : {demande['idLog']}")
            demande["isTraite"] = True
            # Traitement de la transaction si idTPE et idBanqueEmetteur sont les mêmes, le deuxieme parametre est le chemin du fichier
            traiterTransaction(demande['idLog'], chemin_fichier) 
            
        #sinon -> on appelle le serveur interbancaire
        else: 
            #routageTransaction(demande)
            return
            # Si idTPE et idBanqueEmetteur sont différents
            #on appel la fonction du serv inter bancaire avec en paramètre les données de la transac
            

def checkDemandesNonTraitees(chemin_fichier):
    demandes = lireFichierJson(chemin_fichier)
    for demande in demandes:
        traiterDemande(demande, chemin_fichier)
    ecrireFichierJson(chemin_fichier, demandes)

def parcourirFichiersLogs(dossier):
    # Liste tous les fichiers dans le dossier logsTPE
    for filename in os.listdir(dossier):
        if filename.endswith(".json"):
            chemin_fichier = os.path.join(dossier, filename)
            checkDemandesNonTraitees(chemin_fichier)

