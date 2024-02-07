#Fichier contenant les fonctions du serveur d'autoisation

import json
import pymysql
from pymysql import MySQLError

# fonction qui génère une autorisation
def traiterTransaction(idLog):
    db_connection = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
    # Étape 1: Récupérer les informations du log
    try:
        with open("logs/logsTPE/logsTPE.json", 'r') as file:
            logs = json.load(file)
            transaction_log = next((item for item in logs if item["idLog"] == idLog), None)
            if not transaction_log:
                raise ValueError(f"Aucun log trouvé avec l'idLog {idLog}.")
    except (IOError, json.JSONDecodeError, ValueError) as e:
        print(f"Erreur lors de la lecture du fichier de logs: {e}")
        return False
    
    # Étape 2 et 3: Vérification des soldes et transfert des montants
    try:
        with db_connection.cursor() as cursor:
            # Vérifier le solde du compte émetteur
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
            return True
    except MySQLError as e:
        # En cas d'erreur, annuler la transaction
        db_connection.rollback()
        print(f"Erreur lors de la transaction dans la base de données: {e}")
        return False