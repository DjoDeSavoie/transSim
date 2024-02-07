import json
import time

#variable contenant la valeur de la demande a traiter
demandeTransitVersServeurAutorisation = None


def lireFichierJson(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)

def ecrireFichierJson(chemin_fichier, contenu):
    with open(chemin_fichier, 'w') as f:
        json.dump(contenu, f, indent=4)

def traiterDemande(demande):
    if not demande["isTraite"]:
        print("Traitement de la demande : ", demande['idLog'])
        demande["isTraite"] = True


def checkDemandesNonTraitees(demandes):
    demande_a_traiter = None
    for demande in demandes:
        if not demande["isTraite"]:
            traiterDemande(demande)
            demande_a_traiter = demande
            print("Demande à traiter : ", demande)
            #on stocke la demande dans la variable demandeTransitVersServeurAutorisation
            demandeTransitVersServeurAutorisation = demande
            break
    if demande_a_traiter is None:
        print("Toutes les demandes ont déjà été traitées.")
        return

    # Mettre à jour la demande traitée dans le fichier JSON
    ecrireFichierJson(chemin_fichier_json, demandes)

    # Vérifier s'il y a d'autres demandes non traitées
    for demande in demandes:
        if not demande["isTraite"]:
            print("Il reste d'autres demandes non traitées.")
            break

if __name__ == "__main__":
    chemin_fichier_json = "logs/logsTPE/logsTPE.json"

    while True:
        demandes = lireFichierJson(chemin_fichier_json)
        checkDemandesNonTraitees(demandes)
        # Attendre un certain temps avant de vérifier à nouveau le fichier JSON
        time.sleep(5)  # Attendre 5 secondes avant la prochaine vérification
        
        
