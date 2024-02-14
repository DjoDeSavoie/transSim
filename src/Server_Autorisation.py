# Server_Autorisation.py
import json
import time
import pymysql

from pymysql import MySQLError
from Server_NTP import getDateWithTwoYears
from colorama import init, Fore
from utilz import lireFichierJson

# Initialiser colorama
init(autoreset=True)

db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')

def recupereDonneesLog(idLog, fichier):
    try:
        with open(fichier, 'r') as file:
            logs = json.load(file)
            transaction_log = next((item for item in logs if item["idLog"] == idLog), None)
            if not transaction_log:
                raise ValueError(f"Aucun log trouvé avec l'idLog {idLog}.")
            return transaction_log
    except (IOError, json.JSONDecodeError, ValueError) as e:
        print(f"Erreur lors de la lecture du fichier de logs: {e}")
        return False

# fonction qui génère une autorisation
def traiterTransaction(idLog, fichier): 
    # Étape 1: Récupérer les données de la transaction
    transaction_log = recupereDonneesLog(idLog, fichier)
    
    # Étape 2 et 3: Vérification des soldes et transfert des montants
    try:
        with db_connection.cursor() as cursor:
            # Vérifier le solde du compte émetteur
            print(f"Vérification du solde du compte émetteur {transaction_log['numero_compte_emetteur']}...")
            cursor.execute("SELECT soldeCompteEmetteur FROM comptebancaireemetteur WHERE idCompteEmetteur = %s",
                           (transaction_log["numero_compte_emetteur"],))
            solde_emetteur = cursor.fetchone()
            if solde_emetteur is None:
                print("Compte émetteur non trouvé.")
                return False
            if solde_emetteur[0] < transaction_log["montant_transaction"]:
                print("Solde insuffisant pour la transaction.")
                return False

            # Début de la transaction
            db_connection.begin()

            # Débiter le montant du compte émetteur
            cursor.execute("UPDATE comptebancaireemetteur SET soldeCompteEmetteur = soldeCompteEmetteur - %s WHERE idCompteEmetteur = %s",
                           (transaction_log["montant_transaction"], transaction_log["numero_compte_emetteur"]))

            # Créditer le montant au compte acquéreur
            cursor.execute("UPDATE comptebancaireacquereur SET soldeCompteAcquereur = soldeCompteAcquereur + %s WHERE idCompteAcquereur = %s",
                           (transaction_log["montant_transaction"], transaction_log["numero_compte_acquereur"]))

            # Valider la transaction
            db_connection.commit()
            print("La transaction a été traitée avec succès.")
            genereAutorisation(idLog, fichier)
            return True
    except MySQLError as e:
        # En cas d'erreur, annuler la transaction
        db_connection.rollback()
        print(f"Erreur lors de la transaction dans la base de données: {e}")
        return False

# Genere une autorisation
def genereAutorisation(idLog, fichier):
    transaction_log = recupereDonneesLog(idLog, fichier)
    
    # Récupérer les données de la transaction
    idBanqueEmetteur = transaction_log["numero_compte_emetteur"]
    dateAutorisation = transaction_log["date_heure_transaction"]
    montant = transaction_log["montant_transaction"]

    try:
        with db_connection.cursor() as cursor:
            # Création de la requête SQL d'insertion
            sql = """
            INSERT INTO autorisationtransaction (idBanqueEmetteur, dateAutorisation, montantAutorisation)
            VALUES (%s, %s, %s)
            """
            # Exécution de la requête SQL
            cursor.execute(sql, (idBanqueEmetteur, dateAutorisation, montant))
            # Validation des modifications
            db_connection.commit()
            print(f"Autorisation pour la transaction {idLog} insérée avec succès.")
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'insertion dans la base de données: {e}")