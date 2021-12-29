from datetime import timedelta
import numpy as np
import pandas as pd
from numpy import ceil

from function.methodes_annexes_pour_temps_indispo import recherche_des_evenement, boucle_sur_les_jour, calcul_indispo_cum


def calcul_indispo_pompe(NPN, SECOURS, xDF, NPI):
    # -- suivant les 0 ou 1 dans chaque
    #    colonne on détermine si indispo où non -- #
    global ROW
    a = (len(xDF.columns))
    i = 0
    list_empty_empty = []
    for item in xDF.iloc[:, range(0, a)].itertuples():
        # -- positionnement dans l'espace à quoi correspond
        #    tel où bien telle colonne -- #
        DEFelec = xDF.iloc[i, (a - 1)]
        NTh = xDF.iloc[i, (a - 2)]
        ROW = range(0, (a - 2))
        DPP = int(sum(xDF.iloc[i, ROW]))
        # -- calcul d'indisponibilité -- #
        if DEFelec == 1 or (SECOURS > 0 and DPP < NPN) or (SECOURS == 0 and DPP < NPN and NTh == 1):
            list_empty_empty.append(1)
        else:
            list_empty_empty.append(0)
        i += 1
    xDF['IS'] = list_empty_empty
    return xDF


def conteur_temps_indispo(xDF, nom_de_site):
    # -- va déterminer la durée de l'erreur-- #
    TP4 = 240
    # -- va chercher touts les événements
    #    commençant par 1 et ceux términant par 0 -- #

    list_row, list_IS, list_nom_pompe, list_nom_site = recherche_des_evenement(xDF)

    # -- si list != de vide  -- #
    if list_row and list_IS:
        # -- initialisation d'un "df" vide -- #
        a = {}
        df_temporaire = pd.DataFrame(a)
        # -- initialisation du "df_temporaire"
        #    avec les différentes listes
        #    reçue de la methode "recherche_des_evenement" -- #
        df_temporaire['nom_site'] = list_nom_site
        df_temporaire['nom_pompe'] = list_nom_pompe
        df_temporaire['date'] = list_row
        df_temporaire['IS'] = list_IS
        df_temporaire['debut_env'] = df_temporaire.loc[df_temporaire['IS'] == 1, 'date']
        df_temporaire['fin_env'] = df_temporaire.loc[(df_temporaire['IS'] == 0) | (df_temporaire['IS'] == 1), 'date']
        df_temporaire['fin_env'] = df_temporaire['fin_env'].shift(-1, axis=0)
        df_temporaire['date_+24h'] = df_temporaire['debut_env'] + timedelta(days=1)
        df_temporaire['total'] = df_temporaire["fin_env"].sub(df_temporaire["debut_env"])
        df_temporaire['total'] = df_temporaire['total'].dt.total_seconds() / 60.0
        # -- liste des futures colonnes "df_liste_erreur_site"-- #
        col = ['nom_site', 'nom_pompe', 'date', 'IS', 'debut_env', 'fin_env', 'date_+24h', 'temp_env']
        # -- merge avec "df_temporaire" et nom des colonnes -- #
        df_liste_erreur_site = pd.DataFrame(np.array(df_temporaire)[::2], columns=col)
        df_liste_erreur_site = df_liste_erreur_site.drop(['date', 'IS'], axis=1)
        df_liste_erreur_site['temp_env'] = df_liste_erreur_site['temp_env'].astype(int)
        # -- recherche des jours supp à 1440 minutes-- #
        df_liste_erreur_site = boucle_sur_les_jour(df_liste_erreur_site)
        # -- recherche des jours inf à 1440 minutes-- #
        calcul_indispo_cum(df_liste_erreur_site)

        # -- 'Temps_indispo_cum' - 240 minutes -- #
        df_liste_erreur_site['Temps_indispo_cum'] = df_liste_erreur_site['Temps_indispo_cum'] - TP4
        df_liste_erreur_site['Temps_indispo_cum'] = df_liste_erreur_site['Temps_indispo_cum'].astype(int)
        # -- application d'un masque pour éviter
        #    les chiffres negatives -- #
        df_liste_erreur_site['Temps_indispo_cum'] = df_liste_erreur_site['Temps_indispo_cum'].mask(df_liste_erreur_site['Temps_indispo_cum'] < 0).fillna(0).astype(int)

        df_liste_erreur_site['NBhpen'] = ceil(df_liste_erreur_site['Temps_indispo_cum'] / 60).astype(int)
        df_liste_erreur_site['penalisation'] = (df_liste_erreur_site['NBhpen'] * 100).astype(int)
        # -- auto-complete les valeurs manquantes -- #
        df_liste_erreur_site = df_liste_erreur_site.ffill()

        # df_liste_erreur_site['nom_de_pompe'] = nom_de_pompe
        return df_liste_erreur_site





