'''
Ce fichier contient la méthode utilisé pour déduire les features importances
'''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_auc_score, accuracy_score
from sklearn.inspection import permutation_importance

def train_model(x, y, classifier):   # pylint: disable=invalid-name
    """
    Cette fonction forme le modèle.
    """
    x_train, x_test, y_train, y_test = train_test_split(x, y)   
    classifier.fit(x_train, y_train)
    return classifier, x_test, y_test

def model_evaluation(x_test, y_test, trained_classifier):  # pylint: disable=invalid-name
    """
    Cette fonction évalue le modèle.
    """
    preds = trained_classifier.predict(x_test)

    # Metriques
    conf = pd.DataFrame(confusion_matrix(y_test, preds), index=(0, 1), columns=(0, 1))
    auc = roc_auc_score(y_test, preds)
    acc = accuracy_score(y_test, preds)
    print("Confusion matrix:")
    print(conf)
    print(f"AUC: {auc:.2f}")
    print(f"Accuracy: {acc:.2f}")

# pylint: disable=too-many-arguments
def feature_importance_display(x, y, trained_classifier, n_important_features=20, n_repeats=10, random_state=42, n_jobs=-1):  # pylint: disable=invalid-name 
    """
    Dans cette fonction, on utilise la méthode permutation_importance.
    On a les features importances avec cette fonction.
    """
    result = permutation_importance(trained_classifier, x, y, n_repeats=n_repeats, random_state=random_state, n_jobs=n_jobs)
    forest_importances = pd.Series(result.importances_mean, index=x.columns).sort_values(ascending=False).iloc[:n_important_features]
    yerr = result.importances_std[:n_important_features]

    print(f"Most {n_important_features} important features:")
    for item in forest_importances.index:
        print(item)

    return forest_importances, yerr
