# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES 13-16

import time
import os
import csv
from google.cloud import bigquery
import matplotlib.pyplot as plt
from scipy import stats

start = time.time()

# Provide information for the following 4 items (independent, dependent, data_source, db_query)
independent = 'Murder and nonnegligent manslaughter'
dependent = 'Violent crime3'
data_source = 'US_crime.csv' # Full path to a CSV file or a BigQuery table full name, e.g. 'bigquery-public-data.imdb.title_ratings'
db_query = (
    f"SELECT {independent}, {dependent} FROM `{data_source}`;"
            )

if '.csv' in data_source:
    data = []
    with open(data_source, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            data.append(row)
    colName = data[0]
    sqlValues = data[1:]

    independent_var = []
    dependent_var = []
    for i in range(len(sqlValues)):
        independent_var.append(sqlValues[i][colName.index(independent)])
        dependent_var.append(sqlValues[i][colName.index(dependent)])

    x = []
    y = []
    null_values = 0
    for i in range(len(independent_var)):
        if (independent_var[i] is not None or "None" not in str(independent_var[i])) and \
                (dependent_var[i] is not None or "None" not in str(dependent_var[i])):  # Get rid of the NULL values
            x.append(int(independent_var[i]))
            y.append(int(dependent_var[i]))
        else:
            null_values = null_values + 1
    print(f'There are {null_values} non-matching points in the file.')
else:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
    client = bigquery.Client()
    query_job = client.query(db_query)  # API request
    rows = query_job.result()  # Waits for query to finish

    print('Downloading values and populating the lists...')
    colName = []
    sqlValues = []
    for row in list(rows):
        colName.append(row.keys())
        sqlValues.append(row.values())

    independent_var = []
    dependent_var = []
    for i in range(len(sqlValues)):
            independent_var.append(sqlValues[i][0])
            dependent_var.append(sqlValues[i][1])
    x = []
    y = []
    if (independent_var[i] is not None or "None" not in str(independent_var[i])) and (
            dependent_var[i] is not None or "None" not in str(dependent_var[i])):  # Get rid of the NULL values
        x.append(int(independent_var[i]))
        y.append(int(dependent_var[i]))

end = time.time()
print(f"Dependent and independent variables have been fully configured in {end - start} seconds...")

# Set the size of the plotting window.
plt.figure(dpi=128, figsize=(8, 4.5))
# Plot scatter plot and the trend
plt.scatter(x, y, c='blue', cmap=plt.cm.Blues, edgecolor='black', s=10)
slope, intercept, r, p, std_err = stats.linregress(x, y)
def myfunc(x):
  return slope * x + intercept
mymodel = list(map(myfunc, x))
plt.plot(x, mymodel)
# Set chart title and label axes.
if '.csv' in data_source:
    plt.title(f"Regression Analysis of\n...{data_source[-20:]} data", fontsize=10)
else:
    plt.title(f"Regression Analysis of\n{data_source} data", fontsize=10)
plt.xlabel(independent, fontsize=16)
plt.ylabel(dependent, fontsize=16)
# Set size of tick labels.
# plt.tick_params(axis='both', which='major', labelsize=16)
print(f"Correlation coefficient is {r}")
print(f"Coefficient of determination is {r**2}")
plt.show()