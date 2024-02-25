"""
Dans ce fichier, on supprime les textes inutiles en premier lieu.
Deuxiement, on decode les colonnes categorielles dont les cellules contiennent plusieurs categories.
"""

#Librairie
import numpy as np
import pandas as pd
from encodage import (
    duplication, encodage_colonne, replace_nouveau_categorie, 
    fill_based_on_condition_list, replacer_plusieurs_categorie,
    extract_year_from_columns, compute_age_difference
)
from config import (
    valeurs_supprimer,colonnes_supprimer_avant_encodage, 
    colonne_renomer, fill_conditions, replacement_conditions, 
    all_mappings , replacements_manuelle, replacements_pregnancy_complication
)    

#Importation des données et suppression des textes inutiles

data = pd.read_excel('FC.xlsx',sheet_name='Recueil',na_values=valeurs_supprimer)


#Duplication des informations constantes
data = duplication(data,'Patient_Number',2,61)


#Suppression des colonnes inutiles
data = data.drop(colonnes_supprimer_avant_encodage,axis=1)

#Renommer les colonnes pour simplifier
data = data.rename(columns=colonne_renomer)

#Gerer des textes dans quelques colonnes manuellement
data['Miscarriage ou autre'] = data['Miscarriage ou autre'].replace({5:2,"pas de grossesse spontannée obtenue après 6 mois d'Humira":'pas enceinte','GEU':'Autre','GLI':'Autre'})
data['Miscarriage ou autre'] = data.apply(lambda row: 'pas enceinte' if pd.isna(row['Miscarriage ou autre']) and row['Pregnancy_yes1_no0'] == 0 else row['Miscarriage ou autre'], axis=1) 
data['Hydroxychloroquine_No0_pre conception1_during pregnancy2 '] = data['Hydroxychloroquine_No0_pre conception1_during pregnancy2 '].replace({'HCQ / placebo protocole BBQ':0})
data['Deeply infiltrating endometriosis yes1_no2'] = data['Deeply infiltrating endometriosis yes1_no2'].replace({2:0})
data['Oocyte donor_1_sperm donor2_doubledonors3'] = data['Oocyte donor_1_sperm donor2_doubledonors3'].replace({'1 (avec HLA kir compatible)': 1})
data['Nb_emb_transferred'] = data['Nb_emb_transferred'].replace(['0 car hydrosalpinx','0 car qualité pas assez bonne'], 0)
data['Ageofembryo_D3_1_D5_2'] = data['Ageofembryo_D3_1_D5_2'].replace('double tsf J3/J5',2)
data['Pregnancy complications'] = data['Pregnancy complications'].replace(replacements_pregnancy_complication)

#Remplissage des colonnes suivant d'autre colonnes
for condition in fill_conditions:
    data = fill_based_on_condition_list(
        data=data,
        condition_col=condition['condition_col'],
        values=condition['values'],
        target_cols=condition['target_cols'],
        nouvelle_valeur=condition['nouvelle_valeur']
    )

# A ajuster avant de continuer
data ['Pregnancy complications'] = data['Pregnancy complications'].fillna(0)

#Remplissage de tous les textes par une nouvelle categories
data = replace_nouveau_categorie(data,'Conventional antiphospholipid',0,1)

#Remplacer  chaque texte par une categorie spécifique
for condition in replacement_conditions:
    data = replacer_plusieurs_categorie(data, condition['column'], condition['replacement_dict'])

#Encodage des colonnes catégorielles a plusieurs valeurs dans une cellule
for column_name, category_mapping in all_mappings.items():
    data = encodage_colonne(data, column_name, category_mapping)

#Remplissage des valeurs nan par 0 après encodage
colonne_nan_0 = ['Cause_infertility_tubal','Cause_infertitlity_masculine','Cause_infertility_ovarian','Cause_infertility_PCOS',
                 'Cause_infertility_unexplained','Oocyte donor_1_sperm donor2_doubledonors3']
data.loc[:, colonne_nan_0] = data.loc[:, colonne_nan_0].fillna(0)

#Ajustement particulaire a faire
data.loc[data['Patient_Number']==360,['Cause_infertility_tubal','Cause_infertitlity_masculine','Cause_infertility_ovarian',
                                      'Cause_infertility_PCOS','Cause_infertility_unexplained']]=np.nan

# Partner n° (1,2,3..)
data['Partner n° (1,2,3..)'] = data['Partner n° (1,2,3..)'].replace({'Donnneur 1': 1,'Donneur 2 ': 2 ,'Donneur 3': 3 })
groupes = data.groupby('Patient_Number')
valeur_unique = groupes['Partner n° (1,2,3..)'].unique()
nombre_partenaire = valeur_unique.apply(len)
data['Nombre_total_Partner'] = groupes['Patient_Number'].transform(lambda x: nombre_partenaire.loc[x.iloc[0]])
data['Nombre_total_Partner']=data.apply(lambda row: np.nan if row['Patient_Number'] in [96,334]  else row['Nombre_total_Partner'], axis=1)
data['Nombre_total_Partner']=data.apply(lambda row: 3 if row['Patient_Number']==307  else row['Nombre_total_Partner'], axis=1)

#Remplacement manuelle des textes
for col, replace_dict in replacements_manuelle.items():
    data[col] = data[col].replace(replace_dict)

#'Termoftheevent_weeks of amenorrhea
data['Termoftheevent_weeks of amenorrhea']=data['Termoftheevent_weeks of amenorrhea'].astype('float')

#Prednisone stop date in weeks of amenorrhea
data['Prednisone stop date in weeks of amenorrhea'] = data['Prednisone stop date in weeks of amenorrhea'].where(data['Prednisone stop date in weeks of amenorrhea'].astype(str).str.isnumeric(), np.nan)

#Hydroxychloroquine stop date in weeks of amenorrhea
data['Hydroxychloroquine stop date in weeks of amenorrhea'] = data['Hydroxychloroquine stop date in weeks of amenorrhea'].where(data['Hydroxychloroquine stop date in weeks of amenorrhea'].astype(str).str.isnumeric(), np.nan)


#Extractions des informations des dates
col_extraire = ['Date of blood test (month/year)','date of beginning of pregnancy']
data = extract_year_from_columns(data,col_extraire)

#Creation de nouvelles colonnes
data = compute_age_difference(data,'date of beginning of pregnancy','Partner_YearOfBirth','Age_Femme_Enceinte')
data = compute_age_difference(data,'date of beginning of pregnancy','Partner_YearOfBirth','Age_partenaire')
data = compute_age_difference(data,'Date of blood test (month/year)','date of beginning of pregnancy','Duree_Blood_Test')

#Suppression des colonnes inutiles apres encodage
data = data.drop(['Date of blood test (month/year)','date of beginning of pregnancy','Partner_YearOfBirth',
                'date of beginning of pregnancy','Date_of_birth','Partner n° (1,2,3..)','Patient_Number'],axis=1)

#Ajustement des colonnes
data.columns = [col.capitalize() for col in data.columns]

#Telechargement
#data.to_csv("Data_encoder.csv",index=False)