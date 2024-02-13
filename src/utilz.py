############################################    Utilz    ############################################



######### Fonction de hachage SHA-256 #########
import hashlib

def hash_sha256(data):
    # Créer un objet hash SHA-256
    sha256_hash = hashlib.sha256()

    # Mettre à jour l'objet hash avec les données à hasher (doit être des bytes)
    sha256_hash.update(data.encode('utf-8'))

    # Obtenir la représentation hexadécimale du hash
    hashed_data = sha256_hash.hexdigest()

    return hashed_data


# Fonction pour vérifier le solde
def verifier_solde():
    type_compte = input(f"{Fore.YELLOW}Entrez le type de votre compte ('emetteur' : 1 ou 'acquereur': 2) :")
    id_compte = input(f"{Fore.YELLOW}Entrez l'ID de votre compte : ")
    solde = verifieSolde(id_compte, type_compte)
    if solde is not None:
        print(f"{Fore.CYAN}Le solde de votre compte est de {solde}€.")



