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
    cursor.execute("SELECT idCompteAcquereur FROM comptebancaireacquereur WHERE idCompteAcquereur = %s", (idCompte))
    idCompteExiste = cursor.fetchone()
    
    #si l'id existe déjà ou qu'il est de longuer différente de 11, on en génère un nouveau

    while idCompteExiste != None or len(idCompte) != 11:
        idCompte = random11number()
        cursor.execute("SELECT idCompteAcquereur FROM comptebancaireacquereur WHERE idCompteAcquereur = %s", (idCompte))
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
    idCompteAcquereur = creationIdCompteBancaire()
    solde = 0
    
    
    # Exécutez la requête SQL pour créer un compte
    cursor.execute("INSERT INTO comptebancaireacquereur (idCompteAcquereur, idBanqueEmetteur, nom, prenom, soldeCompteEmetteur) VALUES (%s, %s, %s, %s, %s)", (idCompteAcquereur, idBanque, nom, prenom, solde))
    conn.commit()
    print("Compte créé avec succès! ... \n Création de la carte associée au compte ... \n")
    
    
    #CREATION DE LA CARTE ASSOCIEE AU COMPTE
    creationTPE(idCompteAcquereur, idBanque)
    
    
    
    
###############################################################################################
################################# CREATION D'UN TPE ASSOCIE ###################################
###############################################################################################




#creation d'un tableau associant les id d'une banque aux 3 premiers chiffres de sa carte
tabNumCarte = {"creditMutuel" : 132, "banquePostale" : 970, "lcl" : 972, "societeGenerale" : 973, "bnp" : 974, "caisseEpargne" : 978, "creditAgricole":131}


#création du TPE associé au compte acquéreur, dès lors qu'un compte acquéreur est créé
#on crée un TPE par acquéreur





#on génère un numéro de carte 
def genereIdTpeEnFonctionBanque(idBanque):
    
    #on récupère le numéro de la banque
    cursor.execute("SELECT nomBanque FROM banque WHERE idBanque = %s", (idBanque))
    nomBanque = cursor.fetchone()[0]
    #on génère un numéro de carte de 16 chiffres
    valeur234 = tabNumCarte[str(nomBanque)]
    return valeur234 #les 2, 3, 4èmes valeur du numéro de carte
    



def creationTPE(idCompteAcquereur, idBanque):
    numero234 = genereIdTpeEnFonctionBanque(idBanque)
    numero5a15 = idCompteAcquereur
    
    #on concatène les valeurs pour créer un unique id de tpe
    idTPE = str(numero234) + str(numero5a15)   
      
    
    #on fait la requete sql permettant d'insérer les valeurs dans la base de données
    cursor.execute("INSERT INTO TPE (idTPE, idCompteAcquereur) VALUES (%s, %s)",
                   (idTPE, idCompteAcquereur))
    
    conn.commit()
    conn.close()
    
    print("Carte créée avec succès! \n")
    
    
    


# creation d'un compte acquéreur
creerCompte()
