from utilz import ecrireFichierJson
from utilz import lireFichierJson

import pymysql


#Fichier contenant les fonctions du serveur réseau interbancaire

#Fonction pour le routage de la transaction
#on récupère la banque du compte émetteur
def routageTransaction(demande):
    
    print ("Routage de la transaction par le serveur interbancaire...")
    
    if demande["isTraite"]:
        print("La demande a déjà été traitée.")
        return
    
    else : 
        #on récupère l'id de la banque du compte émetteur
        idBanqueEmetteur = demande["idBanqueEmetteur"][0] if isinstance(demande["idBanqueEmetteur"], list) else demande["idBanqueEmetteur"]
        
        #on défini la demande en tant que traitée
        demande["isTraite"] = True
        
        #on récupère le nom de la banque du compte émetteur
        nomBanqueEmetteur = recupererNomBanque(idBanqueEmetteur)
        
        #lecture du fichier de logs de la banque emetteur
        logs = lireFichierJson("logs/logsTPE/logsTPE_" + nomBanqueEmetteur + ".json")
        
        #concaténation des logs lus et de la demande à traiter
        logs.append(demande)
        
        #on inscrit les nouveau contenu du fichier dans le fichier de logs
        ecrireFichierJson("logs/logsTPE/logsTPE_" + nomBanqueEmetteur + ".json", logs)
    
    

def recupererNomBanque(idBanque):
    
    # Connexion à la base de données 
    conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
    cursor = conn.cursor()
    
    # Exécutez la requête SQL pour récupérer le nom de la banque
    cursor.execute("SELECT nomBanque FROM banque WHERE idBanque = %s", (idBanque))
    nomBanque = cursor.fetchone()[0]
    
    # Fermer la connexion à la base de données
    conn.close()
    
    return nomBanque
    
    
    
