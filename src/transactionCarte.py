import pymysql

# Connexion à la base de données
conn = pymysql.connect(user='root', host='34.163.159.223', database='transsim')
cursor = conn.cursor()

# Fonction modifiant le solde des deux comptes concernés par la transaction (compte acquéreur et compte émetteur) en fonction du montant de celle-ci
def modifSoldeComptes(montant, idCompteEmetteur, idCompteAcquereur):
    # Exécutez la requête SQL pour récupérer le solde du compte émetteur
    cursor.execute("SELECT soldeCompteEmetteur FROM comptebancaireemetteur WHERE idCompteEmetteur = %s", (idCompteEmetteur,))
    soldeCompteEmetteur = cursor.fetchone()[0]
    print(soldeCompteEmetteur)

    # Exécutez la requête SQL pour récupérer le solde du compte acquéreur
    cursor.execute("SELECT soldeCompteAcquereur FROM comptebancaireacquereur WHERE idCompteAcquereur = %s", (idCompteAcquereur,))
    soldeCompteAcquereur = cursor.fetchone()[0]

    # Exécutez la requête SQL pour modifier le solde du compte émetteur
    cursor.execute("UPDATE comptebancaireemetteur SET soldeCompteEmetteur = %s WHERE idCompteEmetteur = %s", (soldeCompteEmetteur - montant, idCompteEmetteur))
    # Exécutez la requête SQL pour modifier le solde du compte acquéreur
    cursor.execute("UPDATE comptebancaireacquereur SET soldeCompteAcquereur = %s WHERE idCompteAcquereur = %s", (soldeCompteAcquereur + montant, idCompteAcquereur))

    # Enregistrez les modifications
    conn.commit()
    conn.close()




# TEST
# modifSoldeComptes(100, 14387751794, 1)
