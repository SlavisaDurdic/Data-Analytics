# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES:
# > if only 1 sample in hypothesis testing: 17-20, 34-36 AND 42
# > if 2 samples in hypothesis testing: 17-27, 167-173 AND 179

import time
import os
import csv
from google.cloud import bigquery
import matplotlib.pyplot as plt
import scipy.stats
import statistics as st
import math

start = time.time()

# Provide information for the following items to pull values from BigQuery or CSV files
sample_1_variable = 'Enter your variable name'
data_source_1 = 'Enter a data source'  # Full path of a CSV file or a BigQuery table full name, e.g. 'bigquery-public-data.imdb.title_ratings'
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
    population_mean = 100  # Change the value accordingly
    population_stDev = []  # Put a value in the list if population variance (σ) is known (e.g. [20], if σ is 20); otherwise, leave the list empty

    two_tailed_test = f'H0: {sample_1_variable} = {population_mean} and H1: {sample_1_variable} != {population_mean}'
    left_tailed_test = f'H0: {sample_1_variable} >= {population_mean} and H1: {sample_1_variable} < {population_mean}'
    right_tailed_test = f'H0: {sample_1_variable} <= {population_mean} and H1: {sample_1_variable} > {population_mean}'

    # # According to the above hypothesis definition, make sure to uncomment the valid hypothesis case solely
    hypothesis_testing = two_tailed_test  # Two tailed test
    # # hypothesis_testing = left_tailed_test # Left-sided one-tailed test
    # # hypothesis_testing = right_tailed_test # Right-sided one-tailed test

    print("Hypothesis testing of population mean parameter...")

    if '.csv' not in data_source_1:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'infra-data-391312-15c1b6264ace.json'
        client = bigquery.Client()
        query_job = client.query(sql_query_1)  # API request
        rows = query_job.result()  # Waits for query to finish
        x_values = []
        for row in list(rows):
            x_values.append(row.values())
        x = []
        null_values = 0
        for i in range(len(x_values)):
            if x_values[i] is not None or "None" not in str(x_values[i]):  # Get rid of the NULL values
                x.append(x_values[i][0])  # Index [0] is used to get rid of the brackets in the list
            else:
                null_values = null_values + 1
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
        x = []
        null_values = 0
        for i in range(len(x_values)):
            if x_values[i] is not None or "None" not in str(x_values[i]):  # Get rid of the NULL values
                x.append(int(float(x_values[i])))
            else:
                null_values = null_values + 1

    source_download = time.time()
    print(f"Data download and data cleansing took about {source_download - start} seconds...")
    print(
        f'There is {len(x_values)} of observed data in total, and number of NULL values in the data source equals to {null_values}...')
    print(f'Top x values in the list:{x[0:7]}...')

    x_size = len(x)
    x_mean = sum(x) / x_size
    x_stDev = st.stdev(x)

    t_statistic = round((x_mean - population_mean) / (x_stDev / (x_size ** 0.5)), 2)
    if population_stDev == []:
        Z_statistic = 0
    else:
        Z_statistic = round((x_mean - population_mean) / (population_stDev[0] / (x_size ** 0.5)), 2)

    Z_alpha = scipy.stats.norm.ppf(1 - significance_level / 2)
    Z_alpha_r = scipy.stats.norm.ppf(1 - significance_level)
    Z_alpha_l = scipy.stats.norm.ppf(significance_level)
    t_alpha = scipy.stats.t.ppf(q=1 - significance_level / 2, df=(x_size - 1))
    t_alpha_r = scipy.stats.t.ppf(q=1 - significance_level, df=(x_size - 1))
    t_alpha_l = scipy.stats.t.ppf(q=significance_level, df=(x_size - 1))

    if population_stDev != []:
        print(f"Population standard deviation is known and sample size is {x_size}. Furthermore, if:\n"
              "- sample size is less than 30, but it is normally distributed, or\n"
              "- sample size is 30 or more\n"
              "--> We use Z test (i.e. normal distribution). However, if sample size is less than 30, and the distribution is unknown or not normal"
              ", we need to use non-parametric methods.")
        if hypothesis_testing == two_tailed_test:
            print(
                f"Obviously, this is a two tailed test. Z critical value for the significance level of α/2 = {significance_level / 2} is {Z_alpha}."
                f" Z statistic is {Z_statistic}.")
            if abs(Z_statistic) > Z_alpha:
                print(
                    f"{two_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(
                    f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == left_tailed_test:
            print(
                f"Obviously, this is a left tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_l}."
                f" Z statistic is {Z_statistic}.")
            if Z_statistic < Z_alpha_l:
                print(
                    f"{left_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(
                    f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == right_tailed_test:
            print(
                f"Obviously, this is a right tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_r}."
                f" Z statistic is {Z_statistic}.")
            if Z_statistic > Z_alpha_r:
                print(
                    f"{right_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(
                    f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
    else:
        print(f"Population standard deviation is unknown and sample size is {x_size}. Furthermore, if:\n"
              "- sample size is less than 30, but it is normally distributed, or\n"
              "- sample size is 30 or more\n"
              "--> We use Student t test. However, if sample size is less than 30, and the distribution is unknown or not normal"
              ", we need to use non-parametric methods.")
        if hypothesis_testing == two_tailed_test:
            print(
                f"Obviously, this is a two tailed test. T critical value for the significance level of α/2 = {significance_level / 2} is {t_alpha}."
                f" T statistic is {t_statistic}.")
            if abs(t_statistic) > t_alpha:
                print(
                    f"{two_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(
                    f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == left_tailed_test:
            print(
                f"Obviously, this is a left tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_l}."
                f" T statistic is {t_statistic}.")
            if t_statistic < t_alpha_l:
                print(
                    f"{left_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(
                    f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == right_tailed_test:
            print(
                f"Obviously, this is a right tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_r}."
                f" T statistic is {t_statistic}.")
            if t_statistic > t_alpha_r:
                print(
                    f"{right_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(
                    f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
else:
    print("Testing the mean difference between the two samples...")

    # Provide information for the following items
    significance_level = 0.05  # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
    population_1_mean = 100  # If known, change the value accordingly; otherwise, leave as is
    population_2_mean = 100  # If known, change the value accordingly; otherwise, leave as is
    population_source_1_stDev = []  # Put a value in the list if population variance (σ) is known (e.g. [20], if σ is 20); otherwise, leave the list empty
    population_source_2_stDev = []  # Put a value in the list if population variance (σ) is known (e.g. [20], if σ is 20); otherwise, leave the list empty
    are_samples_independent = True  # True or False
    are_population_variances_equal = True  # True or False

    two_tailed_test = f'H0: μ1-μ2 = 0 (Mean value is the same in both samples) and H1: μ1-μ2 != 0 (Mean value is NOT the same in both samples)'
    left_tailed_test = f'H0: μ1-μ2 >= 0 and H1: μ1-μ2 < 0 (Mean value of sample source 1 is less than mean value of sample source 2)'
    right_tailed_test = f'H0: μ1-μ2 <= 0 and H1: μ1-μ2 > 0 (Mean value of sample source 1 is higher than mean value of sample source 2)'

    # According to the above hypothesis definition, make sure to uncomment the valid hypothesis case solely
    hypothesis_testing = two_tailed_test  # Two tailed test
    # hypothesis_testing = left_tailed_test # Left-sided one-tailed test
    # hypothesis_testing = right_tailed_test # Right-sided one-tailed test

    if '.csv' not in data_source_1 and '.csv' not in data_source_2:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'infra-data-391312-15c1b6264ace.json'
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
        x_1 = []
        null_values_1 = 0
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None or "None" not in str(x_1_values[i]):  # Get rid of the NULL values
                x_1.append(x_1_values[i][0])  # Index [0] is used to get rid of the brackets in the list
            else:
                null_values_1 = null_values_1 + 1
        x_2 = []
        null_values_2 = 0
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None or "None" not in str(x_2_values[i]):  # Get rid of the NULL values
                x_2.append(x_2_values[i][0])  # Index [0] is used to get rid of the brackets in the list
            else:
                null_values_2 = null_values_2 + 1
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
        x_1 = []
        null_values_1 = 0
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None or "None" not in str(x_1_values[i]):  # Get rid of the NULL values
                x_1.append(int(float(x_1_values[i])))
            else:
                null_values_1 = null_values_1 + 1
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
        x_2 = []
        null_values_2 = 0
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None or "None" not in str(x_2_values[i]):  # Get rid of the NULL values
                x_2.append(int(float(x_2_values[i])))
            else:
                null_values_2 = null_values_2 + 1
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
        x_1 = []
        null_values_1 = 0
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None or "None" not in str(x_1_values[i]):  # Get rid of the NULL values
                x_1.append(int(float(x_1_values[i])))
            else:
                null_values_1 = null_values_1 + 1
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'infra-data-391312-15c1b6264ace.json'
        client = bigquery.Client()
        query_job_2 = client.query(sql_query_2)  # API request
        rows_2 = query_job_2.result()  # Waits for query to finish
        x_2_values = []
        for row in list(rows_2):
            x_2_values.append(row.values())
        x_2 = []
        null_values_2 = 0
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None or "None" not in str(x_2_values[i]):  # Get rid of the NULL values
                x_2.append(x_2_values[i][0])  # Index [0] is used to get rid of the brackets in the list
            else:
                null_values_2 = null_values_2 + 1
    if '.csv' not in data_source_1 and '.csv' in data_source_2:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'infra-data-391312-15c1b6264ace.json'
        client = bigquery.Client()
        query_job_1 = client.query(sql_query_1)  # API request
        rows_1 = query_job_1.result()  # Waits for query to finish
        x_1_values = []
        for row in list(rows_1):
            x_1_values.append(row.values())
        x_1 = []
        null_values_1 = 0
        for i in range(len(x_1_values)):
            if x_1_values[i] is not None or "None" not in str(x_1_values[i]):  # Get rid of the NULL values
                x_1.append(x_1_values[i][0])  # Index [0] is used to get rid of the brackets in the list
            else:
                null_values_1 = null_values_1 + 1
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
        x_2 = []
        null_values_2 = 0
        for i in range(len(x_2_values)):
            if x_2_values[i] is not None or "None" not in str(
                    x_2_values[i]):  # Get rid of the NULL values
                x_2.append(int(float(x_2_values[i])))
            else:
                null_values_2 = null_values_2 + 1

    source_download = time.time()
    print(f"Data download and data cleansing took about {source_download - start} seconds...")
    print(
        f'There are {len(x_1_values)} and {len(x_2_values)} of observed data in total in each sample, and number of NULL values in data sources equals to {null_values_1} and {null_values_2}, respectively...')
    print(f'Top x values in both lists:\n{x_1[0:7]}...\n{x_2[0:7]}...')

    x_1_size = len(x_1)
    x_2_size = len(x_2)
    x_1_mean = sum(x_1) / x_1_size
    print(f'Sample 1 mean is {x_1_mean}.')
    x_2_mean = sum(x_2) / x_2_size
    print(f'Sample 2 mean is {x_2_mean}.')
    x_1_stDev = st.stdev(x_1)
    x_2_stDev = st.stdev(x_2)

    if are_samples_independent == True:  # Independent samples
        print("The two samples are independent...")
        if population_source_1_stDev != [] and population_source_2_stDev != []:  # σ1 and σ2 are known
            print(
                f"Population standard deviations are known and sample sizes are {x_1_size} and {x_2_size}. Furthermore, if:\n"
                "- sample size of one or both samples is less than 30, but it is normally distributed, or\n"
                "- sample size is 30 or more\n"
                "--> We use Z test (i.e. normal distribution).")

            st_dev_x_1_2 = ((population_source_1_stDev[0] ** 2) / x_1_size + (
                        population_source_2_stDev[0] ** 2) / x_2_size) ** 0.5
            Z_statistic = round(((x_1_mean - x_2_mean) - (population_1_mean - population_2_mean)) / st_dev_x_1_2, 2)

            Z_alpha = scipy.stats.norm.ppf(1 - significance_level / 2)
            Z_alpha_r = scipy.stats.norm.ppf(1 - significance_level)
            Z_alpha_l = scipy.stats.norm.ppf(significance_level)

            if hypothesis_testing == two_tailed_test:
                print(
                    f"Obviously, this is a two tailed test. Z critical value for the significance level of α/2 = {significance_level / 2} is {Z_alpha}."
                    f" Z statistic is {Z_statistic}.")
                if abs(Z_statistic) > Z_alpha:
                    print(
                        f"{two_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
                else:
                    print(
                        f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
            if hypothesis_testing == left_tailed_test:
                print(
                    f"Obviously, this is a left tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_l}."
                    f" Z statistic is {Z_statistic}.")
                if Z_statistic < Z_alpha_l:
                    print(
                        f"{left_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
                else:
                    print(
                        f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
            if hypothesis_testing == right_tailed_test:
                print(
                    f"Obviously, this is a right tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_r}."
                    f" Z statistic is {Z_statistic}.")
                if Z_statistic > Z_alpha_r:
                    print(
                        f"{right_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
                else:
                    print(
                        f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        else:
            if are_population_variances_equal == True:  # σ1 and σ2 are equal, although NOT known
                print(
                    f"Population standard deviations are unknown and assumed being equal, and sample sizes are {x_1_size} and {x_2_size}. Furthermore, if:\n"
                    "- sample size is less than 30, but it is normally distributed, or\n"
                    "- sample size is 30 or more\n"
                    "--> We use Student t test.")

                # Weighted standard deviation
                Sp = (((x_1_size - 1) * (x_1_stDev ** 2) + (x_2_size - 1) * (x_2_stDev ** 2)) / (
                            x_1_size + x_2_size - 2)) ** 0.5
                # Statistic standard deviation
                Sx_1_2 = Sp * ((1 / x_1_size + 1 / x_2_size) ** 0.5)
                # t statistic
                t_statistic = round(((x_1_mean - x_2_mean) - (population_1_mean - population_2_mean)) / Sx_1_2, 2)

                t_alpha = scipy.stats.t.ppf(q=1 - significance_level / 2, df=(x_1_size + x_2_size - 2))
                t_alpha_r = scipy.stats.t.ppf(q=1 - significance_level, df=(x_1_size + x_2_size - 2))
                t_alpha_l = scipy.stats.t.ppf(q=significance_level, df=(x_1_size + x_2_size - 2))

                if hypothesis_testing == two_tailed_test:
                    print(
                        f"Obviously, this is a two tailed test. T critical value for the significance level of α/2 = {significance_level / 2} is {t_alpha}."
                        f" T statistic is {t_statistic}.")
                    if abs(t_statistic) > t_alpha:
                        print(
                            f"{two_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == left_tailed_test:
                    print(
                        f"Obviously, this is a left tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_l}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic < t_alpha_l:
                        print(
                            f"{left_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == right_tailed_test:
                    print(
                        f"Obviously, this is a right tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_r}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic > t_alpha_r:
                        print(
                            f"{right_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
            else:  # σ1 and σ2 are NOT known, but different
                print(
                    f"Population standard deviations are unknown and assumed being different, and sample sizes are {x_1_size} and {x_2_size}. Furthermore, if:\n"
                    "- sample size is less than 30, but it is normally distributed, or\n"
                    "- sample size is 30 or more\n"
                    "--> We use Student t test.")

                degrees_of_freedom = math.floor(
                    (((x_1_stDev ** 2) / x_1_size + (x_2_stDev ** 2) / x_2_size) ** 2) / (
                            (((x_1_stDev ** 2) / x_1_size) ** 2) / (x_1_size - 1) + (
                            ((x_2_stDev ** 2) / x_2_size) ** 2) / (x_2_size - 1)))
                # Statistic standard deviation
                Sx_1_2 = ((x_1_stDev ** 2) / x_1_size + (x_2_stDev ** 2) / x_2_size) ** 0.5
                t_statistic = round(
                    ((x_1_mean - x_2_mean) - (population_1_mean - population_2_mean)) / Sx_1_2, 2)

                t_alpha = scipy.stats.t.ppf(q=1 - significance_level / 2, df=degrees_of_freedom)
                t_alpha_r = scipy.stats.t.ppf(q=1 - significance_level, df=degrees_of_freedom)
                t_alpha_l = scipy.stats.t.ppf(q=significance_level, df=degrees_of_freedom)

                if hypothesis_testing == two_tailed_test:
                    print(
                        f"Obviously, this is a two tailed test. T critical value for the significance level of α/2 = {significance_level / 2} is {t_alpha}."
                        f" T statistic is {t_statistic}.")
                    if abs(t_statistic) > t_alpha:
                        print(
                            f"{two_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == left_tailed_test:
                    print(
                        f"Obviously, this is a left tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_l}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic < t_alpha_l:
                        print(
                            f"{left_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == right_tailed_test:
                    print(
                        f"Obviously, this is a right tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_r}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic > t_alpha_r:
                        print(
                            f"{right_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
    else:  # Dependent samples
        print("The two samples are dependent...")
        print("TO BE CONTINUED...")

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