import numpy as np
import pandas as pd

"""
Ce fichier contient les étapes de prétraitements faites sur les données avant de les utiliser pour le clustering.
"""

def duplication(data,groupby_column,start_col_index,end_col_index):
    """
    Duplicaton des informations constantes pour certaines variables
    """

    for i in range(start_col_index,end_col_index + 1):
        col = data.columns[i]
        data[col] = data.groupby(groupby_column)[col].ffill() 
    return data 



def encodage_colonne(data, column_name, category_mappings):
    """
    Cette fonction encode les colonnes categorielles dans lequelles les cellules contiennent des combinaisons de catégories.
    On decode la colonne initiale en plusieurs colonnes 
    On commence par remplir ces colonnes par nan
    Apres on remplace par 1 ou 0 selon la valeur dans la colonne initiale
    On supprime la colonne initiale
    """   

    for categories in category_mappings.values():
        for category in categories:
            data[category] = np.nan

    for index, value in data[column_name].iteritems():
        if not pd.isna(value) and value in category_mappings:
            for category in category_mappings[value]:
                data.at[index, category] = 1
            
            unchecked_categories = {item for sublist in category_mappings.values() for item in sublist} - set(category_mappings[value])
            for unchecked_category in unchecked_categories:
                data.at[index, unchecked_category] = 0 

    data.drop(column_name, axis=1, inplace=True)  
     
    return data


def fill_based_on_condition_list(data, condition_col, values, target_cols, nouvelle_valeur):
    """
    Cette fonction remplis les nan dans certaines colonnes par 0 en 
    prenant compte si l'evenement a eu lieu ou non selon une autre colonne
    """

    if not isinstance(values, list):
        values = [values]
    for col in target_cols:
        data.loc[data[condition_col].isin(values), col] = data.loc[data[condition_col].isin(values), col].fillna(nouvelle_valeur)
    
    return data


def replace_nouveau_categorie(data, col, valeur_existante,nouvelle_valeurs):
    """
    Creation d'une nouvelle catégorie pour tous les textes
    """

    condition = (data[col] != valeur_existante) & data[col].notna()
    data.loc[condition, col] = nouvelle_valeurs

    return data


def replacer_plusieurs_categorie(data, col, replacement_dict):
    """
    Chaque collection de textes est remplacer par une categorie
    """

    for value, keys in replacement_dict.items():
        for key in keys: 
            data[col] = data[col].replace(key, value)

    return data



def extract_year_from_columns(data, date_cols):
    """
    Extraire les années des colonnes de date.
    """
    for col in date_cols:
        mask = ~data[col].apply(lambda x: isinstance(x, (int, float)))
        data.loc[mask, col] = pd.to_datetime(data[mask][col], errors='coerce').dt.year
    return data


def compute_age_difference(data, start_col, end_col, new_col):
    """
    Creations de nouvelles colonnes à partir des dates 
    """

    data[new_col] = data[start_col] - data[end_col]

    return data
