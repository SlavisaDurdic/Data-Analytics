
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the Excel file from https://public.tableau.com/app/learn/sample-data?qt-overview_resources=1#qt-overview_resources.
- Connect to the file from Looker Studio and build visuals (https://lookerstudio.google.com/reporting/5f9ff298-dc67-4d7a-a662-6edd4fad6b2e/page/p_yzjndubgbd).
- Perform multivariate analysis in Python to predict output based on both, numerical and categorical values.


*** Python Activities ***

I have used python script "Multivariate Linear Regression analysis - CSV, JSON or BigQuery - Global Burden of Disease.py" (available in the project folder) to run statistical analysis (see Statistical Models section).


*** Looker Studio Activities ***

The report is accessible through this Looker Studio link: https://lookerstudio.google.com/reporting/5f9ff298-dc67-4d7a-a662-6edd4fad6b2e/page/p_yzjndubgbd 
I have built bar, map, and pie charts. Those visuals show age-specific and sex-specific mortality in 187 countries for the period 1970-2010.
In order to better analyze data regarding number of deaths and the death rates, I've configured visuals to act as filters on the Looker report pages.
I was able to make some conclusions based on the visuals:
1) Mortality rates are falling around the world. Globally, 52.6 million deaths occurred in 2010, approximately 13.5% more than in 1990 and 21.9% more than in 1970. But the global crude death rate has fallen from 11.7 to 7.7 per 1,000 population due to the much larger (86.7%) relative increase in world population – from 3.7 billion in 1970 to 6.9 billion in 2010.
2) The world has made tremendous progress fighting child mortality. Deaths of children under the age of 5 were cut by more than half from 16.38 million in 1970 to 11.55 million in 1990 and then to 6.84 million in 2010, although the global annual number of births increased by 12%. This progress has beaten every published prediction. However, child mortality remains a pressing issue. Effective interventions are available to prevent many of the remaining 6.8 million child deaths.
3) African countries and South Asia have the highest death rates.


*** Statistical Models *** 

> Multivariate Linear Regression Analysis:

Just for fun, I have performed multivariate linear regression analysis in Python to demonstrate how model works. I have used sklearn python library "LinearRegression" method to predict outcome based on several inputs (both, numeric and categorical). Also, from sklearn I have used "train_test_split" method to train and test the model. The script "Multivariate Linear Regression analysis - CSV, JSON or BigQuery - Global Burden of Disease.py" that I have created for this project is available in the project folder.

