import pymysql
import random

#on importe le serveur ntp pour utiliser sa fonction de récupération de la date + 2 ans
from Server_NTP import getDateWithTwoYears

conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
cursor = conn.cursor()

#creation d'un tableau associant les id d'une banque aux 3 premiers chiffres de sa carte
tabNumCarte = {"creditMutuel" : 132, "banquePostale" : 970, "lcl" : 972, "societeGenerale" : 973, "bnp" : 974, "caisseEpargne" : 978, "creditAgricole":131}


#création des cartes bancaires associées aux comptes acquéreurs, dès lors qu'un compte acquéreur est créé
#on crée une carte par acquéreur


#on génére un code pin aléatoire
def genererCodePin():
    #creation d'un entier aléatoire de 4 chiffres
    codePin = ""
    for i in range(4):
        codePin += str(random.randint(0,9))
    return codePin


#on génère un code de sécurité aléatoire
def genererCryptogramme():
    #creation d'un entier aléatoire de 4 chiffres
    crypto = ""
    for i in range(4):
        crypto += str(random.randint(0,9))
    return crypto

#pour le choix du réseau émetteur de la carte, nous avons opté polur l'option der l'aléatoire : 
#on choisit aléatoirement un réseau émetteur parmi les 3 proposés pour faire plus simple
def choixReseauEmetteurCarte():
    #choix aléatoire d'un réseau émetteur (3 pour américan express, 4 pour visa et 5 pour mastercard)
    valeur1 = random.randint(3,5)
    return valeur1 #la 1ère valeur du numéro de carte
    


#on génère un numéro de carte 
def genereNumeroCarteEnFonctionBanque(idBanque):
    
    #on récupère le numéro de la banque
    cursor.execute("SELECT nomBanque FROM banque WHERE idBanque = %s", (idBanque))
    nomBanque = cursor.fetchone()[0]
    #on génère un numéro de carte de 16 chiffres
    valeur234 = tabNumCarte[str(nomBanque)]
    return valeur234 #les 2, 3, 4èmes valeur du numéro de carte

#fonction générant la clé de luhn à parti des valeurs précédentes
def cleDeLuhn(numero1, numero234, numero5a15):
    #on concatène les valeurs
    numero = str(numero1) + str(numero234) + str(numero5a15)
    #on calcule la clé de luhn
    somme = 0
    for i in range(15):
        if i%2 == 0:
            somme += int(numero[i])
        else:
            if int(numero[i])*2 > 9:
                somme += int(numero[i])*2 - 9
            else:
                somme += int(numero[i])*2
    cle = 10 - somme%10
    return cle #la 16ème valeur du numéro de carte    
    



def creationCarte(idCompteEmetteur, idBanque):
    numero1 = choixReseauEmetteurCarte()
    numero234 = genereNumeroCarteEnFonctionBanque(idBanque)
    numero5a15 = idCompteEmetteur
    numero16 = cleDeLuhn(numero1, numero234, numero5a15)
    
    #on concatène les valeurs
    numeroCarte = str(numero1) + str(numero234) + str(numero5a15) + str(numero16)    
    
    dateValidite = getDateWithTwoYears()
    pin = genererCodePin()
    crypto = genererCryptogramme()
    
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n")
    
    
    #on fait la requete sql permettant d'insérer les valeurs dans la base de données
    cursor.execute("INSERT INTO cartebancaire (numeroCarte, idCompteEmetteur, dateExpiration, validite, pin, cryptogramme) VALUES (%s, %s, %s, %s, %s, %s)",
                   (numeroCarte, idCompteEmetteur, dateValidite, 1, pin, crypto))
    
    conn.commit()
    conn.close()
    


#teste de la fonction de création de carte avec un id de compte et un id de banque
#creationCarte("12345678910", "1")
