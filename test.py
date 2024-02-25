import pandas as pd
from clustering_fonction import clustering, compute_silhouette_scores, create_cluster_data, save_to_excel
from feature_importances_fonction import model_evaluation, train_model, feature_importance_display
from visualisation_fonctions import plot_importances

from sklearn.ensemble import ExtraTreesClassifier

#Load the data
data = pd.read_csv("Data_Imputation_Xgboost.csv")
col_continue = ["Bmi","Antral follicle count ","Tsh_uui_ml","Most recent amh _ng/ml", "Pregnancy n°","Termoftheevent_weeks of amenorrhea", "Age_femme_enceinte","Age_partenaire", "Date_blood_test","Alcohol_nbglasses/day","Ana ratio","Prednisone no=0 , if yes dosage in mg", "Prednisone stop date in weeks of amenorrhea","Hydroxychloroquine stop date in weeks of amenorrhea","Intralipid stop date in weeks of amenorrhea","Adalimumab stop date in weeks of amenorrhea","Delay in conceiving_months"]

# Rename
y = data['Misscarage'].astype(int)
x = data.drop("Misscarage", axis=1)

#Feature importance
classifier, x_test, y_test = train_model(x,y,ExtraTreesClassifier())
model = model_evaluation(x_test,y_test,classifier)
importance, error = feature_importance_display(x,y,classifier)


#Visualisation

plot_importances(importance,error)
