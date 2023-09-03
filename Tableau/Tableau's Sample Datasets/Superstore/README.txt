
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the Excel file from https://public.tableau.com/app/learn/sample-data?qt-overview_resources=1#qt-overview_resources.
- Build visuals in Tableau (https://public.tableau.com/app/profile/slavisadurdic/viz/SuperstoreSampleDataset_16935201834720/Dashboard1).
- Run hypothesis testing in Python.


*** Python Activities ***

I used python script "Goodness of fit hypothesis testing - superstore.py" (available in the project folder) to run statistical analysis (see Statistical Models section).


*** Tableau Activities ***

I have built many pages/reports which I have combined into a single (just a bit extended) dashboard.
Tableau dashboard has been published: https://public.tableau.com/app/profile/slavisadurdic/viz/SuperstoreSampleDataset_16935201834720/Dashboard1 
I have used many different charts: pie, map, and bar visuals. Those visuals mostly show financial results (sales, profit) of a fictitious company during the period 2014-2017 by geo location (region, US states, cities), category, and segment.
In order to emphasize the interactivity, I've added a filter "Year of Order Date" which helped in analyzing the overall financial data as well as for each year separately.
I was able to make some conclusions based on the visuals:
1) Overall, "Consumer" segment brings the highest profit (around 45% of the total profit).
2) Overall, "Technology" category brings the highest profit (around 50% of the total profit, and it has been increasing over time).
3) California and New York bring the highest sales and profit results, while Texas and Pennsylvania were the two US states with the worst financial results (i.e., financial losses) reported in the given period.
4) Let's take Texas for instance - Although sales amount was one of the best among all states, it seems that negative profit comes from very high cost of goods sold (i.e., furniture COGS). Additionally, "Furniture", as a product category, influenced the most negative financial results.
5) Furthermore, although "Tables" appeared to be a significant revenue item, if we take a closer look at its profitability, we can see that they are least profitable.


*** Statistical Models *** 

> Goodness of fit hypothesis testing model:

I have performed Chi-Square χ² Goodness of Fit hypothesis testing in Python by using the script "Goodness of fit hypothesis testing - superstore.py". I have used stats from scipy python library to get chi_square critical value.
I have tested if profit by categories in year 2017 corresponds to overall profit by categories for the given period 2014-2017.
- expected_frequency for categories: Technology, Office Supplies, and Furniture = [0.5079,0.4277,0.0644], respectively
- observed_frequency for the same categories in year 2017 = [0.5424,0.4253,0.0323], respectively
Model summary results have been shown below.
	Chi-Square χ² Goodness of Fit hypothesis testing...
	H0: Observed frequencies are the same as expected frequencies
	H1: Observed frequencies are NOT the same as expected frequencies
	χ² critical value is 9.21034037197618, for the significance level of α = 0.01 and degrees of freedom of df = 2.
	χ² statistic is 60.79870124924023.
	Since χ² statistic falls under the rejection area, the null hypothesis should be rejected.


