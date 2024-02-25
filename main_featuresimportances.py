'''
Dans ce fichier, nous obtenons les variables importantes sur lesquel on va faire l'analyse
'''
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from feature_importances_fonction import train_model,model_evaluation,feature_importance_display
from visualisation_fonctions_ajuster import  plot_importances

# Load the data 
data = pd.read_csv("Data_imptution_xgboost.csv")

# Division de data
x = data.drop('Miscarriage',axis=1)
y = data['Miscarriage']

# Entrainement du modele
classifier,x_test,y_test = train_model(x,y,ExtraTreesClassifier(n_estimators=1000))

# Evaluation du modele
model_evaluation(x_test,y_test,classifier)

# Feature importance + visualisation
features_important,error =  feature_importance_display(x,y,classifier)
plot_importances(features_important,error)
