import pymysql

conn = pymysql.connect(user ='i22024395', password='Kr6zFGkMQpvFH07', host='aris-issad-etu.pedaweb.univ-amu.fr', database='i22024395')
cursor = conn.cursor()


#création des cartes bancaires associées aux comptes acquéreurs

#savoir si : on crée une carte par acquéreur ou plusieurs, si on le fait automatiquement après la création du compte en banque ou si on le fait manuellement
