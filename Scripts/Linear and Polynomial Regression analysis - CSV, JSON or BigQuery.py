# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES 16-20 (and line 64 in case of JSON file)

import time
import os
import csv
import json
from google.cloud import bigquery
import numpy
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import r2_score

start = time.time()

# Provide information for the following 4 items (independent, dependent, data_source, sql_query)
independent = 'Enter independent variable name'
dependent = 'Enter dependent variable name'
data_source = 'Enter data source'  # Full path to a CSV, JSON file or a BigQuery table full name, e.g. 'bigquery-public-data.imdb.title_ratings'
# If needed, adjust the query (add WHERE condition for example)
sql_query = (
    f"SELECT {independent}, {dependent} FROM `{data_source}`;"
            )

if '.csv' in data_source:
    data = []
    with open(data_source, 'r') as file:
    # with open(data_source, encoding="latin-1") as file:  # Use this line in case of UnicodeDecodeError
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
    print(
        f'There are {len(independent_var)} of independent variables and {len(dependent_var)} of dependent variables in the file.')
    index_list = []
    for i in range(len(independent_var)):  # Get rid of the NULL and no-numeric values
        try:
            if independent_var[i] is not None and dependent_var[i] is not None:
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
        if independent_var[i] is not None and dependent_var[i] is not None:
            x.append(float(independent_var[i]))
            y.append(float(dependent_var[i]))
    print(f'There are {len(x)} of X and {len(y)} of Y values in the file.')
elif '.json' in data_source:
    with open(data_source, "r") as file:
        data = json.load(file)
    independent_var = []
    dependent_var = []
    for i in range(len(data)):  # Make sure to refer the correct file keys/indexes
        independent_var.append(data[i]["Enter key name"][independent])
        dependent_var.append(data[i]["Enter key name"][dependent])
    print(f'There are {len(independent_var)} of independent variables and {len(dependent_var)} of dependent variables in the file.')
    index_list = []
    for i in range(len(independent_var)):  # Get rid of the NULL and no-numeric values
        try:
            if independent_var[i] is not None and dependent_var[i] is not None:  # Get rid of the NULL values
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
        if independent_var[i] is not None and dependent_var[i] is not None:
            x.append(float(independent_var[i]))
            y.append(float(dependent_var[i]))
    print(f'There are {len(x)} of X and {len(y)} of Y values in the file.')
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
    print(
        f'There are {len(independent_var)} of independent variables and {len(dependent_var)} of dependent variables in the table.')
    index_list = []
    for i in range(len(independent_var)):  # Get rid of the NULL and no-numeric values
        try:
            if independent_var[i] is not None and dependent_var[i] is not None:
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
        if independent_var[i] is not None and dependent_var[i] is not None:
            x.append(float(independent_var[i]))
            y.append(float(dependent_var[i]))
    print(f'There are {len(x)} of X and {len(y)} of Y values for the analysis.')

end = time.time()
print(f"Dependent and independent variables have been fully configured in {end - start} seconds...")

# Set the size of the plotting window.
plt.figure(dpi=128, figsize=(8, 4.5))
# Plot scatter plot
plt.scatter(x, y, c='blue', cmap=plt.cm.Blues, edgecolor='black', s=10)
# Linear trend (function)
slope, intercept, r, p, std_err = stats.linregress(x, y)
def linear_func(x):
  return slope * x + intercept
linear_model = list(map(linear_func, x))
plt.plot(x, linear_model)
# Set chart title and label axes.
if '.csv' or '.json' in data_source:
    plt.title(f"Regression Analysis of\n...{data_source[-30:]} data", fontsize=10)
else:
    plt.title(f"Regression Analysis of\n{data_source} data", fontsize=10)
plt.xlabel(independent, fontsize=16)
plt.ylabel(dependent, fontsize=16)
# Set size of tick labels.
# plt.tick_params(axis='both', which='major', labelsize=16)
print(f"Slope and intercept in the linear function Y=a+bX are: a={intercept}, b={slope}.")
print(f"Linear regression correlation coefficient is {r}.")
print(f"Linear regression coefficient of determination is {r**2}.")
# Polynomial function
polynomial_model = numpy.poly1d(numpy.polyfit(x, y, 3))
polynomial_line = numpy.linspace(int(min(x)), int(max(x)), int(max(y)))
plt.plot(polynomial_line, polynomial_model(polynomial_line))
print(f"Polynomial regression coefficient of determination is {r2_score(y, polynomial_model(x))}.")
# Show all plots
plt.show()
