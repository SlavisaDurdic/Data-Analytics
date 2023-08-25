
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the PowerBI "Financials" sample dataset.
- Build visuals in Power BI Desktop.
- Run regression analysis in Power BI Desktop and Python.
- Perform One-factor ANOVA hypothesis testing in Python.


*** Python Activities ***

There is a sample dataset available for Microsoft Power BI. The file is in Excel format. I have done some statistical analysis in Python scripts (see the Statistical Models section).


*** PowerBI Activities ***

I have built 4 pages/reports which included many different charts: bar, line, map, card and scatter plot visuals. Those visuals mostly show financial results (sales and profit) by segment, product and/or time.
I have also configured the mobile layout - a report view for mobile devices.
I was able to make some project insights:
1) "Government" and "Small Business" segments generate most sales and profit.
2) Profit is more or less equally distributed accros all 5 countries.
3) Financial results are more or less steady over time.
4) Result from the 1-factor ANOVA test is that we cannot reject the hypothesis that all products from "Government" segment generate equal profits.


*** Statistical Models *** 

> Simple Regression Model:
I have performed regression analysis in Power BI by using scatter plot (Sales vs. Profit) and built-in trend line feature. Additionally, I have created new measures - Correlation Coefficient and Coefficient of Determination.
I have also performed the analysis in Python ("Simple regression analysis - powerbi_financials_dataset.py" script is available in the project folder). I noticed that results for coefficients slightly differ between Power BI and Python.

> One-factor ANOVA:
I have performed a hypothesis testing to check if all products within "Government" segment generate profits equally.
There is a python script ("1_factor ANOVA - powerbi_sample_financials.py") that I created and that can be found in the project folder. The decision on accepting or rejecting the HO was based on a p value, and the final output is that we don't have enough sifnificant evidence to reject the null hypothesis.

