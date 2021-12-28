import pandas as pd

pd.options.mode.chained_assignment = None
data_de_base_site = pd.read_csv(r'/Users/mbpem/Desktop/projet_Pompe/donnees_Pompes.csv')
df_data_de_base_site = pd.DataFrame(data_de_base_site)
df_data_de_base_site = df_data_de_base_site.drop(["npi", "npn"], axis=1)


def extraction_de_variable(nameSite):
    secours = pd.DataFrame(data_de_base_site)
    for row in secours.iterrows():
        if row[1][0] in nameSite:
            var_global = row[1]
            var_npi = var_global[1]
            var_npn = var_global[2]
            var_secours = var_global[3]

            return var_npn, var_secours, var_npi
