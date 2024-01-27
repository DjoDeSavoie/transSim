#création d'un serveur NTP avec le module ntplib
#le serveur NTP est un serveur de temps qui permet de synchroniser les horloges des ordinateurs connectés à un réseau informatique

from time import ctime
import ntplib

# function retournant le temps du serveur NTP
def getTime():
    ntp = ntplib.NTPClient()
    response = ntp.request('europe.pool.ntp.org', version=3)
    return ctime(response.tx_time)
    
# affichage du temps du serveur NTP
print(getTime())
