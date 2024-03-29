# Fichier contenant les fonctions principales du TPE

from getpass4 import getpass
from Server_NTP import getTime
from datetime import datetime
from colorama import init, Fore
from utilz import hash_sha256, creeFichierLogs

import json
import os
import getpass
import pymysql
import random


# Initialiser colorama
init(autoreset=True)

############################################################ PARTIE VERIFICATION CB ################################################################

db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')

def GetInfosCB():
    # Connexion à la base de données
    db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
    print(f"{Fore.CYAN}Entrez votre numéro de carte bancaire :")
    numeroCarte = input()
    numeroCarte = hash_sha256(numeroCarte)
    # Vérification de l'existence de la carte bancaire
    if verifSiExisteCB(numeroCarte, db_connection) == False:
        print(f"{Fore.RED}Votre numéro de carte n'existe pas")
        return False
    else :
        return numeroCarte


def VerifInfosTransac(numeroCarte):
    # Connexion à la base de données
    db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
    
    # Vérification de la validité de la carte bancaire
    print(f"{Fore.CYAN}Entrez la date d'expiration de votre carte (MM/AA) : ")
    date_exp_utilisateur = input()
    infosCB = recupere_infos_cb(numeroCarte, db_connection)

    # Si la date d'expiration est incorrecte ou la carte est expirée
    if not verifDateExp(date_exp_utilisateur, infosCB[2], db_connection):
        print(f"{Fore.RED}La date d'expiration est incorrecte ou votre carte est expirée.")
        return False

    # Vérification du code PIN
    tentatives = 0
    while tentatives < 3:
        pin = getpass.getpass(f"{Fore.CYAN}Veuillez entrer votre code PIN : ")
        pin = hash_sha256(str(pin))
        if verifPin(infosCB, pin, db_connection):
            print(f"{Fore.GREEN}Vérification réussie.")
            return True
        else:
            tentatives += 1
            print(f"{Fore.RED}Tentative {tentatives} de 3.")
    print(f"{Fore.RED}Votre code PIN est incorrect. Carte bloquée.")
    bloqueCarte(numeroCarte, db_connection)
    return False

def verifSiExisteCB(numeroCarte, db_connection):
    # Vérifie si le numéro de carte existe dans la base de données
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM cartebancaire WHERE numeroCarte = %s", (numeroCarte))
        (count,) = cursor.fetchone()
        return count > 0

