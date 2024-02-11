#Fichier permettant la création d'une banque (nom) et de son fichier de logs (transactionsNomBanque.json)
import pymysql
from Server_NTP import getDateWithTwoYears


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


def creationBanque():
    # Demander à l'utilisateur le nom de la banque à créer
    nomBanque = input("Entrez le nom de la banque que vous souhaitez créer : ")

    # Appeler la fonction pour créer la banque
    creer_banque(nomBanque)


###############################################################################################
############################## CREATION D'UN FICHIER DE LOGS ##################################
###############################################################################################


    # Ouvrir un fichier en mode écriture (crée un fichier s'il n'existe pas)
    with open("logs/logsTPE/fichierLogsTPE" + str(nomBanque.capitalize()) + ".json", "w") as fichier:
        # Écrire dans le fichier
        fichier.write("Fichier de logs de la banque " + str(nomBanque.capitalize()) + ".\n\n")
