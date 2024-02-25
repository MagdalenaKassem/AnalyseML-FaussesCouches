import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score



def clustering(data, clustering_algorithm, n_clusters):
    """
    Application d un algorithme de clustering.
    Cette fonction ne retourne les labels
    """
    clustering_algorithm.set_params(n_clusters=n_clusters)
    labels_data = clustering_algorithm.fit_predict(data)
    
    return labels_data


def analyse_clusters(data, clustering_algorithm, n_clusters, col_continue, col_categorielle, filename):
   # choix de k
    clustering_algorithm.set_params(n_clusters=n_clusters)
    
    # Appliquez le clustering
    labels_data = clustering_algorithm.fit_predict(data)
    data['cluster'] = labels_data
    
    # Caractéristiques de chaque cluster:
    cluster_stats = {}
    for cluster_id in range(n_clusters):
        cluster_data = data[data['cluster'] == cluster_id].drop('cluster', axis=1)
        
        # Pour les variables continues
        numeric_stats = cluster_data[col_continue].describe().round(2)
        numeric_stats = numeric_stats.loc[['count', 'mean']]
        
        # Pour les variables catégorielles
        cluster_data[col_categorielle] = cluster_data[col_categorielle].astype('category')
        category_counts = cluster_data[col_categorielle].describe()
        category_counts = category_counts.loc[['freq', 'top']]
        
        cluster_stats[cluster_id] = {
            'numeric_stats': numeric_stats,
            'category_counts': category_counts
        }
    
    # Sauvegarde dans Excel
    # pylint: disable=abstract-class-instantiated
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        for cluster_nb, stats in cluster_stats.items():
            numeric_stats = stats['numeric_stats'].T
            category_counts = stats['category_counts'].T
            combined_stats = pd.concat([numeric_stats, category_counts], axis=1)
            combined_stats.to_excel(writer, sheet_name=f'Cluster {cluster_nb}')