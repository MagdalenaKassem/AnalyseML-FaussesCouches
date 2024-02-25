'''
En premier lieu, on visualise en utilisant t-sne
Apres on fait du clustering hierarchique
on visualise les scores silhouette
'''
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from visualisation_fonctions_ajuster import tsne_visualization, plot_silhouette_scores
from clustering_fonction import clustering, compute_silhouette_scores


# Load the data
data = pd.read_csv("Data_imptution_xgboost.csv")

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

# Scaler les colonnes continues
scaler=StandardScaler()
data[col_continue]=scaler.fit_transform(data[col_continue])

# Visualisation t-sne
tsne_visualization(data)

# Visualisation t-sne avec clustering hierarchique
labels_data = clustering(data,AgglomerativeClustering,10)
tsne_visualization(data, labels_data,10,n_components=2, random_state=42)

# Visualisation des score silhouette
scores_silhouette = compute_silhouette_scores(data,AgglomerativeClustering,20)
plot_silhouette_scores(scores_silhouette)

