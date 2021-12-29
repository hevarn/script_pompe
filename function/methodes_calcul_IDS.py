import os

import numpy as np
import pandas as pd
from function import auto_complete_value as CompleteValues
from function import methodes_conteur_temps_indispo as conteur_temps_indispo
from import_database import importation_des_donnees_liste_sites as extraction_variable


# -- calcul_ids va servir à calculer la disponibilité des pompes
#    puis a calculer la durée en temps --#
def calcul_ids(xDf_erreur_site, yDf_liste_site):
    global DEFELEC, NTH, secours, df_conteur_temps_indispo
    i = 0
    liste_nome_de_site = []
    liste_totale_site = []
    for item in yDf_liste_site.site:
        # -- si un nom de site dans "xDf_erreur_site"
        #    ce trouve dans "yDf_liste_site" -- #
        if item in xDf_erreur_site.libelle_site.tolist():

            liste_nome_de_site.append(item)
            nom_site = liste_nome_de_site[i]
            # -- création d'un df_temporaire pour transposer
            #    les colonnes 'horodate', 'nom_de_site', 'nom_de_pompe', 'Site_Pompe'
            #    avec les les "defaults" comme valeurs--#
            df_temporaire = pd.DataFrame(xDf_erreur_site[xDf_erreur_site["libelle_site"].str.contains(nom_site)])
            df_temporaire['nom_de_site'] = nom_site
            df_temporaire['nom_de_pompe'] = df_temporaire['source_brute_variable'].values
            df_temporaire["Site_Pompe"] = df_temporaire[["source_brute_variable", "var_libelle_aff"]].agg('@'.join,
                                                                                                          axis=1)
            df_erreur_site = \
                df_temporaire.reset_index().groupby(['horodate', 'nom_de_site', 'nom_de_pompe', 'Site_Pompe'])[
                    'defaut'].first().unstack()

            # -- redéfinition de l'ordre des colonnes
            #    pour que colonnes "DPP", "NTH" et "DEFELEC" soit toujours
            #    dans le même order de rangement
            #    création deux "df" -- #
            df_erreur_site_copy = df_erreur_site.copy()
            df_erreur_site_copy = df_erreur_site_copy.drop(
                # -- cherche les colonnes contenant "NTH" -- #
                df_erreur_site.loc[:, df_erreur_site.columns.str.contains("NTH")],
                axis=1)
            df_erreur_site_copy = df_erreur_site_copy.drop(
                # -- cherche les colonnes contenant "DEFELEC" -- #
                df_erreur_site.loc[:, df_erreur_site.columns.str.contains("DEFELEC")],
                axis=1)
            df_erreur_site = df_erreur_site.drop(
                # -- cherche les colonnes contenant "DPP" -- #
                df_erreur_site.loc[:, df_erreur_site.columns.str.contains("DPP")],
                axis=1)
            # -- puis merge les deux "df" -- #
            df_erreur_site_merge = pd.merge(df_erreur_site_copy, df_erreur_site, how="outer", on=["horodate",
                                                                                                  'nom_de_site',
                                                                                                  "nom_de_pompe"])
            # -- complete les valeurs manquantes -- #
            df_erreur_site_merge = CompleteValues.auto_complete_values(df_erreur_site_merge)
            # -- extraction des valeurs de "npn", "npi", "secours"
            #    via le source d'origine --#
            npn, secours, npi = extraction_variable.extraction_de_variable(nom_site)
            # -- -- #
            df_calcul_indispo_pompe = conteur_temps_indispo.calcul_indispo_pompe(npn,
                                                                                 secours,
                                                                                 df_erreur_site_merge,
                                                                                 npi)
            # -- -- #
            valeur_sortie = conteur_temps_indispo.conteur_temps_indispo(df_calcul_indispo_pompe,
                                                                 nom_site)
            if valeur_sortie is not None:
                liste_totale_site.append(valeur_sortie)

            i += 1
    return pd.concat(liste_totale_site)

