import pandas as pd


def convert_csv_to_sql():
    # #################Conversion d'un fichier CSV###############################################
    data = pd.read_csv("donnees-vaccination-par-tranche-dage-type-de-vaccin-et-departement.csv" , sep=';', engine='python')
    df = pd.DataFrame(data, columns=['region_residence','libelle_region','departement_residence','libelle_departement','population_insee','classe_age','libelle_classe_age','type_vaccin','effectif_1_inj','effectif_termine','effectif_cumu_1_inj','effectif_cumu_termine','date'])
    
    return df