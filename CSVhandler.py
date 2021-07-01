import pandas as pd


def convert_csv_to_sql():
    # #################Conversion d'un fichier CSV###############################################
    data = pd.read_csv('stocks-plateformes.csv', sep=';', engine='python')
    df = pd.DataFrame(data, columns=['nb_UCD', 'nb_doses', 'type_de_vaccin', 'date'])

    return df
