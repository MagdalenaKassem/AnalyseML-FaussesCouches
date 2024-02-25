'''
Dans ce fichier, nous visualisations la distribution des variables avant et apres imputation
'''
import pandas as pd
from visualisation_fonctions_ajuster import compare_continious_imputations,compare_categorical_imputations

# Load the data 
data = pd.read_csv("Data_encoder.csv")
data_xgboost = pd.read_csv("Data_imptution_xgboost.csv").reindex(columns=data.columns)

# Colonne continue
col_continue=[
    'Bmi','Antral follicle count ','Tsh_uui_ml',
    'Most recent amh _ng/ml', 
    'Pregnancy n°','Termoftheevent_weeks of amenorrhea', 
    'Age_femme_enceinte',
    'Age_partenaire', 'Duree_blood_test',
    'Alcohol_nbglasses/day','Ana ratio',
    'Prednisone no=0 , if yes dosage in mg',
    'Prednisone stop date in weeks of amenorrhea',
    'Hydroxychloroquine stop date in weeks of amenorrhea',
    'Intralipid stop date in weeks of amenorrhea',
    'Adalimumab stop date in weeks of amenorrhea',
    'Delay in conceiving_months'
]
col_categorielle = data.drop(col_continue,axis=1).columns

# Creation du dictionnaire 
imputed_data_dict = {
    "xgboost": data_xgboost
}

# Visualisation des barplots des variables categorielles
compare_categorical_imputations(data,imputed_data_dict, col_categorielle)

# Visualisation des histogrammes des variables continues
compare_continious_imputations(data,imputed_data_dict,col_continue)
