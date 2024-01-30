# Fichier contenant les fonctions principales du TPE

from getpass4 import getpass
from Server_NTP import getTime
from datetime import datetime

import json
import os
import getpass
import pymysql

############################################################ PARTIE VERIFICATION CB ################################################################

banque = "lcl"

def GetInfosCB():
    # Connexion à la base de données
    db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
    print("Entrez votre numéro de carte bancaire : 4132438296994163")
    numeroCarte = input()
    # Vérification de l'existence de la carte bancaire
    if verifSiExisteCB(numeroCarte, db_connection) == False:
        print("Votre numéro de carte n'existe pas")
        return False
    else :
        return numeroCarte


def VerifInfosTransac(numeroCarte):
    # Connexion à la base de données
    db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
    
    # Vérification de la validité de la carte bancaire
    print("Entrez la date d'expiration de votre carte (MM/AA) : ")
    date_exp_utilisateur = input()

    infosCB = recupere_infos_cb(numeroCarte, db_connection)

    # Si la date d'expiration est incorrecte ou la carte est expirée
    if not verifDateExp(date_exp_utilisateur, infosCB[2], db_connection):
        print("La date d'expiration est incorrecte ou votre carte est expirée.")
        return False

    # Vérification du code PIN
    verifPin(numeroCarte)
    
    ### FONCTION VERIFPIN A MODIFIER -> REQUETE SQL POUR RECCUP PIN DE LA CB GRACE A SON NUMERO DE CARTE ET LE COMPARER 
    ### FONCTION VERIFPIN A MODIFIER : FAIT UNE BOUCLE WHILE POUR VERIFIER SI LE PIN EST BON OU PAS (3 TENTATIVES MAX) 
    
    tentatives = 0
    while tentatives < 3:
        pin = getpass.getpass("Veuillez entrer votre code PIN : ")
        pin = int(pin)
        
        if verifPin(infosCB, pin, db_connection):
            print("Vérification réussie.")
            return True
        else:
            tentatives += 1
            print(f"Tentative {tentatives} de 3.")
    print("Votre code PIN est incorrect. Carte bloquée.")
    bloqueCarte(numeroCarte, db_connection)
    return False

def verifSiExisteCB(numeroCarte, db_connection):
    # Vérifie si le numéro de carte existe dans la base de données
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM cartebancaire WHERE numeroCarte = %s", (numeroCarte,))
        (count,) = cursor.fetchone()
        return count > 0

def recupere_infos_cb(numeroCarte, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT numeroCarte, idCompteEmetteur, dateExpiration, validite, pin, cryptogramme FROM cartebancaire WHERE numeroCarte = %s", (numeroCarte,))
        return cursor.fetchone()

def verifPin(infos_cb, pin_saisi, db_connection):
    numeroCarte, idCompteEmetteur, dateExpiration, validite, pin_correct, cryptogramme = infos_cb

    if not validite:
        print("Carte bloquée")
        return False
    
    if pin_saisi != pin_correct:
        print("PIN invalide.")
        return False

    return True

def bloqueCarte(numeroCarte, db_connection):
    with db_connection.cursor() as cursor:
        update_query = "UPDATE cartebancaire SET validite = 0 WHERE numeroCarte = %s;"
        cursor.execute(update_query, (numeroCarte,))
        db_connection.commit()

def DebloqueCarte(numeroCarte, db_connection):
    with db_connection.cursor() as cursor:
        update_query = "UPDATE cartebancaire SET validite = 1 WHERE numeroCarte = %s;"
        cursor.execute(update_query, (numeroCarte,))
        db_connection.commit()


def verifDateExp(date_exp_utilisateur, date_exp_db, db_connection):
    # Formatage de la date d'expiration de la base de données en chaîne
    date_exp_db_str = date_exp_db.strftime('%m/%y')  # Format MM/AA

    # Comparaison des dates d'expiration
    if date_exp_utilisateur != date_exp_db_str:
        print("La date d'expiration entrée ne correspond pas à celle de la base de données.")
        return False

    # Vérification de la validité de la date par rapport au serveur NTP
    ntp_time = getTime()
    ntp_date = datetime.strptime(ntp_time, "%a %b %d %H:%M:%S %Y")
    
    # Date d'expiration à partir de la base de données
    exp_date = datetime.strptime('20' + date_exp_db.strftime('%y-%m-01'), '%Y-%m-%d')
    
    # Vérifie si la carte est expirée
    if exp_date < ntp_date:
        print("La carte est expirée.")
        return False
    
    return True

############################################################ PARTIE ENVOI AUTOR ################################################################

def EnvoiAutorisation(numeroCarte, montant, banque):
    # Connexion à la base de données
    db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
    print("Envoi de l'autorisation au serveur s'acquisition...")

    # Envoi de l'autorisation



def createFileLog(idComteEmetteur, idCompteAcquereur, montant):
    # Obtenir la date et l'heure actuelles
    dateHeureTransaction = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Créer un dictionnaire avec les informations
    nouvelleLigne = {
        "numero_compte_emetteur": idComteEmetteur,
        "numero_compte_acquereur": idCompteAcquereur,
        "montant_transaction": montant,
        "date_heure_transaction": dateHeureTransaction
    }

    cheminFichier = "logs/logsTPE/fichierLogsTPE" + str(banque.capitalize()) + ".json"

    # Vérifier si le fichier existe
    if not os.path.exists(cheminFichier):
        raise FileNotFoundError(f"Le fichier {cheminFichier} n'existe pas.")

    # Si le fichier existe, charger son contenu
    with open(cheminFichier, "r") as fichier:
        donneesExistantes = json.load(fichier)

    # Ajouter la nouvelle ligne
    donneesExistantes.append(nouvelleLigne)

    # Sauvegarder le fichier avec la nouvelle ligne
    with open(cheminFichier, "w") as fichier:
        json.dump(donneesExistantes, fichier, indent=2)