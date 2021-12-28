from datetime import timedelta
import numpy as np
import pandas as pd
from numpy import ceil

from function.methodes_pour_temps_indispo import recherche_des_evenement, boucle_sur_les_jour, calcul_indispo_cum


def calcul_indispo_pompe(NPN, SECOURS, xDF, NPI):
    global ROW
    a = (len(xDF.columns))  # 88888
    i = 0
    DEFelec = 1
    NTh = 1
    list_empty_empty = []
    NTH = xDF.columns.str.contains('NTH', case=False)
    DEFELEC = xDF.columns.str.contains('DEFELEC', case=False)
    for item in xDF.iloc[:, range(0, a)].itertuples():
        DEFelec = xDF.iloc[i, (a - 1)]
        NTh = xDF.iloc[i, (a - 2)]
        ROW = range(0, (a - 2))
        DPP = int(sum(xDF.iloc[i, ROW]))
        if DEFelec == 1 or (SECOURS > 0 and (DPP < NPN)) or (SECOURS == 0 and (DPP < NPN) and NTh == 1):
            list_empty_empty.append(1)
        else:
            list_empty_empty.append(0)
        i += 1
    xDF['IS'] = list_empty_empty
    print(xDF)
    return xDF


def conteur_temps_indispo(xDF, name):
    TP4 = 240
    list_row, list_IS = recherche_des_evenement(xDF)
    a = {}
    df_A = pd.DataFrame(a)
    df_A['date'] = list_row
    df_A['IS'] = list_IS
    df_A['debut_env'] = df_A.loc[df_A['IS'] == 1, 'date']
    df_A['fin_env'] = df_A.loc[(df_A['IS'] == 0) | (df_A['IS'] == 1), 'date']
    df_A['fin_env'] = df_A['fin_env'].shift(-1, axis=0)
    df_A['date_+24h'] = df_A['debut_env'] + timedelta(days=1)
    df_A['total'] = df_A["fin_env"].sub(df_A["debut_env"])
    df_A['total'] = df_A['total'].dt.total_seconds() / 60.0
    col = ['date', 'IS', 'debut_env', 'fin_env', 'date_+24h', 'temp_env']
    dfnew = pd.DataFrame(np.array(df_A)[::2], columns=col)
    dfnew = dfnew.drop(['date', 'IS'], axis=1)
    dfnew['temp_env'] = dfnew['temp_env'].astype(int)
    dfnew = boucle_sur_les_jour(dfnew)
    dfnew['Temps_indispo'] = dfnew['temp_env'] - TP4
    dfnew['Temps_indispo'] = dfnew['Temps_indispo'].mask(dfnew['Temps_indispo'] < 0).fillna(0).astype(int)
    dfnew['NBhpen'] = ceil(dfnew['Temps_indispo'] / 60).astype(int)
    dfnew['penalisation'] = (dfnew['NBhpen'] * 100).astype(int)
    calcul_indispo_cum(dfnew)
    print(dfnew)





