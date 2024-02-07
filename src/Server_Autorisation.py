# Server_Autorisation.py

import time
import Server_Acquisition

demande = None

def traiterDemande(demande):
    if not demande["isTraite"]:
        print("Traitement de la demande : ", demande['idLog'])
        demande["isTraite"] = True

while True:
    if Server_Acquisition.demandeTransitVersServeurAutorisation is not None:
        print("Demande à traiter : ", Server_Acquisition.demandeTransitVersServeurAutorisation)
        traiterDemande(Server_Acquisition.demandeTransitVersServeurAutorisation)
        Server_Acquisition.demandeTransitVersServeurAutorisation = None
    else:
        print("Aucune demande à traiter pour le moment.")
    time.sleep(5)  # Attendre 5 secondes avant la prochaine vérification
