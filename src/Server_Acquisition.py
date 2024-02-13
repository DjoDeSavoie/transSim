import json
import time
import os
from Server_Autorisation import traiterTransaction
from colorama import init, Fore

# Initialiser colorama
init(autoreset=True)

dossier_logs = "logs/logsTPE/"

def lireFichierJson(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)

def ecrireFichierJson(chemin_fichier, contenu):
    with open(chemin_fichier, 'w') as f:
        json.dump(contenu, f, indent=4)

def traiterDemande(demande, chemin_fichier):
    if not demande["isTraite"]:
        # Convertir les valeurs en listes en une seule valeur si nécessaire
        idTPE = demande["idTPE"]
        idBanqueEmetteur = demande["idBanqueEmetteur"][0] if isinstance(demande["idBanqueEmetteur"], list) else demande["idBanqueEmetteur"]
        
        if idTPE == idBanqueEmetteur:
            print(f"{Fore.CYAN}Traitement de la demande : {demande['idLog']}")
            demande["isTraite"] = True
            # Traitement de la transaction si idTPE et idBanqueEmetteur sont les mêmes, le deuxieme parametre est le chemin du fichier
            traiterTransaction(demande['idLog'], chemin_fichier) 
        else:
            # appeler reseau interbancaire
            #print(f"{Fore.YELLOW}La demande {demande['idLog']} ne correspond pas à la banque émetteur.")
            print()

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

