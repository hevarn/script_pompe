import pandas as pd
from function import auto_complete_value as CompleteValues
from function import methodes_conteur_temps_indispo as conteur_temps_indispo
from import_database import importation_des_donnees_liste_sites as extraction_variable

# -- calcul_ids va servir à calculer la disponibilité des pompes
#    puis a calculer la durée en temps --#
def calcul_ids(xDf_erreur_site, yDf_liste_site):
    global DEFELEC, NTH, secours
    i = 0
    liste_nome_de_site = []
    for item in yDf_liste_site.site:
        # -- si un nom de site dans "xDf_erreur_site"
        #    ce trouve dans "yDf_liste_site" -- #
        if item in xDf_erreur_site.libelle_site.tolist():

            liste_nome_de_site.append(item)
            nom_site = liste_nome_de_site[i]
            # -- création d'un df_temporaire pour fusionner
            #    les colonnes "nom de pompe" + "nom erreur"--#
            df_temporaire = pd.DataFrame(xDf_erreur_site[xDf_erreur_site["libelle_site"].str.contains(nom_site)])
            df_temporaire["Site_Pompe"] = df_temporaire[["source_brute_variable", "var_libelle_aff"]].agg('@'.join, axis=1)
            df_erreur_site = df_temporaire.reset_index().groupby(['horodate', 'Site_Pompe'])['defaut'].first().unstack()

            # ---- "df_erreur_site" this order "IDP -> NTH -> DEFelec"  ----#
            df_erreur_site_copy = df_erreur_site.copy()
            df_erreur_site_copy = df_erreur_site_copy.drop(
                df_erreur_site.loc[:, df_erreur_site.columns.str.contains("NTH")],
                axis=1)
            df_erreur_site_copy = df_erreur_site_copy.drop(
                df_erreur_site.loc[:, df_erreur_site.columns.str.contains("DEFELEC")],
                axis=1)
            df_erreur_site = df_erreur_site.drop(df_erreur_site.loc[:, df_erreur_site.columns.str.contains("DPP")], axis=1)
            dfResult_merge = pd.merge(df_erreur_site_copy, df_erreur_site, how="outer", on=["horodate"])
            dfSort_values = CompleteValues.auto_complete_values(dfResult_merge)
            npn, secours, npi = extraction_variable.extraction_de_variable(nom_site)
            value = conteur_temps_indispo.calcul_indispo_pompe(npn, secours, dfSort_values, npi)
            value = conteur_temps_indispo.conteur_temps_indispo(value, nom_site)
            #value.to_csv('resulat_indispo_pompe.csv')
            i += 1
