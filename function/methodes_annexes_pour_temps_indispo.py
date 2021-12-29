from itertools import tee
from datetime import timedelta
from numpy import ceil
import pandas as pd


def pour_avoir_rang_suivant(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def creation_nouvelles_colonnes(xDF, i, day):
    # -- va créer une nouvelle ligne
    #    avec une date supp à la précédente -- #
    data = pd.DataFrame({"debut_env": xDF.loc[i, 'debut_env'] + timedelta(days=day),
                         "fin_env": (xDF.loc[i, 'debut_env'] + timedelta(days=day)) + timedelta(days=1),
                         "date_+24h": (xDF.loc[i, 'debut_env'] + timedelta(days=day)) + timedelta(days=1),
                         "temp_env": 1440}, index=[i])
    return data


def calcul_indispo_cum(xDF):
    # -- initialisation avec les premieres
    #    les valeurs du "df" -- #
    DATEDEBUT = xDF.loc[0, 'debut_env']
    DATE24 = xDF.loc[0, 'date_+24h']
    xDF.loc[0, 'Temps_indispo_cum'] = 0
    DISPOCUMUL = xDF.loc[0, 'Temps_indispo_cum']

    for i in range(0, len(xDF)):
        # -- puis reinitialisation des valeurs
        #    à chaque changement d'index  -- #
        date_debut = xDF.loc[i, 'debut_env']
        date_fin = xDF.loc[i, 'fin_env']
        date_24h = xDF.loc[i, 'date_+24h']

        if date_debut >= DATE24 :
            # -- si date debut de l'élément suivant
            #    + grande que l'élément précédant
            #    reinitialisation des valeurs
            #    avec les valeurs aux derniers index -- #
            DATEDEBUT = date_debut
            DATE24 = date_24h
            DISPOCUMUL = 0
            pass
        # -- si non -- #
        DISPOCUMUL = DISPOCUMUL + xDF.loc[i, 'temp_env']
        xDF.loc[i,'Temps_indispo_cum'] = DISPOCUMUL
        xDF.loc[i, 'debut_env'] = DATEDEBUT
        xDF.loc[i, 'fin_env'] = date_fin


def boucle_sur_les_jour(xDF):
    # -- on cherche touts les éléments supérieurs
    #    à 1440 minutes -- #
    data = pd.DataFrame()
    i = 0
    while i < len(xDF):

        if xDF.loc[i, 'temp_env'] > 1440:
            nb_days = ceil(xDF.loc[i, 'temp_env'] / 1440).astype(int)

            for day in range(0, nb_days -1):
                # -- va générer autant de colonnes
                #    que de nombres de jours et il va
                #    découper le "df" à l'endroit de la condition
                #    pour insérer les colonnes -- #
                data = creation_nouvelles_colonnes(xDF, i, day)
                xDF = pd.concat([xDF.iloc[:i], data, xDF.iloc[i:]]).reset_index(drop=True)
                i += 1
            # -- recuperation du reste --#`
            xDF.loc[i, 'debut_env'] = xDF.loc[i -1, 'debut_env'] + timedelta(days=1)
            xDF.loc[i, 'temp_env'] = xDF.loc[i, 'temp_env'] % 1440
            i += 1
        i += 1
    return xDF


def recherche_des_evenement(xDF):
    # -- recherche d'événement suivant la condition
    #    si vraie extraction des dates de debut
    #    et de fin et du statut "IS" -- #
    list_nom_pompe = []
    list_nom_site = []
    list_row = []
    list_IS = []
    xDF.reset_index(inplace=True)
    for itemA, itemB in pour_avoir_rang_suivant(xDF.itertuples()):

        if itemA[-1] == 1 and itemB[-1] == 0 or (itemA[-1] == 1 and itemB[-1] == 1):
            list_row.append(itemA[1])
            list_row.append(itemB[1])
            list_nom_site.append(itemA[2])
            list_nom_site.append(itemB[2])
            list_nom_pompe.append(itemA[3])
            list_nom_pompe.append(itemB[3])
            list_IS.append(itemA[-1])
            list_IS.append(itemB[-1])

    return list_row, list_IS, list_nom_pompe, list_nom_site
