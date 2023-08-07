# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES 13-20, 26-28, AND 34

import time
import os
from google.cloud import bigquery
import matplotlib.pyplot as plt
import scipy.stats
import statistics as st

start = time.time()

# Provide information for the following items to pool values from BigQuery
sample_variable = 'average_rating'
query_source_1 = 'bigquery-public-data.imdb.title_ratings'
query_source_2 = 'Enter the source table'  # If there is no another sample, leave as is
db_query_1 = (
    f"SELECT {sample_variable} FROM `{query_source_1}`"
    # f"LIMIT 10000;"
            )
db_query_2 = (
    f"SELECT {sample_variable} FROM `{query_source_2}`;"
            )

if query_source_2 == 'Enter the source table':
    # Provide information for the following items
    significance_level = 0.05 # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
    population_mean = 7 # Change the value accordingly
    population_stDev = [] # Put a value in the list if population variance (σ) is known; otherwise, leave the list empty

    two_tailed_test = f'H0: {sample_variable} = {population_mean} and H1: {sample_variable} != {population_mean}'
    left_tailed_test = f'H0: {sample_variable} >= {population_mean} and H1: {sample_variable} < {population_mean}'
    right_tailed_test = f'H0: {sample_variable} <= {population_mean} and H1: {sample_variable} > {population_mean}'

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
    if population_stDev == []:
        Z_statistic = 0
    else:
        Z_statistic = round((sample_mean-population_mean)/(population_stDev[0]/(sample_size**0.5)),2)
    t_statistic = round((sample_mean-population_mean)/(sample_stDev/(sample_size**0.5)),2)

    Z_alpha = scipy.stats.norm.ppf(1-significance_level)
    t_alpha = scipy.stats.t.ppf(q=1-significance_level/2,df=(sample_size-1))
    t_alpha_r = scipy.stats.t.ppf(q=1-significance_level,df=(sample_size-1))
    t_alpha_l = scipy.stats.t.ppf(q=significance_level,df=(sample_size-1))

    data_prep = time.time()
    print(f"Calculation of the variables took {data_prep - source_download} seconds...")

    if population_stDev != []:
        print(f"Population standard deviation is known and sample size is {sample_size}. Furthermore, if:\n"
              "- sample size is less than 30, but it is normally distributed, or\n"
              "- sample size is 30 or more\n"
              "-> We use Z test. However, if sample size is less than 30, and the distribution is unknown or not normal"
              ", we need to use non-parametric methods.")
        if hypothesis_testing == two_tailed_test:
            print(f"Obviously, this is a two tailed test. Z critical value for the significance level of α/2 = {significance_level/2} is {Z_alpha/2}."
                  f" Z statistic is {Z_statistic} = ({sample_mean}-{population_mean})/({population_stDev[0]}/{sample_size}**0.5).")
            if abs(Z_statistic) > Z_alpha/2:
                print(f"{two_tailed_test} -> The null hypothesis should be rejected.")
            else:
                print(f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == left_tailed_test:
            print(f"Obviously, this is a left tailed test. Z critical value for the significance level of α = {significance_level} is {-Z_alpha}."
                  f" Z statistic is {Z_statistic} = ({sample_mean}-{population_mean})/({population_stDev[0]}/{sample_size}**0.5).")
            if Z_statistic < -Z_alpha:
                print(f"{left_tailed_test} -> The null hypothesis should be rejected.")
            else:
                print(f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == right_tailed_test:
            print(f"Obviously, this is a right tailed test. Z critical value for the significance level of α = {significance_level} is {Z_alpha}."
                  f" Z statistic is {Z_statistic} = ({sample_mean}-{population_mean})/({population_stDev[0]}/{sample_size}**0.5).")
            if Z_statistic > Z_alpha:
                print(f"{right_tailed_test} -> The null hypothesis should be rejected.")
            else:
                print(f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
    else:
        print(f"Population standard deviation is unknown and sample size is {sample_size}. Furthermore, if:\n"
              "- sample size is less than 30, but it is normally distributed, or\n"
              "- sample size is 30 or more\n"
              "-> We use Student t test. However, if sample size is less than 30, and the distribution is unknown or not normal"
              ", we need to use non-parametric methods.")
        if hypothesis_testing == two_tailed_test:
            print(
                f"Obviously, this is a two tailed test. T critical value for the significance level of α/2 = {significance_level/2} is {t_alpha}."
                f" T statistic is {t_statistic} = ({sample_mean}-{population_mean})/({sample_stDev}/{sample_size}**0.5).")
            if abs(t_statistic) > t_alpha:
                print(f"{two_tailed_test} -> The null hypothesis should be rejected.")
            else:
                print(f"{two_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == left_tailed_test:
            print(
                f"Obviously, this is a left tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_l}."
                f" T statistic is {t_statistic} = ({sample_mean}-{population_mean})/({sample_stDev}/{sample_size}**0.5).")
            if t_statistic > t_alpha_l:
                print(f"{left_tailed_test} -> The null hypothesis should be rejected.")
            else:
                print(f"{left_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")
        if hypothesis_testing == right_tailed_test:
            print(
                f"Obviously, this is a right tailed test. T critical value for the significance level of α = {significance_level} is {t_alpha_r}."
                f" T statistic is {t_statistic} = ({sample_mean}-{population_mean})/({sample_stDev}/{sample_size}**0.5).")
            if t_statistic > t_alpha_r:
                print(f"{right_tailed_test} -> The null hypothesis should be rejected.")
            else:
                print(f"{right_tailed_test} -> We don't have enough evidence from our sample data to reject the null hypothesis.")

    if_statement = time.time()
    print(f"Making a decision on the null hypothesis rejection took {if_statement - data_prep} seconds...")

else:
    print("Test if two samples have the same mean values.")

end = time.time()
print(f"The full script ended in {end - start} seconds...")

# OPTIONAL: Plot a histogram to check if the sample fallows a normal distribution
plt.hist(x)
plt.show()