import pymysql

conn = pymysql.connect(user ='root', password='', host='localhost', database='transsimclient')
cursor = conn.cursor()


# queryCreateCarte = "INSERT INTO cartebancaire (numeroCarte, idCompteEmetteur, dateExpiration, validite, pin, cryptogramme) VALUE (%s, %s, %s, %s, %s, %s)"
# r = cursor.execute(queryCreateCarte, ('1234567891234567', '1', '2020-12-31', '1', '1234', '123'))

