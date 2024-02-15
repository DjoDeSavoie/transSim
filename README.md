# transSim
Projet de simulateur de transaction par carte bancaire développé en python


# Introduction
Ce système de gestion des transactions permet de traiter des transactions financières entre des comptes émetteurs et acquéreurs. Il comprend plusieurs composants interconnectés qui gèrent les différentes étapes d'une transaction, y compris la vérification des soldes, la génération des autorisations et le routage interbancaire.    

# Configuration
Assurez-vous que votre environnement est configuré avec Python 3.x et que vous avez installé les dépendances nécessaires comme pymysql et colorama en utilisant pip:

pip3 install pymysql
pip install getpass4
pip install termcolor
pip install ntplib


# Composants
Server Acquisition : Ce composant exécute une boucle qui surveille continuellement les fichiers de logs dans le répertoire logs/logsTPE/. Il recherche des transactions marquées comme non traitées ("isTraite": false). Lorsqu'une transaction non traitée est détectée, le Server Acquisition appelle le Server Autorisation pour commencer le processus de vérification et d'autorisation.

Server Autorisation : Ce composant est chargé de la vérification des fonds disponibles dans le compte émetteur. Il confirme que le solde est suffisant pour couvrir la transaction demandée. Si les fonds sont suffisants, le serveur procède à l'autorisation de la transaction et enregistre les détails dans la table autorisationtransaction de la base de données.

Routage Interbancaire : Lorsqu'une transaction implique deux banques différentes, le système active un processus de routage interbancaire. Ce service s'assure que les transactions soient correctement acheminées entre les banques émettrices et acquéreurs, en respectant les protocoles interbancaires et les formats d'échange de données.

TPE (Terminal de Paiement Électronique) : Ce terminal virtuel est utilisé pour initier les transactions. Il simule l'interaction d'un terminal physique en envoyant des demandes de transaction au Server Acquisition et en recevant des autorisations du Server Autorisation.

Serveur NTP (Network Time Protocol) : Ce serveur est utilisé pour obtenir des horodatages précis et synchronisés pour chaque transaction. Les horodatages sont essentiels pour la traçabilité et l'audit des transactions.

Utilz : Ce composant est un ensemble d'outils ou de bibliothèques utilitaires utilisés à travers le système pour des tâches communes telles que la manipulation de dates, la génération de logs, etc.

creationBanque : Ce script ou fonction est responsable de l'ajout de nouvelles banques dans la base de données. Il ajoute des enregistrements à la table banque avec les informations nécessaires pour chaque banque nouvellement créée.

creationCarte : Ce composant gère la création de nouvelles cartes bancaires. Il génère les numéros de cartes, les pins, et les dates d'expiration, puis les sauvegarde dans la base de données.

creationCompteAcquereur : Ce script crée de nouveaux comptes acquéreurs qui sont utilisés pour recevoir des fonds lors des transactions. Ces comptes sont ajoutés à la table comptebancaireacquereur avec les détails appropriés.

creationCompteEmetteur : De même, ce script crée de nouveaux comptes émetteurs utilisés pour envoyer de l'argent dans les transactions. Les informations de ces comptes sont stockées dans la table comptebancaireemetteur.

# Fonctionnalités
Traitement de Transactions : Les transactions sont lues à partir d'un fichier de logs JSON. Chaque transaction contient des informations telles que les numéros de compte émetteur et acquéreur, le montant et la date de la transaction.

Vérification des Soldes : Avant de procéder à une transaction, le système vérifie que le compte émetteur dispose d'un solde suffisant.

Génération d'Autorisation : Pour chaque transaction réussie, une autorisation est générée et stockée dans la table autorisationtransaction de la base de données.

Routage des Transactions : Les transactions entre différentes banques sont gérées par le système de routage interbancaire.

Affichage des Tickets : Après chaque transaction, un ticket de caisse est généré affichant les détails de l'autorisation.

# Utilisation
Pour démarrer le système, exécutez le fichier main.py qui lancera le menu principal et permettra aux utilisateurs de choisir différentes actions telles que vérifier le solde, effectuer une transaction ou arrêter le programme.

python main.py

Le système gère automatiquement les transactions en arrière-plan via un processus multithread qui surveille les fichiers de logs JSON.

# Structure de Base de Données
La base de données contient plusieurs tables pour stocker les informations relatives aux transactions, aux comptes émetteurs et acquéreurs, et aux autorisations de transaction. Voici un aperçu de la structure des tables principales :

comptebancaireemetteur : Stocke les détails des comptes émetteurs.
comptebancaireacquereur : Stocke les détails des comptes acquéreurs.
autorisationtransaction : Enregistre les autorisations de transactions réussies.
banque : Liste de toutes les banques
tpe : liste des tpe
carte bancaire : liste des cartes bancaires

# Logs
Les fichiers de logs sont stockés dans le dossier logs/logsTPE/ et sont au format JSON. Ils contiennent les détails des transactions à traiter et sont constamment surveillés par le système pour le traitement.

# Sécurité
Le hachage avec sha256 a été mis en place pour garantir une sécurité optimale tout au long de la transaction.




