# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES 16-19

import time
import os
from google.cloud import bigquery
import matplotlib.pyplot as plt
from scipy import stats

start = time.time()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'

client = bigquery.Client()

# Provide information for the following 4 items (independent, dependent, query_source, db_query) to pull values from BigQuery
independent = 'confirmed_cases'
dependent = 'deaths'
query_source = 'bigquery-public-data.covid19_usafacts.summary'
db_query = (
    f"SELECT {independent}, {dependent} FROM `{query_source}` WHERE date = '2023-05-29';"
            )

query_job = client.query(db_query)  # API request
rows = query_job.result()  # Waits for query to finish

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
for i in range(len(independent_var)):
    x.append(int(independent_var[i]))
y = []
for i in range(len(dependent_var)):
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
plt.title(f"Regression Analysis of\n{query_source} data", fontsize=10)
plt.xlabel(independent, fontsize=16)
plt.ylabel(dependent, fontsize=16)
# Set size of tick labels.
# plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()

print(f"Correlation coefficient is {r}")
print(f"Coefficient of determination is {r**2}")
