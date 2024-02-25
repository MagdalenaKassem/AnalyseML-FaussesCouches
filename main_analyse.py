'''
Dans ce fichier, nous enregistrons des caracteristique pour chaque cluster
'''
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from clustering_fonction import create_cluster_data, save_to_excel

# Load the data 
data = pd.read_csv("Data_imptution_xgboost.csv")

# Variables importantes (a changer si besoin)
top = [
    "Pregnancy_yes1_no0", 
    "Termoftheevent_weeks of amenorrhea",   
    "Ethnicity_europe",
    "Northafrica",
    "Sub_saharan_africa",
    "Overseas_france_south_america",
    "Asia",
    "Fœtal_death",
    'Hypertension',
    "Retroplacental_hemorrhage",
    "Gesta_diab",
    "Oligohydramnios",
    "Hyperemesis_gravidarum",
    "Pee",
    "Intrauterine_growth_restriction",
    "Autre_complication",
    "Pas_de_complications", 
    "Age_femme_enceinte", 
    "Bmi",
    "Tobacco during pregnancy1_yes_0_no",
    'Endometriosis no 0_yes1',
    'Hysteroscopy_normal0_minor conditions (synechias, polyp, uterine septum ..)1_major conditions 2',
    'Seminogram normal0_abormal1',
    "Miscarriage",
    "Livebirth",
    "Abortion",
    "Termination",
    "Autre_methode",
    'Pcos_yes1_no0'

]
data = data[top]

# Colonne continue qui m'interesse
col_continue = ['Termoftheevent_weeks of amenorrhea','Age_femme_enceinte','Bmi']
col_categorielle = data.drop(col_continue,axis=1).columns

#Scaler les variables continues
scaler = StandardScaler()
data[col_continue] = scaler.fit_transform(data[col_continue])

# Statistique sur les clusters
cluster_stat = create_cluster_data(data,AgglomerativeClustering,10,col_continue,col_categorielle)

# Telechargement du fichier
save_to_excel(cluster_stat,"Analyse_clusters.xlsx")
