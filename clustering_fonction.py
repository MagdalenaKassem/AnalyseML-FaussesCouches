'''
Ce fichier contient l'analyse des clusters.
'''

import pandas as pd
from sklearn.metrics import silhouette_score


def clustering(data, clustering_algorithm, n_clusters):
    """
    Application d un algorithme de clustering.
    Cette fonction ne retourne les labels
    """
    cluster_instance = clustering_algorithm()
    cluster_instance.set_params(n_clusters=n_clusters)
    labels_data = cluster_instance.fit_predict(data)
    score = silhouette_score(data, labels_data)    
    print(f"Silhouette Score: {score}")    
    return labels_data
    

def compute_silhouette_scores(data, clustering_algorithm, max_k):
    """
    Calculer les scores silhouette pour une plage de k.
    Cette fonction retourne une liste des scores silhouette pour chaque k de 2 à max_k.
    """
    silhouette_scores = {}    
    for k in range(2, max_k+1):
        labels = clustering(data, clustering_algorithm, k)
        score = silhouette_score(data, labels)
        silhouette_scores[k] = score       
    return silhouette_scores


def compute_cluster_stats(cluster_data, col_continue, col_categorielle):
    """
    Calcul des statistique pour un cluster.
    Premierement on fait pour les variables continues, apres pour les catégorielles.
    """
    numeric_stats = cluster_data[col_continue].describe().round(2)
    numeric_stats = numeric_stats.loc[['count', 'mean']]     
    cluster_data[col_categorielle] = cluster_data[col_categorielle].astype('category')
    category_counts = cluster_data[col_categorielle].describe()
    category_counts = category_counts.loc[['freq', 'top']]    
    return {
        'numeric_stats': numeric_stats,
        'category_counts': category_counts
    }


def create_cluster_data(data, clustering_algorithm, n_clusters, col_continue, col_categorielle):
    """
    On applique la fonction precedente a un cas de clustering précis.
    On regroupe les caracteristiques des clusters obtenus.
    """
    data['cluster'] = clustering(data, clustering_algorithm, n_clusters)   
    cluster_stats = {}
    for cluster_id in range(n_clusters):
        cluster_data = data[data['cluster'] == cluster_id].drop('cluster', axis=1)
        cluster_stats[cluster_id] = compute_cluster_stats(cluster_data, col_continue, col_categorielle)    
    return cluster_stats


def save_to_excel(cluster_stats, filename):
    """Telechargement des résultats des clusters."""
    # pylint: disable=abstract-class-instantiated
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for cluster_nb, stats in cluster_stats.items():
            numeric_stats = stats['numeric_stats'].T
            category_counts = stats['category_counts'].T
            combined_stats = pd.concat([numeric_stats, category_counts], axis=1)
            combined_stats.to_excel(writer, sheet_name=f'Cluster {cluster_nb}')

