############################################    Utilz    ############################################
import json
import pymysql

from colorama import init, Fore
import hashlib
import pymysql
import os


# Initialiser colorama
init(autoreset=True)

######### Fonction de hachage SHA-256 #########
def hash_sha256(data):
    # Créer un objet hash SHA-256
    sha256_hash = hashlib.sha256()

    # Mettre à jour l'objet hash avec les données à hasher (doit être des bytes)
    sha256_hash.update(data.encode('utf-8'))

    # Obtenir la représentation hexadécimale du hash
    hashed_data = sha256_hash.hexdigest()

    return hashed_data


# Fonction pour vérifier le solde
def verifierSolde():
    conn = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
    type_compte = input(f"{Fore.YELLOW}Entrez le type de votre compte ('emetteur' : 1 ou 'acquereur': 2) :")
    id_compte = input(f"{Fore.YELLOW}Entrez l'ID de votre compte : ")
    solde = getSolde(conn, id_compte, type_compte)
    if solde is not None:
        print(f"{Fore.CYAN}Le solde de votre compte est de {solde}€.")

######### Connexion à la base de données #########

conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
cursor = conn.cursor()


def getSolde(db_connection, id_compte, type_compte):
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


######### Fonctions pour lire et écrire des fichiers JSON #########

# Fonction pour lire un fichier JSON
def lireFichierJson(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)

# Fonction pour écrire dans un fichier JSON en conservant les valeurs existantes
def ecrireFichierJson(chemin_fichier, contenu):
    with open(chemin_fichier, 'w') as f:
        json.dump(contenu, f, indent=4)

def creeFichierLogs(nomFichierLogs):
    # Vérifier si le fichier de logs existe déjà pour cette banque
    if not os.path.exists(nomFichierLogs):
        # S'il n'existe pas, initialisez une liste vide
        donneesExistantes = []
        return donneesExistantes
    else:
        # S'il existe, chargez son contenu
        with open(nomFichierLogs, 'r', encoding='utf-8') as fichier:
            donneesExistantes = json.load(fichier)
            return donneesExistantes
        
def recupererNomBanque(idBanque):
    
    # Connexion à la base de données 
    conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
    cursor = conn.cursor()
    
    # Exécutez la requête SQL pour récupérer le nom de la banque
    cursor.execute("SELECT nomBanque FROM banque WHERE idBanque = %s", (idBanque))
    nomBanque = cursor.fetchone()[0]
    
    # Fermer la connexion à la base de données
    conn.close()
    
    return nomBanque

def recupererIdBanque(nomBanque):
    
    # Connexion à la base de données 
    conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
    cursor = conn.cursor()

    # Exécutez la requête SQL pour récupérer l'id de la banque
    cursor.execute("SELECT idBanque FROM banque WHERE nomBanque = %s", (nomBanque))
    idBanque = cursor.fetchone()[0]

    # Fermer la connexion à la base de données
    conn.close()
    return idBanque