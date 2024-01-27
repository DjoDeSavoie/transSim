# Fichier contenant les fonctions principales du TPE

from Server_NTP import getTime

# fonction verifInfosCB
def verifInfosCB(CB):
    # Vérification de la longueur de la CB
    if len(CB) != 16:
        return False

    # Vérification du type de la CB
    if not CB.isdigit():
        return False

    # Vérification de la validité de la clé de luhn CB
    if not luhn(CB):
        return False
    
    # Vérification de la validité de la date d'expiration
    if not verifDateExp(CB):
        return False

    return True


#mettre dans fichier cb

def luhn(CB):
    # Vérification de la validité de la clé de luhn CB
    somme = 0
    for i in range(len(CB)):
        chiffre = int(CB[i])
        if i % 2 == 0:
            chiffre *= 2
            if chiffre > 9:
                chiffre -= 9
        somme += chiffre
    if somme % 10 != 0:
        return False
    return True

def verifDateExp(CB):
    # Vérification de la validité de la date d'expiration
    # voir comment extraire les infos de la CB 
    #mois = convertir en nbr
    #annee = 
    
    if mois < 1 or mois > 12 :
        return False

    # Obtenez l'heure actuelle avec le serveur NTP
    heure_actuelle = getTime()
    mois_actuel = int(heure_actuelle[4:7]) #convertir en nbr
    annee_actuelle = int(heure_actuelle[-4:])
    # Comparaison de la date d'expiration avec la date actuelle
    if annee < annee_actuelle or (annee == annee_actuelle and mois < mois_actuel):
        return False

    return True

