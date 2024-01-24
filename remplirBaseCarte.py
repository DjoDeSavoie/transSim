import pymysql

conn = pymysql.connect(user ='root', password='', host='localhost', database='transsimclient')
cursor = conn.cursor()

queryCreateBanque = "INSERT INTO banque (idBanque, nomBanque) VALUE (%s, %s)"    
rBanque = cursor.execute(queryCreateBanque, ('0', 'Credit Agricole'))

# Validez la transaction en effectuant un commit
conn.commit()

query = "SELECT * FROM banque"
r = cursor.execute(query)
print(cursor.fetchall())


# queryCreateCompteAcquereur = "INSERT INTO comptebancaireacquereur (idCompteAcquereur, idBanqueAcquereur, numeroCompte, nom, prenom, soldeCompteAcquereur) VALUE (%s, %s, %s, %s, %s, %s)"
# rCompteAcquereur = cursor.execute(queryCreateCompteAcquereur, ('0', '0', '123456789', 'Dupont', 'Jean', '1000'))

# queryCreateCarte = "INSERT INTO cartebancaire (numeroCarte, idCompteEmetteur, dateExpiration, validite, pin, cryptogramme) VALUE (%s, %s, %s, %s, %s, %s)"
# r = cursor.execute(queryCreateCarte, ('1234567891234567', '1', '2020-12-31', '1', '1234', '123'))

