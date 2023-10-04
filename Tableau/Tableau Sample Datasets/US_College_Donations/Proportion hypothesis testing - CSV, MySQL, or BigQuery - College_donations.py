# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES: 16-31 AND 37
# > if data comes from a CSV file, specify the conditions on lines: 156 AND 174-175

import time
import os
import csv
from google.cloud import bigquery
import mysql.connector as mysql
from mysql.connector import Error
import matplotlib.pyplot as plt
import scipy.stats

start = time.time()

# Provide information for the following items to pull values from BigQuery, MySQL, or CSV files
sample_variable = 'Gift_Amount'
data_source = 'college_donation'  # CSV file full path, MySQL table name, or a BigQuery table full name, e.g. 'bigquery-public-data.imdb.title_ratings'
# If data comes from a MySQL or BigQuery table, adjust below sql queries with appropriate information (e.g. condition in WHERE clause)
sql_query_set = (
    f"SELECT {sample_variable} FROM `{data_source}`"
    f"WHERE Gift_Date LIKE '%2015%';"
            )
sql_query_subset = (
    f"SELECT {sample_variable} FROM `{data_source}`"
    f"WHERE Gift_Allocation = 'Scholarship' AND Gift_Date LIKE '%2015%';"
            )

# Provide information for the following items
significance_level = 0.05  # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
population_p = 0.43  # Change the value accordingly
sample_p = 0  # If known, change the decimal value accordingly, otherwise let the system calculate it for you based on sample data

two_tailed_test = f'H0: p = {population_p} and H1: p != {population_p}'
left_tailed_test = f'H0: p >= {population_p} and H1: p < {population_p}'
right_tailed_test = f'H0: p <= {population_p} and H1: p > {population_p}'

# According to the above hypothesis definition, make sure to uncomment the valid hypothesis case solely
hypothesis_testing = two_tailed_test  # Two tailed test
# hypothesis_testing = left_tailed_test  # Left-sided one-tailed test
# hypothesis_testing = right_tailed_test  # Right-sided one-tailed test

print("Hypothesis testing of population proportion - one sample...")

if '.csv' not in data_source and 'bigquery-public-data' not in data_source:
    print('MySQL is the datasource.')
    try:
        conn = mysql.connect(host='<server_name>', database='<database_name>', user='<username>', password='<password>')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute(sql_query_set)
            sample_set = cursor.fetchall()
            x_set = []
            for row in sample_set:
                x_set.append(row)
            cursor.execute(sql_query_subset)
            sample_subset = cursor.fetchall()
            x_subset = []
            for row in sample_subset:
                x_subset.append(row)
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
    except Error as e:
        print("Error while connecting to or executing MySQL commands", e)
    index_list = []
    for i in range(len(list(x_set))):  # Get rid of the NULL and no-numeric values
        try:
            if x_set[i] is not None:
                float(x_set[i][0][0])
        except ValueError:
            index_list.append(i)
    print(f'There are {len(set(index_list))} invalid points of x_set in the MySQL table.')
    for i in sorted(set(index_list), reverse=True):
        del x_set[i]
    x_set_cleaned = []
    for i in range(len(x_set)):
        if x_set[i] is not None:
            x_set_cleaned.append(float(x_set[i][0]))
    index_list = []
    for i in range(len(list(x_subset))):  # Get rid of the NULL and no-numeric values
        try:
            if x_subset[i] is not None:
                float(x_subset[i][0][0])
        except ValueError:
            index_list.append(i)
    print(f'There are {len(set(index_list))} invalid points of x_subset in the MySQL table.')
    for i in sorted(set(index_list), reverse=True):
        del x_subset[i]
    x = []
    for i in range(len(x_subset)):
        if x_subset[i] is not None:
            x.append(float(x_subset[i][0]))
    if sample_p == 0:
        sample_p = sum(x)/sum(x_set_cleaned)
    else:
        sample_p
elif '.csv' not in data_source and 'bigquery-public-data' in data_source:
    print('BigQuery table is the datasource.')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
    client = bigquery.Client()
    query_job = client.query(sql_query_set)  # API request
    rows = query_job.result()  # Waits for query to finish
    x_set = []
    for row in list(rows):
        x_set.append(row.values())
    index_list = []
    for i in range(len(x_set)):  # Get rid of the NULL and no-numeric values
        try:
            if x_set[i] is not None:
                float(x_set[i])
        except ValueError:
            index_list.append(i)
    print(f'There are {len(set(index_list))} invalid points of x_set in the BigQuery table.')
    for i in sorted(set(index_list), reverse=True):
        del x_set[i]
    x_set_cleaned = []
    for i in range(len(x_set)):
        if x_set[i] is not None:
            x_set_cleaned.append(float(x_set[i]))
    query_job = client.query(sql_query_subset)  # API request
    rows = query_job.result()  # Waits for query to finish
    x_subset = []
    for row in list(rows):
        x_subset.append(row.values())
    index_list = []
    for i in range(len(x_subset)):  # Get rid of the NULL and no-numeric values
        try:
            if x_subset[i] is not None:
                float(x_subset[i])
        except ValueError:
            index_list.append(i)
    print(f'There are {len(set(index_list))} invalid points of x_subset in the BigQuery table.')
    for i in sorted(set(index_list), reverse=True):
        del x_subset[i]
    x = []
    for i in range(len(x_subset)):
        if x_subset[i] is not None:
            x.append(float(x_subset[i]))
    if sample_p == 0:
        sample_p = sum(x)/sum(x_set_cleaned)
    else:
        sample_p
