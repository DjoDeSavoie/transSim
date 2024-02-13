from utilz import ecrireFichierJson

import pymysql


#Fichier contenant les fonctions du serveur réseau interbancaire

#Fonction pour le routage de la transaction
#on récupère la banque du compte émetteur
def routageTransaction(demande):
    #on récupère l'id de la banque du compte émetteur
    idBanqueEmetteur = demande["idBanqueEmetteur"][0] if isinstance(demande["idBanqueEmetteur"], list) else demande["idBanqueEmetteur"]
    
    #on récupère le nom de la banque du compte émetteur
    nomBanqueEmetteur = recupererNomBanque(idBanqueEmetteur)
    
    #on inscrit la demande dans le fichier de logs de la banque emetteur
    ecrireFichierJson("logs/logsBanqueEmetteur/" + nomBanqueEmetteur + ".json", demande)
    
    

def recupererNomBanque(idBanque):
    
    # Connexion à la base de données 
    conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
    cursor = conn.cursor()
    
    # Exécutez la requête SQL pour récupérer le nom de la banque
    cursor.execute("SELECT nomBanque FROM banque WHERE idBanque = %s", (idBanque))
    nomBanque = cursor.fetchone()[0]
    return nomBanque
    
    
