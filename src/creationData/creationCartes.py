import pymysql

conn = pymysql.connect(user ='root', host='34.163.159.223', database='bdd_porteur')
cursor = conn.cursor()


#création des cartes bancaires associées aux comptes acquéreurs

#savoir si : on crée une carte par acquéreur ou plusieurs, si on le fait automatiquement après la création du compte en banque ou si on le fait manuellement
