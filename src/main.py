#Fichier qui contient le code principal du programme, c'est-à-dire le menu principal
# pour choisir si on veut effectuer une transaction, verifier son solde, se connecter 
# ou quitter le programme 

from TPE import *
from Server_Autorisation import *
from Server_Acquisition import *
from creationData.creationBanque import creer_banque
from creationData.creationComptesAcquereur import creerCompteAcquereur
from creationData.creationComptesEmetteur import creerCompteEmetteur
from colorama import init, Fore
import threading

# Initialiser colorama
init(autoreset=True)

# Fonction wrapper pour Server_Acquisition.py

def run_server_acquisition(dossier_logs):
    print(f"{Fore.YELLOW}Serveur d'acquisition en cours d'exécution...")

    while True:
        parcourirFichiersLogs(dossier_logs)
        # Attendre un certain temps avant de vérifier à nouveau les fichiers JSON
        time.sleep(3)  # Attendre 3 secondes avant la prochaine vérification

    
# Fonction pour démarrer le server acquisition dans un autre thread
def start_server_acquisition(dossier_logs):
    acquisition_thread = threading.Thread(target=run_server_acquisition, args=(dossier_logs,))
    acquisition_thread.daemon = True  # Le thread sera tué lorsque le programme principal se termine
    acquisition_thread.start()

# Fonction pour vérifier le solde
def verifier_solde():
    type_compte = input(f"{Fore.YELLOW}Entrez le type de votre compte ('emetteur' : 1 ou 'acquereur': 2) :")
    id_compte = input(f"{Fore.YELLOW}Entrez l'ID de votre compte : ")
    solde = verifieSolde(id_compte, type_compte)
    if solde is not None:
        print(f"{Fore.CYAN}Le solde de votre compte est de {solde}€.")

# Menu principal
def menu_principal():
    while True:
        time.sleep(3)
        print(f"\n{Fore.CYAN}----- MENU PRINCIPAL -----")
        print("1. Créer une banque")
        print("2. Créer un compte acquéreur")
        print("3. Créer un compte émetteur")
        print("4. Vérifier le solde")
        print("5. Acheter un produit")
        print("0. Quitter")

        choix = input("Entrez votre choix: ")

        if choix == '1':
            nom_banque = input("Entrez le nom de la banque: ")
            creer_banque(nom_banque)
        elif choix == '2':
            creerCompteAcquereur()
        elif choix == '3':
            creerCompteEmetteur()
        elif choix == '4':
            verifier_solde()
        elif choix == '5':
            acheter_produit()
        elif choix == '0':
            print(f"{Fore.YELLOW}Programme terminé. Au revoir!")
            break
        else:
            print(f"{Fore.RED}Choix invalide! Veuillez réessayer.")

if __name__ == "__main__":
    dossier_logs = "logs/logsTPE/"
    # Lancer le server acquisition dans un thread séparé
    start_server_acquisition(dossier_logs)
    
    # Lancer le menu principal
    menu_principal()