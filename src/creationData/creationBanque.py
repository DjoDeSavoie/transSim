#Fichier permettant la création d'une banque (nom) et de son fichier de logs (transactionsNomBanque.json)
import pymysql
from Server_NTP import getDateWithTwoYears
import os
import json

def creer_banque(nomBanque):
    try:
        # Connexion à la base de données
        conn = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
        cursor = conn.cursor()

        # Vérifier si la banque existe déjà
        cursor.execute("SELECT COUNT(*) FROM banque WHERE nomBanque = %s", (nomBanque,))
        existDeja = cursor.fetchone()[0] > 0

        if existDeja:
            print("La banque existe déjà.")
        else:
            # Ajouter la nouvelle banque à la base de données
            cursor.execute("INSERT INTO banque (nomBanque) VALUES (%s)", (nomBanque,))
            print("La banque a été ajoutée avec succès.")

            # Valider la transaction
            conn.commit()

    except pymysql.Error as e:
        print(f"Erreur lors de l'interaction avec la base de données : {e}")
    finally:
        # Fermer la connexion
        if conn:
            conn.close()

# Demander à l'utilisateur le nom de la banque à créer
nomBanque = input("Entrez le nom de la banque que vous souhaitez créer : ")

# Appeler la fonction pour créer la banque
creer_banque(nomBanque)


###############################################################################################
############################## CREATION D'UN FICHIER DE LOGS ##################################
###############################################################################################


# Ouvrir un fichier en mode écriture (crée un fichier s'il n'existe pas)
with open("logs/fichierLogsTPE" + str(nomBanque.capitalize()) + ".json", "w") as fichier:
    # Écrire dans le fichier
    fichier.write("Fichier de logs de la banque " + str(nomBanque.capitalize()) + ".\n\n")

# Chaque banque possède un fichier de logs qui, lorsqu'une transaction est effectuée, enregistre les informations suivantes :
# - numéro de compte de l'émetteur
# - numéro de compte de l'acquéreur
# - montant de la transaction
# - date et heure de la transaction


# def createFileLog(idComteEmetteur, idCompteAcquereur, montant):
#     # Obtenir la date et l'heure actuelles
#     dateHeureTransaction = getDateWithTwoYears()

#     # Créer un dictionnaire avec les informations
#     nouvelleLigne = {
#         "numero_compte_emetteur": idComteEmetteur,
#         "numero_compte_acquereur": idCompteAcquereur,
#         "montant_transaction": montant,
#         "date_heure_transaction": dateHeureTransaction
#     }

#     cheminFichier = "transactions.json"

#     # Si le fichier existe, charger son contenu
#     if os.path.exists(cheminFichier):
#         with open(cheminFichier, "r") as fichier:
#             donneesExistantes = json.load(fichier)
#     else:
#         donneesExistantes = []

#     # Ajouter la nouvelle ligne
#     donneesExistantes.append(nouvelleLigne)

#     # Sauvegarder le fichier avec la nouvelle ligne
#     with open(cheminFichier, "w") as fichier:
#         json.dump(donneesExistantes, fichier, indent=2)

# # Exemple d'utilisation
# creer_ou_ajouter_ligne_fichier_json("123456789", "987654321", 100.50)




# # Ouvrir un fichier en mode écriture (crée un fichier s'il n'existe pas)
# with open("mon_fichier.txt", "w") as fichier:
#     # Écrire dans le fichier
#     fichier.write("Contenu du fichier.\nLigne suivante.")