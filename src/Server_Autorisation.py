# Server_Autorisation.py

import json
import time
import pymysql

from Server_NTP import getDateWithTwoYears

chemin_fichier_json = "logs/logsTPE/logsTPE.json"

#connexion à la base de données
conn = pymysql.connect(user ='root', host='34.163.159.223', database='transsim')
cursor = conn.cursor()

def lireFichierJson(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)
    
def checkInfoTransaction(demande):
    #vérification de la validité de la demande : solde emetteur suffisant, validité de la carte, etc
    #on vérifie que le solde de l'emetteur est suffisant
    cursor.execute("SELECT solde FROM compte WHERE idCompte = %s", (demande['idCompteEmetteur']))
    solde = cursor.fetchone()[0]
    if solde < demande['montant']:
        print("Solde insuffisant pour la transaction.")
        return False
    #on vérifie la validité de la carte
    cursor.execute("SELECT dateExpiration FROM carte WHERE idCarte = %s", (demande['idCarteEmetteur']))
    dateExpiration = cursor.fetchone()[0]
    if dateExpiration < getDateWithTwoYears():
        print("Carte expirée.")
        return False
    
def saveInfoTransacDansBase(demande):
    #sauvegarde des informations de la transaction
    cursor.execute("INSERT INTO transaction (idCompteEmetteur, idCompteAcquereur, montant, idCarteEmetteur, idCarteRecepteur, dateTransaction) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (demande['idCompteEmetteur'], demande['idCompteRecepteur'], demande['montant'], demande['idCarteEmetteur'], demande['idCarteRecepteur'], demande['dateTransaction']))
    
    


def genererAutorisation(idDemande):
    #on récupère les données du fichier json
    donnees = lireFichierJson(chemin_fichier_json)
    
    #tri des données : on récupère la donnée de la demande ou idLog vaut idDemande
    demande = [demande for demande in donnees if demande['idLog'] == idDemande][0]
    print("Données de la demande : ", demande)
    if checkInfoTransaction(demande):
        #sauvegarde des informations de la transaction
        saveInfoTransacDansBase(demande)
    print("Génération de l'autorisation pour la demande : ", idDemande)
    
