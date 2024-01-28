import pymysql

# Remplacez ces valeurs par les vôtres
db_host = "34.163.159.223"
db_user = "root"
db_name = "bdd_porteur"

# Établissez la connexion
conn = pymysql.connect(host=db_host, user=db_user, database=db_name)

# Créez un objet cursor pour interagir avec la base de données
cursor = conn.cursor()

# Exemple de requête pour récupérer des données
cursor.execute("SELECT * FROM ")

# Récupérez les résultats
results = cursor.fetchall()

# Affichez les résultats
for row in results:
    print(row)

# N'oubliez pas de fermer les connexions
cursor.close()
conn.close()
