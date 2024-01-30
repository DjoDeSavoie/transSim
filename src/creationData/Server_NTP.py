#création d'un serveur NTP avec le module ntplib
#le serveur NTP est un serveur de temps qui permet de synchroniser les horloges des ordinateurs connectés à un réseau informatique

from time import ctime
import ntplib
from datetime import datetime, timedelta


# function retournant le temps du serveur NTP
def getTime():
    ntp = ntplib.NTPClient()
    response = ntp.request('europe.pool.ntp.org', version=3)
    return ctime(response.tx_time)
    

# Fonction retournant la date du serveur NTP
def getDate():
    ntp = ntplib.NTPClient()
    response = ntp.request('europe.pool.ntp.org', version=3)
    time_str = ctime(response.tx_time)
    
    # Convertir la chaîne de date en objet datetime
    datetime_obj = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
    
    # Formater la date
    date_formatted = datetime_obj.strftime("%Y-%m-%d")
    
    return date_formatted



# Fonction retournant la date avec 2 ans ajoutés
def getDateWithTwoYears():
    ntp = ntplib.NTPClient()
    response = ntp.request('europe.pool.ntp.org', version=3)
    time_str = ctime(response.tx_time)
    
    # Convertir la chaîne de date en objet datetime
    datetime_obj = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
    
    # Ajouter 2 ans à la date
    date_with_two_years = datetime_obj + timedelta(days=365 * 2)
    
    # Formater la date
    date_formatted = date_with_two_years.strftime("%Y-%m-%d")
    
    return date_formatted

