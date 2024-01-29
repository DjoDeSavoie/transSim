#Fichier permettant la création des comptes acquéreurs

import pymysql

#Connexion à la base de données
conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsimclient')
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



# Fonction pour créer un compte en banque
def creerCompte():
    nom = input("Entrez votre nom : ")
    prenom = input("Entrez votre prénom : ")

    # Liste des choix de banques
    nomsBanques = recupererNomsBanques()
    choixBanque = choisirBanque(nomsBanques)
    idBanque = recupererIdBanqueChoisie(choixBanque)
    
    
    # Exécutez la requête SQL pour créer un compte
    cursor.execute("INSERT INTO comptebancaireemetteur (nom, prenom, idBanqueEmetteur) VALUES (%s, %s, %s)", (nom, prenom, idBanque))
    conn.commit()
    conn.close()
    print("Compte créé avec succès.")
    


#creation d'un compte acquéreur
creerCompte()
