# MAKE SURE TO PROVIDE CORRECT INFO FOR LINES 11-14

# The Chi-square goodness of fit test is a statistical hypothesis test used to determine whether a variable is likely to come from a specified distribution or not.
# It is often used to evaluate whether sample data is representative of the full population.

import scipy.stats

print("Chi-Square χ² Goodness of Fit hypothesis testing...") # Always right tailed test

# Provide information for the following items
significance_level = 0.01  # Normally, alpha (α) is taken as 0.1, 0.05, or 0.01
expected_frequency = [0.5079,0.4277,0.0644]  # Enter % value(s), e.g. [0.3,0.2,0.5]
observed_frequency = [0.5424,0.4253,0.0323]  # Enter % or nominal value(s) accordingly
sample_size = 3312  # Change the value accordingly

H0 = 'H0: Observed frequencies are the same as expected frequencies'
print(H0)
H1 = 'H1: Observed frequencies are NOT the same as expected frequencies'
print(H1)

observed_sum = 0
for i in observed_frequency:
    observed_sum = observed_sum + i
if observed_sum > sample_size*0.98 and observed_sum < sample_size*0.98: # 2% of tolerance
    print(f'Sum of observed frequencies is {observed_sum}, and sample size is {sample_size}.')
    chi_square_statistic = 0
    for i in range(len(observed_frequency)):
        chi_square_statistic = chi_square_statistic + ((observed_frequency[i] - expected_frequency[i]*sample_size) ** 2)/(expected_frequency[i]*sample_size)
else:
    print(f'Sum of observed frequencies is {observed_sum}.')
    print("Observed frequencies seem to be provided as percentage values...")
    chi_square_statistic = 0
    for i in range(len(observed_frequency)):
        chi_square_statistic = chi_square_statistic + (
                    (observed_frequency[i]*sample_size - expected_frequency[i] * sample_size) ** 2) / (
                                           expected_frequency[i] * sample_size)

for i in range(len(expected_frequency)):
    sample_check = []
    if sample_size * expected_frequency[i] < 5:
        print(f'Please note that n{i}*p{i} is {sample_size * expected_frequency[i]}<5...')
        sample_check.append(i)
if sample_check == []:
    print("Checked performed -> Sample size seems fine...")

chi_square = scipy.stats.chi2.ppf(1 - significance_level, len(observed_frequency) - 1)
print(
    f"χ² critical value is {chi_square}, for the significance level of α = {significance_level} and degrees of freedom of df = {len(observed_frequency) - 1}."
    f"\nχ² statistic is {chi_square_statistic}.")
if chi_square_statistic > chi_square:
    print(
        f"Since χ² statistic falls under the rejection area, the null hypothesis should be rejected.")
else:
    print(f"The difference is not statistically significant, so we don't/can't reject the null hypothesis.")