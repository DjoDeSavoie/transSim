#Fichier permettant la création des comptes acquéreurs

import pymysql
import random
from datetime import datetime


#importe le serveur NTP pour la fonction de récupération de la date actuelle + 2 ans 
from Server_NTP import getDateWithTwoYears

#Connexion à la base de données
conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
cursor = conn.cursor()


###############################################################################################
################################### CREATION D'UN COMPTE ######################################
###############################################################################################


# Fonction pour récupérer la liste des noms de banques depuis la base de données
def recupererNomsBanques():

    # Exécutez la requête SQL pour récupérer les noms de banques
    cursor.execute("SELECT nomBanque FROM banque")
    nomsBanques = [row[0] for row in cursor.fetchall()]

    return nomsBanques



#fonction pour permettre à l'utilisateur de choisir une banque parmi la liste des banques
def choisirBanque(choixBanques):
    # Affichage des choix de banques
    print("Choisissez une banque parmi les options suivantes :")
    for i, banque in enumerate(choixBanques, 1):
        print("{}. {}".format(i, banque))

    # Saisie du choix de l'utilisateur
    choix = int(input("Entrez le numéro de la banque choisie : "))
    # Vérification de la saisie
    while choix < 1 or choix > len(choixBanques):
        choix = int(input("Entrez le numéro de la banque choisie : "))
    print("Vous avez choisi la banque {}.".format(choixBanques[choix - 1]))
    return choixBanques[choix - 1]



#Fonction pour récupérer l'id d'une banque depuis la base de données
def recupererIdBanqueChoisie(choixBanque):

    # Exécutez la requête SQL pour récupérer l'id de la banque
    cursor.execute("SELECT idBanque FROM banque WHERE nomBanque = %s", (choixBanque))
    idBanque = cursor.fetchone()[0]

    return idBanque

def random11number():
    num = ""
    for i in range(11):
        num += str(random.randint(0,9))
    return num

def creationIdCompteBancaire():
    #choisit 11 chiffre aléatoire
    idCompte = random11number()
    
    #on vérifie que l'id n'existe pas déjà 
    cursor.execute("SELECT idCompteEmetteur FROM comptebancaireemetteur WHERE idCompteEmetteur = %s", (idCompte))
    idCompteExiste = cursor.fetchone()
    
    #si l'id existe déjà ou qu'il est de longuer différente de 11, on en génère un nouveau

    while idCompteExiste != None or len(idCompte) != 11:
        idCompte = random11number()
        cursor.execute("SELECT idCompteEmetteur FROM comptebancaireemetteur WHERE idCompteEmetteur = %s", (idCompte))
        idCompteExiste = cursor.fetchone()
        
    return idCompte

numCompte = creationIdCompteBancaire()

#affichage du numéro de compte
print("Le numéro de compte est : ", numCompte)



# Fonction pour créer un compte en banque
def creerCompte():
    nom = input("Entrez votre nom : ")
    prenom = input("Entrez votre prénom : ")

    # Liste des choix de banques
    nomsBanques = recupererNomsBanques()
    choixBanque = choisirBanque(nomsBanques)
    idBanque = recupererIdBanqueChoisie(choixBanque)
    idCompteEmetteur = creationIdCompteBancaire()
    solde = 1500
    
    
    # Exécutez la requête SQL pour créer un compte
    cursor.execute("INSERT INTO comptebancaireemetteur (idCompteEmetteur, idBanqueEmetteur, nom, prenom, soldeCompteEmetteur) VALUES (%s, %s, %s, %s, %s)", (idCompteEmetteur, idBanque, nom, prenom, solde))
    conn.commit()
    print("Compte créé avec succès! ... \n")
    
    
    #CREATION DE LA CARTE ASSOCIEE AU COMPTE
    creationCarte(idCompteEmetteur, idBanque)
    
    
    
    
###############################################################################################
################################### CREATION D'UNE CARTE ######################################
###############################################################################################




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
    for i in range(3):
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
    print("Création de la carte associée au compte ... \n")
    
    numero1 = choixReseauEmetteurCarte()
    numero234 = genereNumeroCarteEnFonctionBanque(idBanque)
    numero5a15 = idCompteEmetteur
    numero16 = cleDeLuhn(numero1, numero234, numero5a15)
    
    #on concatène les valeurs
    numeroCarte = str(numero1) + str(numero234) + str(numero5a15) + str(numero16)
    
    dateValidite = getDateWithTwoYears()
    pin = genererCodePin()
    crypto = genererCryptogramme()    
    
    #on fait la requete sql permettant d'insérer les valeurs dans la base de données
    cursor.execute("INSERT INTO cartebancaire (numeroCarte, idCompteEmetteur, dateExpiration, validite, pin, cryptogramme) VALUES (%s, %s, %s, %s, %s, %s)",
                   (numeroCarte, idCompteEmetteur, dateValidite, 1, pin, crypto))
    
    conn.commit()
    conn.close()
    
    print("Carte créée avec succès! \n")
    
    
    


# creation d'un compte acquéreur
creerCompte()
