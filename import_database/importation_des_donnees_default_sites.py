import pandas as pd

# 88888888888888-------88888888888888#
# ---- initialisation des données ---#
# - et reorganisation des colonnes --#
# 88888888888888-------88888888888888#
pd.options.mode.chained_assignment = None
data_de_base_pompe = pd.read_csv(r'/Users/mbpem/Desktop/projet_Pompe/Jeu_données_pompe2.csv')
df_data_de_base_pompe = pd.DataFrame(data_de_base_pompe)
# df_data_de_base_pompe["Site_Pompe"] = df_data_de_base_pompe[["libelle_site", "var_libelle_aff", "source_brute_variable"]].agg('-'.join, axis=1)
df_Fromat_pompe = df_data_de_base_pompe.drop(
    ['var_id_systeme_source', 'id_site', 'var_libelle', 'libelle_court_variable', 'var_famille','Commentaire (ne pas charger)'],
    axis=1)
mid = df_Fromat_pompe['libelle_site']
df_Fromat_pompe.drop(labels=['libelle_site'], axis=1,inplace = True)
df_Fromat_pompe.insert(0, 'libelle_site', mid)
# avoir dans un autre cas
# dfDefault = pd.DataFrame([df_data_de_base_pompe["var_libelle_aff"], df_data_de_base_pompe["Site_Pompe"]])
