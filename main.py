from datetime import date

import pandas as pd

from import_database import importation_des_donnees_liste_sites
from import_database import importation_des_donnees_default_sites
from function import methodes_calcul_IDS as calcul_IDS

now = date.today()
# -- df de base --#
df_erreur_site = importation_des_donnees_default_sites.df_Fromat_pompe
df_erreur_site['horodate'] = pd.to_datetime(df_erreur_site['horodate'], format='%Y-%m-%d %H:%M:%S')
df_liste_site = importation_des_donnees_liste_sites.df_data_de_base_site

# -- importation des df dans la methode IDS--#
df_final = calcul_IDS.calcul_ids(df_erreur_site, df_liste_site)

df_final.to_csv('resultat.csv')