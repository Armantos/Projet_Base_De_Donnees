import psycopg2.extras
import pandas as pd
import matplotlib.pyplot as plt
from CSVhandler import convert_csv_to_sql
from graphicData import graphic_data


def connect_to_database():
    # ################# Connection à la base de données###############################################
    conn = psycopg2.connect(host="localhost", user="postgres", password="root", database="postgres")
    print("Connexion à la bdd réussie")
    return conn


def insert_into_database(conn):
    df = convert_csv_to_sql()
    # #################Manipulation de la bdd###############################################
    # with conn == commit ==> valide les changements faits à la bdd
    # with conn:
    # DictCursor affiche le curseur sous forme de dictionnaire []
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # #################Creation de la table dans la bdd###############################################
        # TODO empecher l'insertion de doublons (avec UNIQUE ?)
        cur.execute('CREATE TABLE IF NOT EXISTS stock_plateformes ('
                    'nb_UCD int NOT NULL ,'
                    'nb_doses int NOT NULL,'
                    'type_de_vaccin varchar(50) NOT NULL,'
                    'date varchar(50) NOT NULL)'
                    ';')

        print("creation table reussie")

        # #################Insertion des données dans la bdd###############################################
        for row in df.itertuples():
            sql = "INSERT INTO stock_plateformes VALUES (%s,%s,%s,%s);"
            val = (row.nb_UCD,
                   row.nb_doses,
                   row.type_de_vaccin,
                   row.date)
            cur.execute(sql, val)
        print("insertion reussie")


# conn.close()


def update_from_database(conn):
    print("update")


def delete_from_database(conn):
    print("delete")


def select_all_from_database(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # #################Lectures des données dans la bdd###############################################
        cur.execute("SELECT * FROM stock_plateformes ;")
        print(cur.fetchall())


def select_total_number_of_vaccines(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # #################Lectures des données dans la bdd###############################################
        """
        sql_query = "SELECT SUM(nb_doses),type_de_vaccin FROM stock_plateformes GROUP BY type_de_vaccin ;"
        cur.execute(sql_query)
        print(cur.fetchall())
        """
        sql_query = pd.read_sql_query(
            "SELECT SUM(nb_doses) AS nombre_de_doses ,type_de_vaccin "
            "FROM stock_plateformes "
            "GROUP BY type_de_vaccin",
            conn)

        df = pd.DataFrame(sql_query, columns=['nombre_de_doses', 'type_de_vaccin'])
        df.plot(x="type_de_vaccin", y="nombre_de_doses", kind="bar", rot=4, fontsize=8) # nb doses en millions
        #df.plot.pie( y="nombre_de_doses", label="type_de_vaccin")
        #df.hist()
        plt.show()
        #print(df)
