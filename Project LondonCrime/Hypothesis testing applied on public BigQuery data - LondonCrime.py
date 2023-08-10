# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES:
# > if only 1 sample in hypothesis testing: 16-19, 34-36 AND 42
# > if 2 samples in hypothesis testing: 16-26, 149-155 AND 201

import time
import os
from google.cloud import bigquery
import matplotlib.pyplot as plt
import scipy.stats
import statistics as st
import math

start = time.time()

# Provide information for the following items to pool values from BigQuery
sample_1_variable = 'value'
query_source_1 = 'bigquery-public-data.london_crime.crime_by_lsoa' # A BigQuery table full name, e.g. 'bigquery.imdb.title_ratings'
# If needed, adjust the sql query with additional information (e.g. condition in WHERE clause)
db_query_1 = (
    f"SELECT {sample_1_variable} FROM `{query_source_1}`"
    f"WHERE borough = 'Westminster';"
            )
sample_2_variable = 'value' # If there is no another sample, leave as is
query_source_2 = 'bigquery-public-data.london_crime.crime_by_lsoa'  # If there is no another sample, leave as is
# If needed, adjust the sql query with additional information (e.g. condition in WHERE clause)
db_query_2 = (
    f"SELECT {sample_2_variable} FROM `{query_source_2}` WHERE borough = 'Lambeth';"
            )