def recupere_infos_cb(numeroCarte, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT numeroCarte, idCompteEmetteur, dateExpiration, validite, pin, cryptogramme FROM cartebancaire WHERE numeroCarte = %s", (numeroCarte))
        return cursor.fetchone()

def verifPin(infos_cb, pin_saisi, db_connection):
    numeroCarte, idCompteEmetteur, dateExpiration, validite, pin_correct, cryptogramme = infos_cb

    if not validite:
        print(f"{Fore.RED}Carte bloquée")
        return False

    if pin_saisi != pin_correct:
        print(f"{Fore.RED}PIN invalide.")
        return False

    return True

def bloqueCarte(numeroCarte, db_connection):
    with db_connection.cursor() as cursor:
        update_query = "UPDATE cartebancaire SET validite = 0 WHERE numeroCarte = %s;"
        cursor.execute(update_query, (hash_sha256(numeroCarte)))
        db_connection.commit()

def DebloqueCarte(numeroCarte, db_connection):
    with db_connection.cursor() as cursor:
        update_query = "UPDATE cartebancaire SET validite = 1 WHERE numeroCarte = %s;"
        cursor.execute(update_query, (hash_sha256(numeroCarte)))
        db_connection.commit()


def verifDateExp(date_exp_utilisateur, date_exp_db, db_connection):
    # Formatage de la date d'expiration de la base de données en chaîne
    date_exp_db_str = date_exp_db.strftime('%m/%y')  # Format MM/AA

    # Comparaison des dates d'expiration
    if date_exp_utilisateur != date_exp_db_str:
        print(f"{Fore.RED}La date d'expiration entrée ne correspond pas à celle de la base de données.")
        return False

    # Vérification de la validité de la date par rapport au serveur NTP
    ntp_time = getTime()
    ntp_date = datetime.strptime(ntp_time, "%a %b %d %H:%M:%S %Y")
    
    # Date d'expiration à partir de la base de données
    exp_date = datetime.strptime('20' + date_exp_db.strftime('%y-%m-01'), '%Y-%m-%d')
    
    # Vérifie si la carte est expirée
    if exp_date < ntp_date:
        print(f"{Fore.RED}La carte est expirée.")
        return False
    
    return True

# Fonction pour acheter un produit
def acheter_produit():
    cursor = db_connection.cursor()
    cursor.execute("SELECT idCompteAcquereur, nom, prenom FROM comptebancaireacquereur")
    fournisseurs = cursor.fetchall()

    # Créer une liste de produits fictifs avec des montants
    produits = [
    {"nom": "Ballon de football", "montant": 20.0},
    {"nom": "T-shirt de sport", "montant": 15.0},
    {"nom": "Raquette de tennis", "montant": 45.0},
    {"nom": "Chaussures de running", "montant": 50.0},
    {"nom": "Sac de sport", "montant": 25.0},
    {"nom": "Montre de fitness", "montant": 70.0},
    {"nom": "Bandes de résistance", "montant": 30.0},
    {"nom": "Gourde", "montant": 10.0},
    {"nom": "Casquette", "montant": 12.0},
    {"nom": "Serviette de sport", "montant": 7.5}
]

    # Ajouter le nom du fournisseur aux produits de manière aléatoire
    for produit in produits:
        fournisseur = random.choice(fournisseurs)  # Choix aléatoire d'un fournisseur
        produit['fournisseur'] = f"{fournisseur[1]} {fournisseur[2]}"
        produit['idCompteAcquereur'] = fournisseur[0]  # Ajouter l'ID du fournisseur

    # Afficher les produits avec les noms des fournisseurs
    print(f"{Fore.CYAN}Liste des produits disponibles :")
    for idx, produit in enumerate(produits, 1):
        print(f"{Fore.GREEN}{idx}. {produit['nom']} - {produit['montant']}€ - Fourni par {Fore.WHITE}{produit['fournisseur']}{Fore.GREEN}")

    # Demander à l'utilisateur de choisir un produit
    choix_produit = int(input(f"{Fore.CYAN}Sélectionnez le numéro du produit que vous souhaitez acheter : "))
    produit_selectionne = produits[choix_produit - 1]

    # Utiliser l'idCompteAcquereur du fournisseur sélectionné pour le produit
    idCompteAcquereur = produit_selectionne['idCompteAcquereur']

    # Appeler initTransac avec l'idCompteAcquereur et le montant du produit
    initTransac(idCompteAcquereur, produit_selectionne['montant'])

    printTicket()

def printTicket():
    try:
        with db_connection.cursor() as cursor:
            # Sélectionnez la dernière entrée ajoutée à la table autorisationtransaction
            cursor.execute("""
                SELECT numeroAutorisation, idBanqueEmetteur, dateAutorisation, montantAutorisation
                FROM autorisationtransaction
                ORDER BY numeroAutorisation DESC
                LIMIT 1
            """)
            dernier_log = cursor.fetchone()

            if dernier_log:
                # Afficher le ticket de caisse
                print("Ticket de caisse:".center(40, "-"))
                print(f"Numéro d'autorisation : {dernier_log[0]}")
                print(f"ID de la banque émettrice : {dernier_log[1]}")
                print(f"Date d'autorisation : {dernier_log[2].strftime('%d/%m/%Y')}")
                print(f"Montant de l'autorisation : {dernier_log[3]} EUR")
                print("".center(40, "-"))
            else:
                print("Aucun log trouvé dans la base de données.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la récupération du dernier log: {e}")
    
############################################################ PARTIE ENVOI TRANS ################################################################

# Fonction pour obtenir le prochain ID
def get_next_id(donneesExistantes):
    # Cette fonction devrait générer le prochain ID de log basé sur les données existantes
    # Par exemple, en prenant l'ID le plus élevé et en ajoutant 1
    if donneesExistantes:
        return max(demande["idLog"] for demande in donneesExistantes) + 1
    else:
        return 1


def EnvoiAutorisation(idCompteEmetteur, idCompteAcquereur, montant):
    try:
        with db_connection.cursor() as cursor:
            # Récupérer l'ID de la banque acquéreur
            cursor.execute("SELECT idBanqueAcquereur FROM comptebancaireacquereur WHERE idCompteAcquereur = %s", (idCompteAcquereur,))
            idBanqueAcquereur = cursor.fetchone()[0]

            # Récupérer le nom de la banque acquéreur
            cursor.execute("SELECT nomBanque FROM banque WHERE idBanque = %s", (idBanqueAcquereur,))
            nomBanque = cursor.fetchone()[0]

            # Définir le chemin du fichier de logs basé sur le nom de la banque
            nomFichierLogs = f"logs/logsTPE/logsTPE_{nomBanque}.json"

            # Créer le fichier de logs s'il n'existe pas et obtenir les données existantes
            donneesExistantes = creeFichierLogs(nomFichierLogs)

            # Obtenez le prochain ID de log
            next_id = get_next_id(donneesExistantes)

            cursor = db_connection.cursor()
            cursor.execute("SELECT idBanqueEmetteur FROM comptebancaireemetteur WHERE idCompteEmetteur = %s", (idCompteEmetteur))
            idBanqueEmetteur = cursor.fetchone()[0]

            # Créer la nouvelle ligne pour le log
            nouvelleLigne = {
                "idLog": next_id,
                "idBanqueAcquereur": idBanqueAcquereur,  # Utiliser l'ID de la banque acquéreur
                "idBanqueEmetteur": idBanqueEmetteur,
                "numero_compte_emetteur": idCompteEmetteur,
                "numero_compte_acquereur": idCompteAcquereur,
                "montant_transaction": montant,
                "date_heure_transaction": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "isTraite": False,
                "hasToBeRouted": False if idBanqueAcquereur == idBanqueEmetteur else True
            }

            # Ajouter la nouvelle ligne aux données existantes
            donneesExistantes.append(nouvelleLigne)

            # Sauvegarder les données mises à jour dans le fichier de logs
            with open(nomFichierLogs, 'w', encoding='utf-8') as fichier:
                json.dump(donneesExistantes, fichier, indent=4)

            print(f"{Fore.GREEN}Transaction enregistrée dans le fichier de logs de {nomBanque}.")

    except pymysql.MySQLError as e:
        print(f"{Fore.RED}Erreur lors de la récupération des informations de la banque: {e}")


def convertCardtoID(numeroCarte):
    cursor = db_connection.cursor()
    cursor.execute("SELECT idCompteEmetteur FROM cartebancaire WHERE numeroCarte = %s", (numeroCarte,))
    idCompteEmetteur = cursor.fetchone()[0]
    return idCompteEmetteur

def initTransac(idAq, montant):
    #Appel de la fonction pour récupérer les informations
    numeroCarte = GetInfosCB()

    if numeroCarte != False:
        if VerifInfosTransac(numeroCarte) == True:
            idEm = convertCardtoID(numeroCarte)
            EnvoiAutorisation(idEm, idAq, montant)
