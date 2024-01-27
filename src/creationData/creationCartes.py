import pymysql

conn = pymysql.connect(user ='root', password='', host='localhost', database='transsimclient')
cursor = conn.cursor()


#création des cartes bancaires associées aux comptes acquéreurs

#savoir si : on crée une carte par acquéreur ou plusieurs, si on le fait automatiquement après la création du compte en banque ou si on le fait manuellement