else:
    print('CSV file is the datasource.')
    data = []
    with open(data_source, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            data.append(row)
    columns = data[0]
    file_values = data[1:]
    x_set = []
    for i in range(len(file_values)):
        if file_values[i][columns.index('conditional_attribute_1')] == 'conditional_attribute_1':
            x_set.append(file_values[i][columns.index(sample_variable)])
    index_list = []
    for i in range(len(x_set)):  # Get rid of the NULL and no-numeric values
        try:
            if x_set[i] is not None:
                float(x_set[i])
        except ValueError:
            index_list.append(i)
    print(f'There are {len(set(index_list))} invalid points of x_set in the file.')
    for i in sorted(set(index_list), reverse=True):
        del x_set[i]
    x_set_cleaned = []
    for i in range(len(x_set)):
        if x_set[i] is not None:
            x_set_cleaned.append(float(x_set[i]))
    x_subset = []
    for i in range(len(file_values)):
        if file_values[i][columns.index('conditional_attribute_1')] == 'conditional_attribute_1' \
                and file_values[i][columns.index('conditional_attribute_2')] > 'conditional_attribute_2':
            x_subset.append(file_values[i][columns.index(sample_variable)])
    index_list = []
    for i in range(len(x_subset)):  # Get rid of the NULL and no-numeric values
        try:
            if x_subset[i] is not None:
                float(x_subset[i])
        except ValueError:
            index_list.append(i)
    print(f'There are {len(set(index_list))} invalid points of x_subset in the file.')
    for i in sorted(set(index_list), reverse=True):
        del x_subset[i]
    x = []
    for i in range(len(x_subset)):
        if x_subset[i] is not None:
            x.append(float(x_subset[i]))
    if sample_p == 0:
        sample_p = sum(x)/sum(x_set_cleaned)
    else:
        sample_p
print(f'There are {len(x_set_cleaned)} of x_set values and {len(x)} of x_subset values.')
print(f'Top x_subset values in the list:{x[0:7]}...')

source_download = time.time()
print(f"Data download and data cleansing took about {source_download - start} seconds...")

x_size = len(x_set_cleaned)
if x_size*population_p > 5 and x_size*(1-population_p) > 5:
    print(f'Sample is considered large, since n*p and n*q are {x_size*population_p} and {x_size*(1-population_p)}, respectively, larger than 5...')
else:
    print(
        f'Either n*p or n*q is less than 5, therefore this is not a large sample...')

Z_statistic = round((sample_p-population_p)/(population_p*(1-population_p)/x_size)**0.5, 2)

Z_alpha = scipy.stats.norm.ppf(1 - significance_level/2)
Z_alpha_r = scipy.stats.norm.ppf(1 - significance_level)
Z_alpha_l = scipy.stats.norm.ppf(significance_level)

print(f'Sample p is {sample_p}.')

if hypothesis_testing == two_tailed_test:
    print(f"Obviously, this is a two tailed test. Z critical value for the significance level of α/2 = {significance_level/2} is {Z_alpha}."
          f" Z statistic is {Z_statistic}.")
    if abs(Z_statistic) > Z_alpha:
        print(f"{two_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
    else:
        print(f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
if hypothesis_testing == left_tailed_test:
    print(f"Obviously, this is a left tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_l}."
          f" Z statistic is {Z_statistic}.")
    if Z_statistic < Z_alpha_l:
        print(f"{left_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
    else:
        print(f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
if hypothesis_testing == right_tailed_test:
    print(f"Obviously, this is a right tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_r}."
          f" Z statistic is {Z_statistic}.")
    if Z_statistic > Z_alpha_r:
        print(f"{right_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
    else:
        print(f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")

end = time.time()
print(f"The full script ended in {end - start} seconds...")

# OPTIONAL: Plot a histogram to visualize and confirm if the sample(s) fallows a normal distribution
plt.hist(x_set_cleaned)
plt.hist(x)
plt.show()