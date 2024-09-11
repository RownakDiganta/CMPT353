# Exercise 8
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632

import pandas as pd 
import sys 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def main():
    # reading files 
    labelled_file_name = sys.argv[1]
    unlabelled_file_name  = sys.argv[2]
    monthly_data_labelled = pd.read_csv(labelled_file_name)
    monthly_data_unlabelled = pd.read_csv(unlabelled_file_name)
    
    # Extracting data to train the machine learning model 
    X = monthly_data_labelled[monthly_data_labelled.columns[2:]]
    X = X.values
    #print(X)
    
    y = monthly_data_labelled[monthly_data_labelled.columns[0]]
    y = y.values 
    #print(y)
    
    # Partition your data into training and validation sets using train_test_split.
    X_train, X_valid, y_train, y_valid = train_test_split(X,y) 
    
    # Creating machine learning model 
    
    
    rf_model = RandomForestClassifier(n_estimators= 100, max_depth= 12, min_samples_leaf = 4 )
    #rf_model.fit(X_train,y_train)
    #model_accuracy_score = rf_model.score(X_valid,y_valid)
    #print("The model's accuracy score:", model_accuracy_score)
    
    # Taken inspiration from slides. Topic: Feature Scaling .
    rf_model = make_pipeline(StandardScaler(),RandomForestClassifier(n_estimators= 100, max_depth= 12, min_samples_leaf = 4 ))
    rf_model.fit(X_train,y_train)

    # finding the accuracy score 
    model_accuracy_score = rf_model.score(X_valid,y_valid)
    print("The model's accuracy score:", model_accuracy_score)
    
    # Getting the prediction 
    X_prediction = monthly_data_unlabelled[monthly_data_unlabelled.columns[2:]]
    X_prediction = X_prediction.values

    
    predictions = rf_model.predict(X_prediction)
    #print(predictions)
    pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)
    
    # Answer.txt (hint) 
    #df = pd.DataFrame({'truth': y_valid, 'prediction': rf_model.predict(X_valid)})
    #print(df[df['truth'] != df['prediction']])

if __name__ == '__main__':
    main()