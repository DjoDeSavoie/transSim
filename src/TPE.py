# Fichier contenant les fonctions principales du TPE

from getpass4 import getpass
from Server_NTP import getTime

import getpass
import pymysql

# Connexion à la base de données
conn = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
cursor = conn.cursor()

def lectureCarte():
    # Lecture de la carte bancaire
    numeroCarte = input("Entrez votre numéro de carte bancaire : ")
    return numeroCarte

def verifCarteExiste(numeroCarte):
    # Vérifie si le numéro de carte existe dans la base de données
    cursor.execute("SELECT COUNT(*) FROM cartebancaire WHERE numeroCarte = %s", (numeroCarte,))
    (count,) = cursor.fetchone()
    return count > 0 #renvoie true si le numero de carte existe dans la base de données

def verifCarteValide(numeroCarte):
    # Vérifie si la carte est valide
    cursor.execute("SELECT validite FROM cartebancaireemmeteur WHERE numeroCarte = %s", (numeroCarte,))
    (validite,) = cursor.fetchone()
    return validite > 0
    

##### Il faut recuperer aussi les info de la CB du compte acquereur afin de pouvoir faire transiter l'argentdu compte emmeteur vers le compte acquerreur
#En gros, le tpe doit recup aussi le num de compte de l'acquereur (commercant) pour savoir vers qui envoyer l'argent
#-> peut être qu'il faut aujouter un champ idantifiant le tpe  dans la bdd pour pouvoir faire la requete sql pour recuperer les infos du du compte acquereur


# Fonction principale du TPE consistant à lire la carte bancaire et à effectuer toutes les vérifications
def processInfoCarte():

# Lecture de la carte bancaire (on simùule la lecture de la carte bancaire en demandant à l'utilisateur de rentrer le numéro de sa carte bancaire)
    numeroCarte = lectureCarte()
    
    
    # Verification de l'existance de la carte
    verifCarteExiste(numeroCarte)
    print("Votre numéro de carte n'existe pas")

    verifCarteValide(numeroCarte)
    # Vérification de la validité de la carte bancaire
    ###PAS BESOIN DE RENTRER LA DATE D'EXPIRATION, ON LA RECUPERE DIRECTEMENT DE LA BASE DE DONNEES AVEC UN REQUETE SQL
    ### FONCTION VERIFDATEEXP A MODIFIER -> REQUETE SQL POUR RECCUP DATE EXP DE LA CB GRACE A SON NUMERO DE CARTE
    
    # Vérification du code PIN
    verifPin(numeroCarte)
    
    ### FONCTION VERIFPIN A MODIFIER -> REQUETE SQL POUR RECCUP PIN DE LA CB GRACE A SON NUMERO DE CARTE ET LE COMPARER 
    ### FONCTION VERIFPIN A MODIFIER : FAIT UNE BOUCLE WHILE POUR VERIFIER SI LE PIN EST BON OU PAS (3 TENTATIVES MAX) 
    
    tentatives = 0
    while tentatives < 3:
        pin = getpass.getpass("Veuillez entrer votre code PIN : ")
        if verifPin(infosCB, pin, db_connection):
            print("Transaction réussie.")
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

#mettre dans fichier cb

# def luhn(CB):
#     # Vérification de la validité de la clé de luhn CB
#     somme = 0
#     for i in range(len(CB)):
#         chiffre = int(CB[i])
#         if i % 2 == 0:
#             chiffre *= 2
#             if chiffre > 9:
#                 chiffre -= 9
#         somme += chiffre
#     if somme % 10 != 0:
#         return False
#     return True



###ON PASS EN PARAM UNIQUEMENT LE NUMERO DE CARTE, LA FONCTION VERFIDATEEXP VA RECUPERER LA DATE D'EXPIRATION DE LA CB DANS LA BASE DE DONNEES ET FAIRE LA VERIFI ELLE MEME
def verifDateExp(date_exp_utilisateur, date_exp_db, db_connection):
    # Comparaison des dates d'expiration
    if date_exp_utilisateur != date_exp_db.split('-')[1] + '/' + date_exp_db.split('-')[0][2:]:
        print("La date d'expiration entrée ne correspond pas à celle de la base de données.")
        return False

    # Vérification de la validité de la date par rapport au serveur NTP
    ntp_time = getTime()
    ntp_date = ntp_time.strptime(ntp_time, "%a %b %d %H:%M:%S %Y")
    
    # Date d'expiration à partir de la base de données
    exp_date = ntp_time.strptime('20' + date_exp_db.split('-')[0][2:] + '-' + date_exp_db.split('-')[1] + '-01', '%Y-%m-%d')
    
    # Vérifie si la carte est expirée
    if exp_date < ntp_date:
        print("La carte est expirée.")
        return False
    
    return True

