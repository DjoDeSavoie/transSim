# Fichier contenant les fonctions principales du TPE

from getpass4 import getpass
from Server_NTP import getTime
from datetime import datetime
from colorama import init, Fore

import json
import os
import getpass
import pymysql
import hashlib


def hash_sha256(data):
    # Créer un objet hash SHA-256
    sha256_hash = hashlib.sha256()

    # Mettre à jour l'objet hash avec les données à hasher (doit être des bytes)
    sha256_hash.update(data.encode('utf-8'))

    # Obtenir la représentation hexadécimale du hash
    hashed_data = sha256_hash.hexdigest()

    return hashed_data


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
        {"nom": f"{Fore.GREEN}Ballon de football", "montant": 20.0, "fournisseur": ""},
        {"nom": f"{Fore.GREEN}T-shirt de sport", "montant": 15.0, "fournisseur": ""},
        {"nom": f"{Fore.GREEN}Raquette de tennis", "montant": 45.0, "fournisseur": ""}
    ]

    # Ajouter le nom du fournisseur aux produits
    for produit in produits:
        # Sélection aléatoire d'un fournisseur pour l'exemple
        fournisseur = fournisseurs[0]
        produit['fournisseur'] = f"{fournisseur[1]} {fournisseur[2]}"

    # Afficher les produits avec les noms des fournisseurs
    print(f"{Fore.CYAN}Liste des produits disponibles :")
    for idx, produit in enumerate(produits, 1):
        print(f"{idx}. {produit['nom']} - {produit['montant']}€ - Fourni par {produit['fournisseur']}")

    # Demander à l'utilisateur de choisir un produit
    choix_produit = int(input(f"{Fore.CYAN}Sélectionnez le numéro du produit que vous souhaitez acheter : "))
    produit_selectionne = produits[choix_produit - 1]

    # Récupérer l'idCompteAcquereur du fournisseur sélectionné
    idCompteAcquereur = fournisseurs[0][0]  # Même sélection que pour le produit

    # Appeler initTransac avec l'idCompteAcquereur et le montant du produit
    initTransac(idCompteAcquereur, produit_selectionne['montant'])


def verifieSolde(id_compte, type_compte):
    try:
        with db_connection.cursor() as cursor:
            if type_compte == '1':
                cursor.execute("SELECT soldeCompteEmetteur FROM comptebancaireemetteur WHERE idCompteEmetteur = %s", (hash_sha256(id_compte)))
            elif type_compte == '2':
                cursor.execute("SELECT soldeCompteAcquereur FROM comptebancaireacquereur WHERE idCompteAcquereur = %s", (hash_sha256(id_compte)))
            else:
                print(f"{Fore.RED}Type de compte non valide.")
                return None

            solde = cursor.fetchone()
            if solde:
                return solde[0]
            else:
                print(f"{Fore.RED}Aucun compte trouvé avec cet ID.")
                return None
    except pymysql.MySQLError as e:
        print(f"{Fore.RED}Erreur lors de la connexion à la base de données: {e}")
        return None

############################################################ PARTIE ENVOI AUTOR ################################################################

# Fonction pour obtenir le prochain ID
def get_next_id(file_path='logs/logsTPE/logsTPE.json'):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Trouver le plus grand idLog existant
            existing_ids = [entry['idLog'] for entry in data]
            if not existing_ids:
                next_id = 1
            else : 
                next_id = max(existing_ids) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        next_id = 1

    return next_id

# Fonction pour envoyer une autorisation au serveur d'acquisition
def EnvoiAutorisation(idComteEmetteur, idCompteAcquereur, montant):
    cheminFichier = "logs/logsTPE/logsTPE.json"

    # Vérifier si le fichier existe
    if not os.path.exists(cheminFichier):
        raise FileNotFoundError(f"{Fore.RED}Le fichier {cheminFichier} n'existe pas.")

    # Charger les données existantes ou initialiser avec une liste vide si le fichier est vide
    try:
        with open(cheminFichier, "r", encoding='utf-8') as fichier:
            try:
                donneesExistantes = json.load(fichier)
            except json.JSONDecodeError:
                # Initialiser avec une liste vide si le fichier est vide
                donneesExistantes = []
    except IOError as e:
        print(f"{Fore.RED}Une erreur est survenue lors de la lecture du fichier: {e}")
        raise

    # Obtenez le prochain ID
    next_id = get_next_id()

    # Ajouter la nouvelle ligne avec les informations
    nouvelleLigne = {
        "idLog" : next_id,
        "idTPE" : 1,
        "numero_compte_emetteur": idComteEmetteur,
        "numero_compte_acquereur": idCompteAcquereur,
        "montant_transaction": montant,
        "date_heure_transaction": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "isTraite": False
    }
    donneesExistantes.append(nouvelleLigne)

    # Sauvegarder dans le fichier JSON
    with open(cheminFichier, "w", encoding='utf-8') as fichier:
        json.dump(donneesExistantes, fichier, indent=2)

    print(f"{Fore.GREEN}Transaction enregistrée dans le fichier de logs.")
    
def convertCardtoID(numeroCarte):
    cursor = db_connection.cursor()
    cursor.execute("SELECT idCompteEmetteur FROM cartebancaire WHERE numeroCarte = %s", (numeroCarte,))
    idCompteEmetteur = cursor.fetchone()
    print("titktitkti")
    print(idCompteEmetteur)
    return idCompteEmetteur

def initTransac(idAq, montant):
    #Appel de la fonction pour récupérer les informations
    numeroCarte = GetInfosCB()

    if numeroCarte != False:
        if VerifInfosTransac(numeroCarte) == True:
            idEm = convertCardtoID(numeroCarte)
            EnvoiAutorisation(idEm, idAq, montant)
