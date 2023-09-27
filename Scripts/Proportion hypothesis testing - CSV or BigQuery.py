# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES:
# > if only 1 sample in hypothesis testing: 15-18, 32-34 AND 40
# > if 2 samples in hypothesis testing: 15-25, 138-142 AND 148

import time
import os
import csv
from google.cloud import bigquery
import matplotlib.pyplot as plt
import scipy.stats

start = time.time()

# Provide information for the following items to pull values from BigQuery or CSV files
sample_1_variable = 'Enter your variable name'
data_source_1 = 'Enter a data source'  # CSV file full path or a BigQuery table full name, e.g. 'bigquery-public-data.imdb.title_ratings'
# If needed, adjust the sql query with additional information (e.g. condition in WHERE clause)
sql_query_1 = (
    f"SELECT {sample_1_variable} FROM `{data_source_1}`"
    # f"LIMIT 10000;"
            )
sample_2_variable = 'Enter your variable name'  # If there is no another sample, leave as is
data_source_2 = 'Enter a data source'  # If there is no another sample, leave as is
# If needed, adjust the sql query with additional information (e.g. condition in WHERE clause)
sql_query_2 = (
    f"SELECT {sample_2_variable} FROM `{data_source_2}`;"
            )

if data_source_2 == 'Enter a data source':

    # Provide information for the following items
    significance_level = 0.05  # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
    population_p = 0.7  # Change the value accordingly
    sample_p = 0.66  # Change the value accordingly

    two_tailed_test = f'H0: p = {population_p} and H1: p != {population_p}'
    left_tailed_test = f'H0: p >= {population_p} and H1: p < {population_p}'
    right_tailed_test = f'H0: p <= {population_p} and H1: p > {population_p}'

    # According to the above hypothesis definition, make sure to uncomment the valid hypothesis case solely
    hypothesis_testing = two_tailed_test  # Two tailed test
    # hypothesis_testing = left_tailed_test  # Left-sided one-tailed test
    # hypothesis_testing = right_tailed_test  # Right-sided one-tailed test

    print("Hypothesis testing of population proportion...")

    if '.csv' not in data_source_1:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
        client = bigquery.Client()
        query_job = client.query(sql_query_1)  # API request
        rows = query_job.result()  # Waits for query to finish
        x_values = []
        for row in list(rows):
            x_values.append(row.values())
        index_list = []
        for i in range(len(x_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_values[i] is not None:
                    float(x_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the BigQuery table.')
        for i in sorted(set(index_list), reverse=True):
            del x_values[i]
        x = []
        for i in range(len(x_values)):
            if x_values[i] is not None:
                x.append(float(x_values[i]))
    else:
        data = []
        with open(data_source_1, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                data.append(row)
        columns = data[0]
        file_values = data[1:]
        x_values = []
        for i in range(len(file_values)):
            x_values.append(file_values[i][columns.index(sample_1_variable)])
        index_list = []
        for i in range(len(x_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_values[i] is not None:
                    float(x_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the file.')
        for i in sorted(set(index_list), reverse=True):
            del x_values[i]
        x = []
        for i in range(len(x_values)):
            if x_values[i] is not None:
                x.append(float(x_values[i]))
    print(f'There are {len(x)} of relevant X values for the analysis.')
    print(f'Top X values in the list:{x[0:7]}...')

    source_download = time.time()
    print(f"Data download and data cleansing took about {source_download - start} seconds...")

    x_size = len(x)
    if x_size*population_p > 5 and x_size*(1-population_p) > 5:
        print(f'Sample is considered large, since n*p and n*q are {x_size*population_p} and {x_size*(1-population_p)}, respectively, larger than 5...')
    else:
        print(
            f'Either n*p or n*q is less than 5, therefore this is not a large sample...')

    Z_statistic = round((sample_p-population_p)/(population_p*(1-population_p)/x_size)**0.5, 2)

    Z_alpha = scipy.stats.norm.ppf(1 - significance_level/2)
    Z_alpha_r = scipy.stats.norm.ppf(1 - significance_level)
    Z_alpha_l = scipy.stats.norm.ppf(significance_level)

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
else:
    print("Testing the proportion difference of two populations based on large and independent samples...")

    # Provide information for the following items
    significance_level = 0.05  # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
    population_1_p = 0.7  # Change the value accordingly
    sample_1_p = 0.66  # Change the value accordingly
    population_2_p = 0.7  # Change the value accordingly
    sample_2_p = 0.66  # Change the value accordingly

    two_tailed_test = 'H0: p1 - p2 = 0 and H1: p1 - p2 != 0'
    left_tailed_test = 'H0: p1 - p2 >= 0 and H1: p1 - p2 < 0'
    right_tailed_test = 'H0: p1 - p2 <= 0 and H1: p1 - p2 > 0'

    # According to the above hypothesis definition, make sure to uncomment the valid hypothesis case solely
    hypothesis_testing = two_tailed_test  # Two tailed test
    # hypothesis_testing = left_tailed_test  # Left-sided one-tailed test
    # hypothesis_testing = right_tailed_test  # Right-sided one-tailed test

    if '.csv' not in data_source_1 and '.csv' not in data_source_2:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
        client = bigquery.Client()
        query_job_1 = client.query(sql_query_1)  # API request
        query_job_2 = client.query(sql_query_2)  # API request
        rows_1 = query_job_1.result()  # Waits for query to finish
        rows_2 = query_job_2.result()  # Waits for query to finish
        x_1_values = []
        x_2_values = []
        for row in list(rows_1):
            x_1_values.append(row.values())
        for row in list(rows_2):
            x_2_values.append(row.values())
        index_list = []
        for i in range(len(x_1_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_1_values[i] is not None:
                    float(x_1_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the table.')
        for i in sorted(set(index_list), reverse=True):
            del x_1_values[i]
        x_1 = []
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None:
                x_1.append(float(x_1_values[i]))
        index_list = []
        for i in range(len(x_2_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_2_values[i] is not None:
                    float(x_2_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the table.')
        for i in sorted(set(index_list), reverse=True):
            del x_2_values[i]
        x_2 = []
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None:
                x_2.append(float(x_2_values[i]))
    if '.csv' in data_source_1 and '.csv' in data_source_2:
        data_1 = []
        with open(data_source_1, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                data_1.append(row)
        columns_1 = data_1[0]
        file_1_values = data_1[1:]
        x_1_values = []
        for i in range(len(file_1_values)):
            x_1_values.append(file_1_values[i][columns_1.index(sample_1_variable)])
        index_list = []
        for i in range(len(x_1_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_1_values[i] is not None:
                    float(x_1_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the file.')
        for i in sorted(set(index_list), reverse=True):
            del x_1_values[i]
        x_1 = []
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None:
                x_1.append(float(x_1_values[i]))
        data_2 = []
        with open(data_source_2, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                data_2.append(row)
        columns_2 = data_2[0]
        file_2_values = data_2[1:]
        x_2_values = []
        for i in range(len(file_2_values)):
            x_2_values.append(file_2_values[i][columns_2.index(sample_2_variable)])
        index_list = []
        for i in range(len(x_2_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_2_values[i] is not None:
                    float(x_2_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the file.')
        for i in sorted(set(index_list), reverse=True):
            del x_2_values[i]
        x_2 = []
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None:
                x_2.append(float(x_2_values[i]))
    if '.csv' in data_source_1 and '.csv' not in data_source_2:
        data_1 = []
        with open(data_source_1, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                data_1.append(row)
        columns_1 = data_1[0]
        file_1_values = data_1[1:]
        x_1_values = []
        for i in range(len(file_1_values)):
            x_1_values.append(file_1_values[i][columns_1.index(sample_1_variable)])
        index_list = []
        for i in range(len(x_1_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_1_values[i] is not None:
                    float(x_1_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the file.')
        for i in sorted(set(index_list), reverse=True):
            del x_1_values[i]
        x_1 = []
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None:
                x_1.append(float(x_1_values[i]))
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
        client = bigquery.Client()
        query_job_2 = client.query(sql_query_2)  # API request
        rows_2 = query_job_2.result()  # Waits for query to finish
        x_2_values = []
        for row in list(rows_2):
            x_2_values.append(row.values())
        index_list = []
        for i in range(len(x_2_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_2_values[i] is not None:
                    float(x_2_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the table.')
        for i in sorted(set(index_list), reverse=True):
            del x_2_values[i]
        x_2 = []
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None:
                x_2.append(float(x_2_values[i]))
    if '.csv' not in data_source_1 and '.csv' in data_source_2:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
        client = bigquery.Client()
        query_job_1 = client.query(sql_query_1)  # API request
        rows_1 = query_job_1.result()  # Waits for query to finish
        x_1_values = []
        for row in list(rows_1):
            x_1_values.append(row.values())
        index_list = []
        for i in range(len(x_1_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_1_values[i] is not None:
                    float(x_1_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the table.')
        for i in sorted(set(index_list), reverse=True):
            del x_1_values[i]
        x_1 = []
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None:
                x_1.append(float(x_1_values[i]))
        data_2 = []
        with open(data_source_2, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                data_2.append(row)
        columns_2 = data_2[0]
        file_2_values = data_2[1:]
        x_2_values = []
        for i in range(len(file_2_values)):
            x_2_values.append(file_2_values[i][columns_2.index(sample_2_variable)])
        index_list = []
        for i in range(len(x_2_values)):  # Get rid of the NULL and no-numeric values
            try:
                if x_2_values[i] is not None:
                    float(x_2_values[i])
            except ValueError:
                index_list.append(i)
        print(f'There are {len(set(index_list))} invalid points in the file.')
        for i in sorted(set(index_list), reverse=True):
            del x_2_values[i]
        x_2 = []
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None:
                x_2.append(float(x_2_values[i]))
    print(f'There are {len(x_1)} and {len(x_2)} of relevant X values for the analysis.')
    print(f'Top X values in both lists:\n{x_1[0:7]}...\n{x_2[0:7]}...')

    source_download = time.time()
    print(f"Data download and data cleansing took about {source_download - start} seconds...")

    x_1_size = len(x_1)
    x_2_size = len(x_2)
    if x_1_size*population_1_p > 5 and x_1_size*(1-population_1_p) > 5 and x_2_size*population_2_p > 5 and x_2_size*(1-population_2_p) > 5:
        print(f'Samples are considered large, since all n*p and n*q ({x_1_size*population_1_p, x_1_size*(1-population_1_p),x_2_size*population_2_p, x_2_size*(1-population_2_p)}) are larger than 5...')
    else:
        print(f'At least one of n*p or n*q ({x_1_size*population_1_p, x_1_size*(1-population_1_p),x_2_size*population_2_p, x_2_size*(1-population_2_p)}) is less than 5, therefore this is not the case with large samples...')

    Z_statistic = round(((sample_1_p-sample_2_p)-(population_1_p-population_2_p))/(population_1_p*(1-population_1_p)/x_1_size + population_2_p*(1-population_2_p)/x_2_size)**0.5, 2)

    Z_alpha = scipy.stats.norm.ppf(1 - significance_level/2)
    Z_alpha_r = scipy.stats.norm.ppf(1 - significance_level)
    Z_alpha_l = scipy.stats.norm.ppf(significance_level)

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
if data_source_2 == 'Enter a data source':
    plt.hist(x)
    plt.show()
else:
    plt.hist(x_1)
    plt.hist(x_2)
    plt.show()
