import json
import time

from Server_Autorisation import traiterTransaction
from colorama import init, Fore

# Initialiser colorama
init(autoreset=True)
chemin_fichier_json = "logs/logsTPE/logsTPE.json"

def lireFichierJson(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)

def ecrireFichierJson(chemin_fichier, contenu):
    with open(chemin_fichier, 'w') as f:
        json.dump(contenu, f, indent=4)

def traiterDemande(demande):
    if not demande["isTraite"]:
        print("Traitement de la demande : ", demande['idLog'])
        demande["isTraite"] = True

def checkDemandesNonTraitees(demandes):
    demande_a_traiter = None
    for demande in demandes:
        if not demande["isTraite"]:
            traiterDemande(demande)
            demande_a_traiter = demande
            print(f"{Fore.CYAN}Id de la demande à traiter : ", demande['idLog'])
            #on stocke la demande dans la variable idDemande
            traiterTransaction(demande['idLog'])
            break
    if demande_a_traiter is None:
        # print(f"{Fore.GREEN}Toutes les demandes ont déjà été traitées.")
        return

    # Mettre à jour la demande traitée dans le fichier JSON
    ecrireFichierJson(chemin_fichier_json, demandes)

    # Vérifier s'il y a d'autres demandes non traitées
    for demande in demandes:
        if not demande["isTraite"]:
            print(f"{Fore.CYAN}Il reste d'autres demandes non traitées.")
            break



        