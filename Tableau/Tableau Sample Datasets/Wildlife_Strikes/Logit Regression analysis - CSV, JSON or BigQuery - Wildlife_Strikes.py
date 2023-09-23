# MAKE SURE TO PROVIDE CORRECT INFO FOR BELOW SPECIFIED LINES:
# - in case of simple logistic regression: 18-22, 68 (if json data file) and 145
# - in case of multivariate logistic regression: 173, 177 and 181

import time
import os
import csv
import json
from google.cloud import bigquery
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

start = time.time()

independent = 'Enter independent variable name'
dependent = 'Enter dependent variable name'
data_source = 'Enter data source' # Full path to a CSV, JSON file or a BigQuery table full name, e.g. 'bigquery-public-data.imdb.title_ratings'
# If needed, adjust the query (add WHERE condition for example)
sql_query = (
    f"SELECT {independent}, {dependent} FROM `{data_source}`;"
            )

if independent != 'Enter independent variable name':
    if '.csv' in data_source:
        data = []
        with open(data_source, 'r') as file:
        # with open(data_source, encoding="latin-1") as file: # Use this line in case of UnicodeDecodeError
            csvreader = csv.reader(file)
            for row in csvreader:
                data.append(row)
        columns = data[0]
        source_values = data[1:]
        independent_var = []
        dependent_var = []
        for i in range(len(source_values)):
            independent_var.append(source_values[i][columns.index(independent)])
            dependent_var.append(source_values[i][columns.index(dependent)])
        print(f'There are {len(independent_var)} of independent variables and {len(dependent_var)} of dependent variables in the file.')
        index_list = []
        for i in range(len(independent_var)): # Get rid of the NULL and no-numeric values
            try:
                if (independent_var[i] is not None and dependent_var[i] is not None):
                    float(independent_var[i])
                    float(dependent_var[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} mismatching points in the file.')
        for i in sorted(set(index_list), reverse=True):
            del independent_var[i]
            del dependent_var[i]
        x = []
        y = []
        for i in range(len(independent_var)):
            if (independent_var[i] is not None and dependent_var[i] is not None):
                x.append(float(independent_var[i]))
                y.append(float(dependent_var[i]))
        print(f'There are {len(x)} of X and {len(y)} of Y values in the file.')
        x = np.array(x).reshape(-1, 1)
        y = np.array(y)
    elif '.json' in data_source:
        with open(data_source, "r") as file:
            data = json.load(file)
        independent_var = []
        dependent_var = []
        for i in range(len(data)): # Make sure to refer the correct file keys/indexes
            independent_var.append(data[i]["fields"][independent])
            dependent_var.append(data[i]["fields"][dependent])
        print(f'There are {len(independent_var)} of independent variables and {len(dependent_var)} of dependent variables in the file.')
        index_list = []
        for i in range(len(independent_var)): # Get rid of the NULL and no-numeric values
            try:
                if (independent_var[i] is not None and dependent_var[i] is not None):
                    float(independent_var[i])
                    float(dependent_var[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} mismatching points in the file.')
        for i in sorted(set(index_list), reverse=True):
            del independent_var[i]
            del dependent_var[i]
        x = []
        y = []
        for i in range(len(independent_var)):
            if (independent_var[i] is not None and dependent_var[i] is not None):
                x.append(float(independent_var[i]))
                y.append(float(dependent_var[i]))
        print(f'There are {len(x)} of X and {len(y)} of Y values in the file.')
        x = np.array(x).reshape(-1, 1)
        y = np.array(y)
    else:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
        client = bigquery.Client()
        query_job = client.query(sql_query)  # API request
        rows = query_job.result()  # Waits for query to finish
        print('Downloading values and populating the lists...')
        columns = []
        source_values = []
        for row in list(rows):
            columns.append(row.keys())
            source_values.append(row.values())
        independent_var = []
        dependent_var = []
        for i in range(len(source_values)):
            independent_var.append(source_values[i][0])
            dependent_var.append(source_values[i][1])
        print(f'There are {len(independent_var)} of independent variables and {len(dependent_var)} of dependent variables in the file.')
        index_list = []
        for i in range(len(independent_var)): # Get rid of the NULL and no-numeric values
            try:
                if (independent_var[i] is not None and dependent_var[i] is not None):
                    float(independent_var[i])
                    float(dependent_var[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} mismatching points between the columns in the BigQuery table.')
        for i in sorted(set(index_list), reverse=True):
            del independent_var[i]
            del dependent_var[i]
        x = []
        y = []
        for i in range(len(independent_var)):
            if (independent_var[i] is not None and dependent_var[i] is not None):
                x.append(float(independent_var[i]))
                y.append(float(dependent_var[i]))
        print(f'There are {len(x)} of X and {len(y)} of Y values for the analysis.')
        x = np.array(x).reshape(-1, 1)
        y = np.array(y)

    log_reg = LogisticRegression()
    log_reg.fit(x, y)

    def logit_prob(log_reg, X):
      log_odds = log_reg.coef_ * X + log_reg.intercept_
      odds = np.exp(log_odds)
      probability = odds / (1 + odds)
      return(probability)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)
    # Predicting the output with certain input assumptions
    x_input = 6000  # Change the value accordingly
    predicted_y = log_reg.predict(np.array(x_input).reshape(-1, 1))[0]
    print(
        f'Predicted value for x = {x_input} is {predicted_y}.'
        f'Probability that output will be 1 for x = {x_input} is {logit_prob(log_reg, x_input)[0]}.')  # Alternatively, "LogisticRegression().predict_proba" method can be used
    # Scoring the model (returns the mean accuracy on the given test data and labels)
    print(f'Accuracy of the model is {log_reg.score(X_test, y_test)}.')

    end = time.time()
    print(f"The script ended in {end - start} seconds...")

    # Set the size of the plotting window.
    plt.figure(dpi=128, figsize=(8, 4.5))
    # Plot scatter plot
    plt.scatter(x, y, marker='+', color='red')
    # Set chart title and label axes.
    if '.csv' or '.json' in data_source:
        plt.title(f"Regression Analysis of\n...{data_source[-30:]} data", fontsize=10)
    else:
        plt.title(f"Regression Analysis of\n{data_source} data", fontsize=10)
    plt.xlabel(independent, fontsize=16)
    plt.ylabel(dependent, fontsize=16)
    # Sigmoid logistic regression function
    x_reshaped = np.linspace(0, max(x)[0]).reshape(-1, 1)
    plt.plot(x_reshaped, logit_prob(log_reg, x_reshaped), c='blue')
    # Show all plots
    plt.show()
else:
    data_source = 'faa_data_subset - logit.csv' # Full path to a CSV file
    data = pd.read_csv(data_source)
    data = pd.get_dummies(data, drop_first=True)
    print(data.columns)
    # print(data.sample(5))
    X_train, X_test, y_train, y_test = train_test_split(data.drop('Indicated Damage', axis=1), data['Indicated Damage'])
    log_reg = LogisticRegression(solver='lbfgs')
    log_reg.fit(X_train, y_train)
    # Predicting the output with certain input assumptions
    # (e.g., Feet above ground = 1800, Miles from airport = 50, Time of day = Day, Animal Category = Birds)
    predicted_y = log_reg.predict(np.array([[1800,50,1,0,0,1,0,0]]))[0]
    print(f'Predicted output for the given parameters is {predicted_y}.')
    print(f'Outcome probabilities for the given parameters: {log_reg.predict_proba(np.array([[1800, 50, 1, 0, 0, 1, 0, 0]]))}.')
    # Scoring the model
    print(f'Accuracy of the model is {log_reg.score(X_test, y_test)}.')

    end = time.time()
    print(f"The script ended in {end - start} seconds...")