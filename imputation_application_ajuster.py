"""
Dans ce fichier, on impute les valeurs manquantes en utilisant XGBoost
"""
#Biblioteques
import pandas as pd
from methode_imputation_fonction import imputation_supervise

#Telecharger le data
data = pd.read_csv("Data_encoder.csv")
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

#Imputation avec XGB
xgb_params={'n_estimators': 500, 'max_depth': 50}
data_imputed_xgboost = imputation_supervise('XGB',data,col_continue,xgb_params=xgb_params)

#Telechargement 
data_imputed_xgboost.to_csv("Data_imptution_xgboost.csv",index=False)
