import psycopg2.extras
import pandas as pd

from CSVhandler import convert_csv_to_sql
from databaseHandler import connect_to_database, select_all_from_database, select_total_number_of_vaccines
from graphicData import graphic_data

# graphic_data()

# convert_csv_to_sql()
conn = connect_to_database()

#select_all_from_database(conn)
select_total_number_of_vaccines(conn)

choice = 0

while choice != 4:
    print("Choisissez un diagramme à afficher \n"
          "1)Nombre total de vaccin \n"
          "2)Nombre de vaccins par mois \n"
          "3)Evolution du nombre de vaccins au court du temps \n"
          "4)Quitter")

    choice = int(input())

    if choice == 1:
        print("Nombre total de vaccin")
    elif choice == 2:
        print("Nombre de vaccins par mois")
    elif choice == 3:
        print("Evolution du nombre de vaccins au court du temps")
    else:
        print("Au revoir !")

print("Fin du programme")
conn.close()  # Ferme la connexion à la bdd
