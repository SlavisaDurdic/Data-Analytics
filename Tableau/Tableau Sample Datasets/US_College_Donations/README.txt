
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the Excel file from https://public.tableau.com/app/learn/sample-data?qt-overview_resources=1#qt-overview_resources.
- Use ETL python script to load the data to MySQL table(s).
- Execute some basic SQL queries.
- Build visuals in Tableau (https://public.tableau.com/app/profile/slavisadurdic/viz/USCollegeDonations_16962790623100/USCollegeDonations).
- Run proportion hypothesis testing in Python.


*** Python Activities ***

I used python script "ETL from BigQuery or CSV file to MySQL - College_donations.py" (available in the project folder) to run ETL process to load data from CSV file to a MySQL table, as well as "Proportion hypothesis testing - CSV, MySQL, or BigQuery - College_donations.py" (also available in the project folder) to run statistical analysis (see Statistical Models section).


*** MySQL Activities ***

In MySQL I've performed below queries and I have confirmed that:

- all rows have been successfully inserted into table(s).
	
	SELECT COUNT(*) FROM data_analysis.college_donation;

- there are no duplicates as no value has been returned:
	
	WITH cte AS (	
	SELECT ï»¿Allocation_Subcategory, City, College, Gift_Allocation, Gift_Amount, Gift_Date, Major, Prospect_ID, State, ROW_NUMBER() OVER(PARTITION BY ï»¿Allocation_Subcategory, City, College, Gift_Allocation, Gift_Amount, Gift_Date, Major, Prospect_ID, State) AS RN  			
	FROM data_analysis.college_donation	 	)	

	SELECT * FROM cte WHERE RN > 1;

- percentage of Scholarship in total gift amount for all dataset years (=43%), and for just year 2015 (=42%):

	SELECT 
		SUM(Gift_Amount) AS gift_amount,
		SUM(CASE WHEN Gift_Allocation = 'Scholarship' THEN Gift_Amount END) AS scholarship_gift_amount,
		ROUND(SUM(CASE WHEN Gift_Allocation = 'Scholarship' THEN Gift_Amount END)/SUM(Gift_Amount),2) AS scholarship_percentage,
		SUM(CASE WHEN Gift_Date LIKE '%2015%' THEN Gift_Amount END) AS gift_amount_y2015,
		SUM(CASE WHEN Gift_Date LIKE '%2015%' AND Gift_Allocation = 'Scholarship' THEN Gift_Amount END) AS scholarship_gift_amount_y2015,
		ROUND(SUM(CASE WHEN Gift_Date LIKE '%2015%' AND Gift_Allocation = 'Scholarship' THEN Gift_Amount END)/SUM(CASE WHEN Gift_Date LIKE '%2015%' 			THEN Gift_Amount END),2) AS scholarship_percentage_y2015
	FROM data_analysis.college_donation;


*** Tableau Activities ***

I have built a large number of pages/worksheets out of which I have created four dashboards. Then, I created a Tableau story page made of these dashboards.
Tableau story report has been saved and published on Tableau Public page: https://public.tableau.com/app/profile/slavisadurdic/viz/USCollegeDonations_16962790623100/USCollegeDonations 
I have used many different charts: pie, map, bar, and line charts. Those visuals show $ amount of donations in a form of scholarship, endowment, and campus resource by college, allocation subcategory, major, time, year of graduation, and state and city in the United States during the five years period 2010-2015.
In order to better observe data changes/evolution/insights and so, I've added filters "Year of Gift Date" and "Gift Allocation" to all of my reports, and I have marked all dashboard visuals as filters, too.
I was able to make some conclusions based on the visuals:
1) More than 2/3 of total gift amount goes to: College of Natural Science, Arts and Sciences, Social Science, and Agriculture and Natural Resources.
2) Colleges in California, Colorado, and Texas received most donations. Denver is top one city in the US with respect to gift amount received.
3) Gift Amount tends to slightly increase over time. It seems that most donations used to be made beginning/end of year - perhaps due to some yearly event in January and/or December.


*** Statistical Models *** 

> Hypothesis Testing:

I have performed hypothesis testing over one sample to test if Scholarship share is statistically significantly different in year 2015 compared to the whole period, i.e. as shown below.

 Null hypothesis (H0): Share of scholarship in year 2015 is the same as the share of scholarship of all years (=43%);
 Alternative hypothesis (H1): Share of scholarship in year 2015 is different from the share of scholarship of all years (=43%);

There is a python script "Proportion hypothesis testing - CSV, MySQL, or BigQuery - College_donations.py" that I created and that can be found in the project folder. The decision on accepting or rejecting the HO was based on a critical value method, and the final output is that with the confidence level of 95% we don't have enough evidence in the sample to reject the null hypothesis.
Model summary results have been shown below.
	Hypothesis testing of population proportion - one sample...
	MySQL is the datasource.
	You're connected to database:  ('data_analysis',)
	There are 0 invalid points of x_set in the MySQL table.
	There are 0 invalid points of x_subset in the MySQL table.
	There are 723 of x_set values and 303 of x_subset values.
	Top x_subset values in the list:[5779.0, 5384.0, 2633.0, 5214.0, 1655.0, 2002.0, 4648.0]...
	Data download and data cleansing took about 0.16159605979919434 seconds...
	Sample is considered large, since n*p and n*q are 310.89 and 412.11000000000007, respectively, larger than 5...
	Sample p is 0.4190233913813066.
	Obviously, this is a two tailed test. Z critical value for the significance level of α/2 = 0.025 is 1.959963984540054. Z statistic is -0.6.
	H0: p = 0.43 and H1: p != 0.43 -> We don't have enough evidence from our sample data to reject the null hypothesis.
	The full script ended in 0.16737675666809082 seconds...


