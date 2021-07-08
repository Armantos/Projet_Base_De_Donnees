import psycopg2.extras
import pandas as pd
import matplotlib.pyplot as plt
from CSVhandler import convert_csv_to_sql


def connect_to_database():
    # ################# Connection à la base de données###############################################
    conn = psycopg2.connect(host="localhost", user="postgres", password="root", database="postgres")
    print("Connexion à la bdd réussie")
    return conn


def insert_into_database(conn):
    df = convert_csv_to_sql()
    

    # #################Manipulation de la bdd###############################################
    # with conn == COMMIT ==> valide les changements faits à la bdd
    # with conn:
    # DictCursor affiche le curseur sous forme de dictionnaire []
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # #################Creation de la table dans la bdd###############################################
        # TODO empecher l'insertion de doublons (avec UNIQUE ?)
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Vaccin (
                    Nom_Vaccin VARCHAR(50) UNIQUE NOT NULL,
                    PRIMARY KEY (Nom_Vaccin));COMMIT;''')

        print("creation table Vaccin reussie")
        
  
        cur.execute('''CREATE TABLE IF NOT EXISTS TranchesAges (
                    ID_tranches VARCHAR(50) NOT NULL,
                    Libelle_tranche VARCHAR(50),
                    PRIMARY KEY (ID_tranches) );COMMIT;''')

        print("creation table TranchesAges reussie")
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Region (
                    ID_region INT NOT NULL,
                    Libelle_region VARCHAR(50),
                    Nbr_population INT NOT NULL,
                    PRIMARY KEY (ID_region) );COMMIT;''')

        print("creation table Region reussie")
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Departements (
                    ID_departement VARCHAR(50) NOT NULL,
                    Libelle_departement VARCHAR(50),
                    ID_region INT NOT NULL,
                    PRIMARY KEY (ID_departement),
                    FOREIGN KEY (ID_region) REFERENCES Region (ID_region)
                    );COMMIT;''')

        print("creation table Departements reussie")
        
        cur.execute('''CREATE TABLE IF NOT EXISTS Vaccinations (
                    ID_vaccination SERIAL PRIMARY KEY,
                    eff_1_dose BIGINT,
                    eff_2_dose BIGINT,
                    eff_total_1_dose BIGINT,
                    eff_total_2_dose BIGINT,
                    Nom_Vaccin VARCHAR(50) NOT NULL,
                    ID_departement VARCHAR(50) NOT NULL,
                    ID_tranches VARCHAR(50) NOT NULL,
                    FOREIGN KEY (Nom_Vaccin) REFERENCES Vaccin (Nom_Vaccin),
                    FOREIGN KEY (ID_departement) REFERENCES Departements (ID_departement),
                    FOREIGN KEY (ID_tranches) REFERENCES TranchesAges (ID_tranches)) ;COMMIT;''')

        print("creation table Vaccinations reussie")

        # #################Insertion des données dans la bdd###############################################
        for row in df.itertuples():
            if ((row.date == "2021-06-27") and (row.departement_residence != "Tout département")):
                sql = "INSERT IGNORE INTO Vaccin VALUES (%s);"
                val = (row.type_vaccin)
                cur.execute(sql, val)
        print("insertion reussie pour vaccin")
        
        """
        for row in df.itertuples():
            if ((row.date == "2021-06-27") and (row.departement_residence != "Tout département")):
                sql = "INSERT IGNORE INTO TanchesAges VALUES (%s,%s);"
                val = (row.classe_age, 
                       row.libelle_classe_age)
                cur.execute(sql, val)
        print("insertion reussie pour les classes ages")
        
        for row in df.itertuples():
            if ((row.date == "2021-06-27") and (row.departement_residence != "Tout département") and (row.class_age == "TOUT_AGE")):
                sql = "INSERT INTO Region VALUES (%d,%s,%d);"
                val = (row.region_residence,
                       row.libelle_region,
                       row.population_insee)
                cur.execute(sql, val)
        print("insertion reussie pour les Regions")
        
        for row in df.itertuples():
            if ((row.date == "2021-06-27") and (row.departement_residence != "Tout département")):
                sql = "INSERT INTO Departements VALUES (%s,%s,%d);"
                val = (row.departement_residence,
                       row.libelle_departement,
                       row.region_residence)
                cur.execute(sql, val)
        print("insertion reussie pour les residences")
        
        for row in df.itertuples():
            if ((row.date == "2021-06-27") and (row.departement_residence != "Tout département")):
                sql = "INSERT INTO Vaccinations VALUES (%d,%d,%d,%d,%s,%s);"
                val = (row.effectif_1_inj,
                       row.effectif_termine,
                       row.effectif_cumu_1_inj,
                       row.effectif_cumu_termine,
                       row.type_vaccin,
                       row.departement_residence,
                       row.classe_age)
                cur.execute(sql, val)
        print("insertion reussie pour les residences")
"""
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
    
