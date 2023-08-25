# The ANOVA test has important assumptions that must be satisfied in order for the associated p-value to be valid.
# 1) The samples are independent.
# 2) Each sample is from a normally distributed population.
# 3) The population standard deviations of the groups are all equal. This property is known as homoscedasticity.

# scipy.stats.f_oneway
# The length of each group must be at least one, and there must be at least one group with length greater than one.
# If these conditions are not satisfied, a warning is generated and (np.nan, np.nan) is returned.
# If all values in each group are identical, and there exist at least two groups with different values, the function generates a warning and returns (np.inf, 0).
# If all values in all groups are the same, function generates a warning and returns (np.nan, np.nan).

# Interpretation of the f_oneway results
# The p value obtained from ANOVA analysis is significant if p_value is less than alpha (=0.05).
# If the p-value is less than alpha (=0.05), we reject the null hypothesis.
# This implies that we have sufficient proof to say that there exists a difference in the mean values.

from scipy.stats import f_oneway
import csv

null_hypothesis = 'H0: μ1 = μ2 = μ3 = … = μk (It implies that the means of all the population are equal.)'
alternative_hypothesis = 'H1: It states that there will be at least one population mean that differs from the rest.'

data = []
with open("Financial Sample.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        data.append(row)
columns = data[0]
# print(columns)
values = data[1:]
# print(values)

products = []
for i in range(len(values)):
    products.append(values[i][2])
product = set(products)
# print(f'All products:{product}.')

amarilla_var = []
carretera_var = []
montana_var = []
paseo_var = []
velo_var = []
vtt_var = []

# Takes profit for each product separately under Government segment
for i in range(len(values)):
    if 'Government'in values[i][0]:
        if 'Amarilla' in values[i][2]:
            amarilla_var.append(values[i][11])
        if 'Carretera' in values[i][2]:
            carretera_var.append(values[i][11])
        if 'Montana' in values[i][2]:
            montana_var.append(values[i][11])
        if 'Paseo' in values[i][2]:
            paseo_var.append(values[i][11])
        if 'Velo' in values[i][2]:
            velo_var.append(values[i][11])
        if 'VTT' in values[i][2]:
            vtt_var.append(values[i][11])

amarilla = []
carretera = []
montana = []
paseo = []
velo = []
vtt = []
# Removing possible nulls and strings prior to conversion to integers
for i in range(len(amarilla_var)):
    if amarilla_var[i] is not None or "None" not in str(amarilla_var[i]):
        amarilla.append(int(float(amarilla_var[i])))
for i in range(len(carretera_var)):
    if carretera_var[i] is not None or "None" not in str(carretera_var[i]):
        carretera.append(int(float(carretera_var[i])))
for i in range(len(montana_var)):
    if montana_var[i] is not None or "None" not in str(montana_var[i]):
        montana.append(int(float(montana_var[i])))
for i in range(len(paseo_var)):
    if paseo_var[i] is not None or "None" not in str(paseo_var[i]):
        paseo.append(int(float(paseo_var[i])))
for i in range(len(velo_var)):
    if velo_var[i] is not None or "None" not in str(velo_var[i]):
        velo.append(int(float(velo_var[i])))
for i in range(len(vtt_var)):
    if vtt_var[i] is not None or "None" not in str(vtt_var[i]):
        vtt.append(int(float(vtt_var[i])))

# Conduct the one-way ANOVA
fvalue, pvalue = f_oneway(amarilla, carretera, montana, paseo, vtt)
print(f'F value is {fvalue}.')
print(f'P value is {pvalue}.')
if pvalue < 0.05:
    print(f'Since p value is less than 0.05, we reject the null hypothesis. This p value implies that we have overall significance, i.e. sufficient proof to say that there exists a difference in population mean values.'
          f' Also, you should compare F statistic with the F critical value (not available in f_oneway) for furhter insights.')
else:
    print(f'Since p value is higher than 0.05, we have no significant results, so we cannot reject the null hypothesis.'
          f' Also, you can ignore F statistic.')