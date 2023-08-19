
import time
import csv
import matplotlib.pyplot as plt
from scipy import stats

start = time.time()

data = []
with open("Financial Sample.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        data.append(row)
columns = data[0]
# print(columns)
values = data[1:]
# print(values)

independent_var = []
dependent_var = []
for i in range(len(values)):
    independent_var.append(values[i][9]) # Taking only values for sales column
    dependent_var.append(values[i][11]) # Taking only values for profit column
print(f'Number of ALL independent values is {len(independent_var)}.')
print(f'Number of ALL dependent values is {len(independent_var)}.')

x = []
y = []
for i in range(len(independent_var)): # Removing nulls and strings prior to conversion to integers
    if independent_var[i] is not None and dependent_var[i] is not None:
        if "None" not in str(independent_var[i]) and "None" not in str(dependent_var[i]):
            x.append(int(float(independent_var[i])))
            y.append(int(float(dependent_var[i])))
print(f'Number of independent integer values is {len(x)}.')
print(f'Number of dependent integer values is {len(y)}.')

# Set the size of the plotting window.
plt.figure(dpi=128, figsize=(8, 4.5))
# Plot scatter plot and the trend
plt.scatter(x, y, c='blue', cmap=plt.cm.Blues, edgecolor='black', s=10)
slope, intercept, r, p, std_err = stats.linregress(x, y)
print(f"Correlation coefficient is {r}")
print(f"Coefficient of determination is {r**2}")
def myfunc(x):
  return slope * x + intercept
mymodel = list(map(myfunc, x))
plt.plot(x, mymodel)
# Set chart title and label axes.
plt.title(f"Regression Analysis of\nPowerBI Financials sample dataset", fontsize=10)
plt.xlabel('Sales', fontsize=16)
plt.ylabel('Profit', fontsize=16)
# Set size of tick labels.
# plt.tick_params(axis='both', which='major', labelsize=16)

end = time.time()
print(f"Dependent and independent variables have been fully configured in {end - start} seconds...")

plt.show()