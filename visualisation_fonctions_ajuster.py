'''
Ce fichier contient differntes illustrations visuelles.
'''

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE
import seaborn as sns


def plot_silhouette_scores(silhouette_scores):
    """
    Affichr la courbe de score silhouette.
    """
    k_values = list(silhouette_scores.keys())
    scores = list(silhouette_scores.values())

    plt.plot(k_values, scores, marker='o')
    plt.xlabel('Nombre de clusters (k)')
    plt.xticks(k_values)
    plt.ylabel('Score silhouette moyen')
    plt.title('Comparaison des scores silhouette pour différents k')
    plt.show()


def tsne_visualization(data, labels_data=None, n_clusters=None,n_components=2, random_state=42):
    """
    Visualisation de notre data en utilisant t-sne.
    Si on a fait du clustering, on les mets.
    """
    tsne = TSNE(n_components=n_components, random_state=random_state)
    features_tsne = tsne.fit_transform(data)
    
    sns.set(style='white')
    plt.figure(figsize=(10, 6))
    
    if labels_data is not None and n_clusters is not None:
        sns.scatterplot(x=features_tsne[:, 0], y=features_tsne[:, 1], hue=labels_data, palette=sns.color_palette("tab20", n_colors=n_clusters))
    else:
        sns.scatterplot(x=features_tsne[:, 0], y=features_tsne[:, 1])

    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.title("t-SNE visualization")
    plt.legend() 
    plt.show()  


def compare_continious_imputations(original_data, imputed_datasets, continious_columns):
    """
    Cette fonction affiche les histogrammes des distributions des variables continues avant et apres imputation.
    """
    for col in continious_columns:
        plt.figure(figsize=(12, 5 * len(imputed_datasets)))

        # Avant imputation
        plt.subplot(len(imputed_datasets) + 1, 1, 1)
        plt.hist(original_data[col], bins=20, edgecolor='black', alpha=0.5, label='Avant Imputation')
        plt.title(f'{col} - Avant Imputation')
        plt.xlabel(col)
        plt.ylabel('Fréquence')
        plt.legend()

        # Pour chaque méthode d'imputation
        for idx, (method, imputed_data) in enumerate(imputed_datasets.items(), start=2):
            plt.subplot(len(imputed_datasets) + 1, 1, idx)
            plt.hist(imputed_data[col], bins=20, edgecolor='black', alpha=0.5, label=f'Après Imputation {method}')
            plt.title(f'{col} - Après Imputation {method}')
            plt.xlabel(col)
            plt.ylabel('Fréquence')
            plt.legend()

        plt.tight_layout()
        plt.show()


def compare_categorical_imputations(original_data, imputed_data_dict, categorical_columns):
    """
    Même chose mais pour les variables catégorielles.
    """
    for col in categorical_columns:
        if original_data[col].isnull().sum() > 0:
            proportions = {
                "Sans Imputation": original_data[col].value_counts(normalize=True)
            }
            for method_name, imputed_data in imputed_data_dict.items():
                imputed_data[col] = imputed_data[col].astype(int)
                proportions[method_name] = imputed_data[col].value_counts(normalize=True)

            # Créez un dataframe à partir du dictionnaire
            df_proportions = pd.DataFrame(proportions).T.fillna(0)

            # Créez un graphique à barres empilées horizontalement
            df_proportions.plot(kind='barh', stacked=True, figsize=(10, 6), colormap='viridis')

            # Personnalisez le titre, les étiquettes et la légende
            plt.title(f'Distribution des valeurs pour {col}')
            plt.xlabel('Proportion')
            plt.ylabel('Méthode d\'Imputation')
            plt.legend(title="Valeurs", loc='center left', bbox_to_anchor=(1.0, 0.5))
            plt.show()


def plot_importances(importances, errors, title="Feature importances"): 
    """
    Affichage des features qui sont importantes
    """
    _, ax = plt.subplots(figsize=(10, 6))    # pylint: disable=invalid-name
    importances.plot.bar(yerr=errors, ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Mean decrease of accuracy")
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.show()   
         