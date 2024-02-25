import pandas as pd
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier , KNeighborsRegressor
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder

'''
Ce fichier contient les differentes méthodes d'imputation utilisée pour gérer
 les valeurs manquantes.
'''

def imputation_regression(data, col, model, col_continue):
    """
    Cette fonction impute les valeurs manquantes dans les colonnes continues

    """
    data_imputer_cont = data.loc[:, :col]
    data_train = data_imputer_cont[data[col].notnull()]
    X_train = data_train.drop(col, axis=1)
    y_train = data_train[col]

    model.fit(X_train, y_train)

    data_predict = data_imputer_cont[data[col].isnull()]
    x_predict = data_predict.drop(col, axis=1)

    predictions = model.predict(x_predict)
    data.loc[data[col].isnull(), col] = predictions

    for col in col_continue:
        if col != 'Date_blood_test':
            data[col] = data[col].apply(lambda x: max(0, x))

    return data


def imputation_classification(data, col, model, encoder=None):
    """
    Cette fonction impute les valeurs manquantes dans les colonnes catégorielles

    """
    data_imputer_categ = data.loc[:, :col]
    data_train = data_imputer_categ[data[col].notnull()]
    x_train = data_train.drop(col, axis=1)

    if encoder:
        y_train = encoder.fit_transform(data_train[col])
    else:
        y_train = data_train[col]

    model.fit(x_train, y_train)

    data_predict = data_imputer_categ[data[col].isnull()]
    x_predict = data_predict.drop(col, axis=1)

    predictions = model.predict(x_predict)

    if encoder:
        data.loc[data[col].isnull(), col] = encoder.inverse_transform(predictions)
    else:
        data.loc[data[col].isnull(), col] = predictions

    return data


def imputation_supervise(modele, data, col_continue, xgb_params={}, knn_params={}):
    """
    Cette fonction impute les valeurs manquantes en utilisant les 2 fonctions définies préalablement
    """
    colonne_sorted_by_missing = data.isnull().sum().sort_values().index
    data = data[colonne_sorted_by_missing].copy()

    for col in data.columns:
        if data[col].isnull().sum() > 0:
            if col in col_continue:
                if modele == 'XGB':
                    model = XGBRegressor(**xgb_params)
                elif modele == 'KNN':
                    model = KNeighborsRegressor(**knn_params)
                data = imputation_regression(data, col, model, col_continue)
            else:
                if modele == 'XGB':
                    encoder = LabelEncoder()
                    model = XGBClassifier(**xgb_params)
                    data = imputation_classification(data, col, model, encoder)
                elif modele == 'KNN':
                    model = KNeighborsClassifier(**knn_params)
                    data = imputation_classification(data, col, model)

    return data


def imputation_knnimputer(data, imputer_params={}) :
    """
    Imputation en utilisant KNNImputer

    """
    imputer = KNNImputer(**imputer_params)
    data_imputed = imputer.fit_transform(data)
    data_imputed = pd.DataFrame(data_imputed, columns = data.columns)

    return data_imputed


def imputation_naive(data, col_continue) :
    """
    Imputation par la moyenne des variables continues
    Imputation par la valeur la plus fréquentes dans les variables catégorielles

    """
    for col in data.columns :

        if col in col_continue :
            moyenne = data[col].mean()
            data[col].fillna(moyenne, inplace = True)

        else :

            mode = data[col].mode().values[0]
            data[col].fillna(mode, inplace=True)

    return data
