from itertools import tee
from datetime import timedelta
from numpy import ceil
import pandas as pd


def pour_avoir_rang_suivant(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def creation_nouvelles_colonnes(xDF, i, day):
    data = pd.DataFrame({"debut_env": xDF.loc[i, 'debut_env'] + timedelta(days=day),
                         "fin_env": (xDF.loc[i, 'debut_env'] + timedelta(days=day)) + timedelta(days=1),
                         "date_+24h": (xDF.loc[i, 'debut_env'] + timedelta(days=day)) + timedelta(days=1),
                         "temp_env": 1440}, index=[i])
    return data


def calcul_indispo_cum(xDF):
    DATEDEBUT = xDF.loc[0, 'debut_env']
    DATE24 = xDF.loc[0, 'date_+24h']
    xDF.loc[0, 'indispo cumul'] = 0
    xDF.loc[0, 'indispo cumul'] = xDF.loc[0, 'indispo cumul'].astype(int)
    DISPOCUMUL = xDF.loc[0, 'indispo cumul']
    for i in range(0, len(xDF)):
        date_debut = xDF.loc[i, 'debut_env']
        date_fin = xDF.loc[i, 'fin_env']
        date_24h = xDF.loc[i, 'date_+24h']
        if date_debut >= DATE24 :
            DATEDEBUT = date_debut
            DATE24 = date_24h
            DISPOCUMUL = 0
            pass

        DISPOCUMUL = DISPOCUMUL + xDF.loc[i, 'temp_env']
        xDF.loc[i, 'indispo cumul'] = DISPOCUMUL
        xDF.loc[i, 'debut_env'] = DATEDEBUT
        xDF.loc[i, 'fin_env'] = date_fin


def boucle_sur_les_jour(xDF):
    data = pd.DataFrame()
    i = 0
    while i < len(xDF):
        if xDF.loc[i, 'temp_env'] > 1440:
            nb_days = ceil(xDF.loc[i, 'temp_env'] / 1440).astype(int)
            for day in range(0, nb_days):
                data = creation_nouvelles_colonnes(xDF, i, day)
                xDF = pd.concat([xDF.iloc[:i], data, xDF.iloc[i:]]).reset_index(drop=True)
                i += 1
            xDF.loc[i, 'temp_env'] = xDF.loc[i, 'temp_env'] % 1440
            i += 1
        i += 1
    return xDF


def recherche_des_evenement(xDF):
    list_row = []
    list_IS = []
    xDF.reset_index(inplace=True)
    for itemA, itemB in pour_avoir_rang_suivant(xDF.itertuples()):
        if itemA[-1] == 1 and itemB[-1] == 0 or (itemA[-1] == 1 and itemB[-1] == 1):
            list_row.append(itemA[1])
            list_row.append(itemB[1])
            list_IS.append(itemA[-1])
            list_IS.append(itemB[-1])
    return list_row, list_IS
