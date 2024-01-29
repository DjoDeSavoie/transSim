#Fichier permettant la création des comptes acquéreurs

import pymysql
import random

#on importe la focntion de création de carte
import creationCartes

#Connexion à la base de données
conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
cursor = conn.cursor()

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
    
    
    # Exécutez la requête SQL pour créer un compte
    cursor.execute("INSERT INTO comptebancaireemetteur (idCompteEmetteur, idBanqueEmetteur, nom, prenom) VALUES (%s, %s, %s, %s)", (idCompteEmetteur, idBanque, nom, prenom))
    conn.commit()
    conn.close()
    print("Compte créé avec succès! ... \n Création de la carte associée au compte ... \n")
    
    creationCartes.creationCarte(idCompteEmetteur, idBanque)
    


# creation d'un compte acquéreur
creerCompte()
