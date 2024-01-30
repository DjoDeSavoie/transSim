#Fichier qui contient le code principal du programme, c'est-à-dire le menu principal
# pour choisir si on veut effectuer une transaction, verifier son solde, se connecter 
# ou quitter le programme 

from TPE import *

# Appel de la fonction pour récupérer les informations
numeroCarte = GetInfosCB()

if numeroCarte != False:
    VerifInfosTransac(numeroCarte)

createFileLog(numeroCarte, 1, 300)