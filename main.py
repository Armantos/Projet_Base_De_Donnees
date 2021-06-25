import psycopg2.extras
import pandas as pd

################## Connection à la base de données###############################################
conn = psycopg2.connect(host="localhost", user="postgres", password="root", database="postgres")

##################Conversion d'un fichier CSV###############################################
data = pd.read_csv('stocks-plateformes.csv', sep=';', engine='python')
df = pd.DataFrame(data, columns=['nb_UCD', 'nb_doses', 'type_de_vaccin', 'date'])

print(df)

##################Creation de la table dans la bdd###############################################
# with conn == conn.commit() ==> valide les changements faits à la bdd
with conn:
    # with conn.cursor(...) == declaration + cur.close()
    # DictCursor affiche le curseur sous forme de dictionnaire []
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS stock_plateformes ('
                    'nb_UCD int NOT NULL ,'
                    'nb_doses int NOT NULL,'
                    'type_de_vaccin varchar(50) NOT NULL,'
                    'date varchar(50) NOT NULL)'
                    ';')

        print("creation table reussie")

        ##################Insertion des données dans la bdd###############################################
        for row in df.itertuples():
            sql = "INSERT INTO stock_plateformes VALUES (%s,%s,%s,%s);"
            val = (row.nb_UCD,
                   row.nb_doses,
                   row.type_de_vaccin,
                   row.date)
            cur.execute(sql, val)
        print("insertion reussie")

        ##################Lectures des données dans la bdd###############################################
        cur.execute("SELECT * FROM stock_plateformes WHERE nb_ucd = 0 ;")
        print(cur.fetchall())

conn.close()

# TODO affichage des données avec pandas