if query_source_2 == 'Enter the source table':
    print("Hypothesis testing of population mean parameter...")

    # Provide information for the following items
    significance_level = 0.05 # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
    population_mean = 100 # Change the value accordingly
    population_stDev = [] # Put a value in the list if population variance (σ) is known (e.g. [20], if σ is 20); otherwise, leave the list empty

    two_tailed_test = f'H0: {sample_1_variable} = {population_mean} and H1: {sample_1_variable} != {population_mean}'
    left_tailed_test = f'H0: {sample_1_variable} >= {population_mean} and H1: {sample_1_variable} < {population_mean}'
    right_tailed_test = f'H0: {sample_1_variable} <= {population_mean} and H1: {sample_1_variable} > {population_mean}'

    # According to the above hypothesis definition, make sure to uncomment the valid hypothesis case solely
    hypothesis_testing = two_tailed_test # Two tailed test
    # hypothesis_testing = left_tailed_test # Left-sided one-tailed test
    # hypothesis_testing = right_tailed_test # Right-sided one-tailed test

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
    client = bigquery.Client()
    query_job = client.query(db_query_1)  # API request
    rows = query_job.result()  # Waits for query to finish
    sample_values = []
    for row in list(rows):
        sample_values.append(row.values())

    x = []
    null_values = 0
    for i in range(len(sample_values)):
        if sample_values[i] is not None:
            if "None" not in str(sample_values[i]): # Get rid of the NULL values
                x.append(sample_values[i][0]) # Get rid of the brackets in the list
            else:
                null_values = null_values + 1
        else:
            null_values = null_values + 1

    source_download = time.time()
    print(f"Data download and data cleansing took about {source_download - start} seconds...")
    print(
        f'There is {len(sample_values)} of sample data in total, and number of NULL values equals to {null_values}...')

    sample_size = len(x)
    sample_mean = sum(x)/sample_size
    sample_stDev = st.stdev(x)

    t_statistic = round((sample_mean - population_mean) / (sample_stDev / (sample_size ** 0.5)), 2)
    if population_stDev == []:
        Z_statistic = 0
    else:
        Z_statistic = round((sample_mean-population_mean)/(population_stDev[0]/(sample_size**0.5)),2)

    Z_alpha = scipy.stats.norm.ppf(1 - significance_level/2)
    Z_alpha_r = scipy.stats.norm.ppf(1 - significance_level)
    Z_alpha_l = scipy.stats.norm.ppf(significance_level)
    t_alpha = scipy.stats.t.ppf(q=1-significance_level/2,df=(sample_size-1))
    t_alpha_r = scipy.stats.t.ppf(q=1-significance_level,df=(sample_size-1))
    t_alpha_l = scipy.stats.t.ppf(q=significance_level,df=(sample_size-1))

    if population_stDev != []:
        print(f"Population standard deviation is known and sample size is {sample_size}. Furthermore, if:\n"
              "- sample size is less than 30, but it is normally distributed, or\n"
              "- sample size is 30 or more\n"
              "--> We use Z test (i.e. normal distribution). However, if sample size is less than 30, and the distribution is unknown or not normal"
              ", we need to use non-parametric methods.")
        if hypothesis_testing == two_tailed_test:
            print(f"Obviously, this is a two tailed test. Z critical value for the significance level of α/2 = {significance_level/2} is {Z_alpha}."
                  f" Z statistic is {Z_statistic} = ({sample_mean}-{population_mean})/({population_stDev[0]}/{sample_size}**0.5).")
            if abs(Z_statistic) > Z_alpha:
                print(f"{two_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == left_tailed_test:
            print(f"Obviously, this is a left tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_l}."
                  f" Z statistic is {Z_statistic} = ({sample_mean}-{population_mean})/({population_stDev[0]}/{sample_size}**0.5).")
            if Z_statistic < Z_alpha_l:
                print(f"{left_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == right_tailed_test:
            print(f"Obviously, this is a right tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_r}."
                  f" Z statistic is {Z_statistic} = ({sample_mean}-{population_mean})/({population_stDev[0]}/{sample_size}**0.5).")
            if Z_statistic > Z_alpha_r:
                print(f"{right_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
    else:
        print(f"Population standard deviation is unknown and sample size is {sample_size}. Furthermore, if:\n"
              "- sample size is less than 30, but it is normally distributed, or\n"
              "- sample size is 30 or more\n"
              "--> We use Student t test. However, if sample size is less than 30, and the distribution is unknown or not normal"
              ", we need to use non-parametric methods.")
        if hypothesis_testing == two_tailed_test:
            print(
                f"Obviously, this is a two tailed test. T critical value for the significance level of α/2 = {significance_level/2} is {t_alpha}."
                f" T statistic is {t_statistic} = ({sample_mean}-{population_mean})/({sample_stDev}/{sample_size}**0.5).")
            if abs(t_statistic) > t_alpha:
                print(f"{two_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == left_tailed_test:
            print(
                f"Obviously, this is a left tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_l}."
                f" T statistic is {t_statistic} = ({sample_mean}-{population_mean})/({sample_stDev}/{sample_size}**0.5).")
            if t_statistic < t_alpha_l:
                print(f"{left_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == right_tailed_test:
            print(
                f"Obviously, this is a right tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_r}."
                f" T statistic is {t_statistic} = ({sample_mean}-{population_mean})/({sample_stDev}/{sample_size}**0.5).")
            if t_statistic > t_alpha_r:
                print(f"{right_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
            else:
                print(f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
else:
    print("Testing the mean difference between the two samples...")

    # Provide information for the following items
    significance_level = 0.05  # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
    population_1_mean = 100 # If known, change the value accordingly; otherwise, leave as is
    population_2_mean = 100 # If known, change the value accordingly; otherwise, leave as is
    population_source_1_stDev = []  # Put a value in the list if population variance (σ) is known (e.g. [20], if σ is 20); otherwise, leave the list empty
    population_source_2_stDev = []  # Put a value in the list if population variance (σ) is known (e.g. [20], if σ is 20); otherwise, leave the list empty
    are_samples_independent = True # True or False
    are_σs_equal = True # True or False

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'
    client = bigquery.Client()
    query_job_1 = client.query(db_query_1)  # API request
    query_job_2 = client.query(db_query_2)  # API request
    rows_1 = query_job_1.result()  # Waits for query to finish
    rows_2 = query_job_2.result()  # Waits for query to finish
    sample_values_1 = []
    sample_values_2 = []
    for row in list(rows_1):
        sample_values_1.append(row.values())
    for row in list(rows_2):
        sample_values_2.append(row.values())

    x_1 = []
    null_values_1 = 0
    for i in range(len(sample_values_1)):
        if sample_values_1[i] is not None:
            if "None" not in str(sample_values_1[i]):  # Get rid of the NULL values
                x_1.append(sample_values_1[i][0])  # Get rid of the brackets in the list
            else:
                null_values_1 = null_values_1 + 1
        else:
            null_values_1 = null_values_1 + 1
    x_2 = []
    null_values_2 = 0
    for i in range(len(sample_values_2)):
        if sample_values_2[i] is not None:
            if "None" not in str(sample_values_2[i]):  # Get rid of the NULL values
                x_2.append(sample_values_2[i][0])  # Get rid of the brackets in the list
            else:
                null_values_2 = null_values_2 + 1
        else:
            null_values_2 = null_values_2 + 1

    source_download = time.time()
    print(f"Data download and data cleansing took about {source_download - start} seconds...")
    print(
        f'There is {len(sample_values_1)} and {len(sample_values_2)} of data points in each sample, '
        f'and number of NULL values equals to {null_values_1} and {null_values_2}, respectively...')

    two_tailed_test = f'H0: μ1-μ2 = 0 (Mean value is the same in both samples) and H1: μ1-μ2 != 0 (Mean value is NOT the same in both samples)'
    left_tailed_test = f'H0: μ1-μ2 >= 0 and H1: μ1-μ2 < 0 (Mean value of sample source 1 is less than mean value of sample source 2)'
    right_tailed_test = f'H0: μ1-μ2 <= 0 and H1: μ1-μ2 > 0 (Mean value of sample source 1 is higher than mean value of sample source 2)'

    # According to the above hypothesis definition, make sure to uncomment the valid hypothesis case solely
    # hypothesis_testing = two_tailed_test  # Two tailed test
    hypothesis_testing = left_tailed_test # Left-sided one-tailed test
    # hypothesis_testing = right_tailed_test # Right-sided one-tailed test

    sample_1_size = len(x_1)
    sample_2_size = len(x_2)
    sample_1_mean = sum(x_1) / sample_1_size
    print(f'Sample 1 mean is {sample_1_mean}.')
    sample_2_mean = sum(x_2) / sample_2_size
    print(f'Sample 2 mean is {sample_2_mean}.')
    sample_1_stDev = st.stdev(x_1)
    sample_2_stDev = st.stdev(x_2)

    if are_samples_independent == True: # Independent samples
        print("The two samples are independent...")
        if population_source_1_stDev != [] and population_source_2_stDev != []: # σ1 and σ2 are known
            print(f"Population standard deviations are known and sample sizes are {sample_1_size} and {sample_2_size}. Furthermore, if:\n"
                  "- sample size of one or both samples is less than 30, but it is normally distributed, or\n"
                  "- sample size is 30 or more\n"
                  "--> We use Z test (i.e. normal distribution).")

            σ_x_1_2 = ((population_source_1_stDev[0] ** 2) / sample_1_size + (population_source_2_stDev[0] ** 2) / sample_2_size) ** 0.5
            Z_statistic = round(((sample_1_mean - sample_2_mean) - (population_1_mean - population_2_mean)) / σ_x_1_2, 2)

            Z_alpha = scipy.stats.norm.ppf(1 - significance_level/2)
            Z_alpha_r = scipy.stats.norm.ppf(1 - significance_level)
            Z_alpha_l = scipy.stats.norm.ppf(significance_level)

            if hypothesis_testing == two_tailed_test:
                print(
                    f"Obviously, this is a two tailed test. Z critical value for the significance level of α/2 = {significance_level / 2} is {Z_alpha}."
                    f" Z statistic is {Z_statistic}.")
                if abs(Z_statistic) > Z_alpha:
                    print(f"{two_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
                else:
                    print(
                        f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
            if hypothesis_testing == left_tailed_test:
                print(
                    f"Obviously, this is a left tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_l}."
                    f" Z statistic is {Z_statistic}.")
                if Z_statistic < Z_alpha_l:
                    print(f"{left_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
                else:
                    print(
                        f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
            if hypothesis_testing == right_tailed_test:
                print(
                    f"Obviously, this is a right tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha_r}."
                    f" Z statistic is {Z_statistic}.")
                if Z_statistic > Z_alpha_r:
                    print(f"{right_tailed_test} -> Since Z statistic falls under the rejection area, the null hypothesis should be rejected.")
                else:
                    print(
                        f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        else:
            if are_σs_equal == True: # σ1 and σ2 are equal, although NOT known
                print(f"Population standard deviations are unknown and equal, and sample sizes are {sample_1_size} and {sample_2_size}. Furthermore, if:\n"
                      "- sample size is less than 30, but it is normally distributed, or\n"
                      "- sample size is 30 or more\n"
                      "--> We use Student t test.")

                # Weighted standard deviation
                Sp = (((sample_1_size - 1) * (sample_1_stDev ** 2) + (sample_2_size - 1) * (sample_2_stDev ** 2)) / (sample_1_size + sample_2_size - 2)) ** 0.5
                # Statistic standard deviation
                Sx_1_2 = Sp * ((1 / sample_1_size + 1 / sample_2_size) ** 0.5)
                # t statistic
                t_statistic = round(((sample_1_mean - sample_2_mean) - (population_1_mean - population_2_mean)) / Sx_1_2, 2)

                t_alpha = scipy.stats.t.ppf(q=1 - significance_level/2, df=(sample_1_size + sample_2_size - 2))
                t_alpha_r = scipy.stats.t.ppf(q=1 - significance_level, df=(sample_1_size + sample_2_size - 2))
                t_alpha_l = scipy.stats.t.ppf(q=significance_level, df=(sample_1_size + sample_2_size - 2))

                if hypothesis_testing == two_tailed_test:
                    print(
                        f"Obviously, this is a two tailed test. T critical value for the significance level of α/2 = {significance_level / 2} is {t_alpha}."
                        f" T statistic is {t_statistic}.")
                    if abs(t_statistic) > t_alpha:
                        print(f"{two_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == left_tailed_test:
                    print(
                        f"Obviously, this is a left tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_l}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic < t_alpha_l:
                        print(f"{left_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == right_tailed_test:
                    print(
                        f"Obviously, this is a right tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_r}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic > t_alpha_r:
                        print(f"{right_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
            else: # σ1 and σ2 are NOT known, but different
                print(
                    f"Population standard deviations are unknown and different, and sample sizes are {sample_1_size} and {sample_2_size}. Furthermore, if:\n"
                    "- sample size is less than 30, but it is normally distributed, or\n"
                    "- sample size is 30 or more\n"
                    "--> We use Student t test.")

                degrees_of_freedom = math.floor(
                    (((sample_1_stDev ** 2) / sample_1_size + (sample_2_stDev ** 2) / sample_2_size) ** 2) / (
                            (((sample_1_stDev ** 2) / sample_1_size) ** 2) / (sample_1_size - 1) + (
                            ((sample_2_stDev ** 2) / sample_2_size) ** 2) / (sample_2_size - 1)))
                # Statistic standard deviation
                Sx_1_2 = ((sample_1_stDev ** 2) / sample_1_size + (sample_2_stDev ** 2) / sample_2_size) ** 0.5
                t_statistic = round(
                    ((sample_1_mean - sample_2_mean) - (population_1_mean - population_2_mean)) / Sx_1_2, 2)

                t_alpha = scipy.stats.t.ppf(q=1 - significance_level/2, df=degrees_of_freedom)
                t_alpha_r = scipy.stats.t.ppf(q=1 - significance_level, df=degrees_of_freedom)
                t_alpha_l = scipy.stats.t.ppf(q=significance_level, df=degrees_of_freedom)

                if hypothesis_testing == two_tailed_test:
                    print(
                        f"Obviously, this is a two tailed test. T critical value for the significance level of α/2 = {significance_level / 2} is {t_alpha}."
                        f" T statistic is {t_statistic}.")
                    if abs(t_statistic) > t_alpha:
                        print(f"{two_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == left_tailed_test:
                    print(
                        f"Obviously, this is a left tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_l}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic < t_alpha_l:
                        print(f"{left_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
                if hypothesis_testing == right_tailed_test:
                    print(
                        f"Obviously, this is a right tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_r}."
                        f" T statistic is {t_statistic}.")
                    if t_statistic > t_alpha_r:
                        print(f"{right_tailed_test} -> Since t statistic falls under the rejection area, the null hypothesis should be rejected.")
                    else:
                        print(
                            f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
    else: # Dependent samples
        print("The two samples are dependent...")
        print("TO BE CONTINUED...")

end = time.time()
print(f"The full script ended in {end - start} seconds...")

# OPTIONAL: Plot a histogram to visualize and confirm if the sample(s) fallows a normal distribution
if query_source_2 == 'Enter the source table':
    plt.hist(x)
    plt.show()
else:
    plt.hist(x_1)
    plt.hist(x_2)
    plt.show()