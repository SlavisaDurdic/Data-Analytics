
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the "bigquery-public-data.covid19_usafacts.summary" dataset available on - BigQuery.
- Load the data to a MySQL table.
- Execute some basic sql queries to get first insights about the data.
- Build visuals in Power BI Desktop.
- Run statistical models.


*** Python Activities ***

For the ETL processes, I have used Python programming language and accordingly the "Python Client for Google BigQuery" Google Cloud official documentation reference (https://cloud.google.com/python/docs/reference/bigquery/latest).

I've generated a python script in PyCharm integrated development environment - "GoogleCloudAPI data ETL from BigQuery to MySQL - covid19.py" (which is available in the GitHub project folder) in order to automate the process as much as possible. Users should edit lines 20 and 23 of the script, i.e. users need to 1) provide information about the MySQL table name which will be created in the database, and 2) define sql query to pull data from the "bigquery-public-data.covid19_usafacts.summary" dataset on BigQuery.

You can notice different python libraries imported to my .py file, such as pandas (... to work with dataframes), mysql.connector (... to connect to and load data into a mySQL database), and decimal (due to the formating reasons).

Table "bigquery-public-data.covid19_usafacts.summary" consists of 7 columns. I aimed to add one more, which I did, so I could execute the "CREATE TABLE" sql command in the first place. This additional column is a sort of an id column, and I named it "helper_id".

In this case, the code is written in order to get everything done from scratch: create a new table and insert all records. Note: It is not configured to support incremental activities.

Once uploaded, please note that 3.905.039 records are saved. The size of the table was 278.8 MB.

Using the same python script, I've also downloaded two more sources to my .py file: "bigquery-public-data.census_bureau_acs.state_2020_5yr" and "bigquery-public-data.census_bureau_acs.county_2020_5yr". I did that in order to get the number of total population in each state and/or county, which I've used in MySQL queries to calculate number of confirmed cases and/or deaths per 100000 (for more info see the following section).


*** MySQL Activities ***

By looking at the data summary, I soon realized that confirmed cases and death values refer to cumulative amounts, which I was able to confirm on the following links (especially the link No. 4):
  1) https://www.nytimes.com/interactive/2023/05/11/us/covid-deaths-us.html
  2) https://console.cloud.google.com/marketplace/product/usafacts-public-data/covid19-us-cases?project=true-conduit-266216
  3) https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/
  4) https://usafacts.org/articles/detailed-methodology-covid-19-data/

In MySQL I've performed queries and confirmed that:

- all 3.905.039 rows have been successfully inserted.

- NULL values don't exist in the table:

	SELECT COUNT(*) FROM data_analysis.publicbigquery_covid19_usafacts_summary
	WHERE deaths IS NULL OR confirmed_cases IS NULL OR date IS NULL OR state_fips_code IS NULL
	OR state IS NULL OR county_name IS NULL OR county_fips_code IS NULL;

- it seems that there are no duplicates:
	
	WITH cte AS (
  		SELECT county_fips_code, county_name, state, state_fips_code, date, confirmed_cases, deaths,
    		ROW_NUMBER() OVER(PARTITION BY county_fips_code, county_name, state, state_fips_code, date, 				confirmed_cases, deaths) AS pos_in_group
  		FROM data_analysis.publicbigquery_covid19_usafacts_summary
		)
	SELECT *
	FROM cte
	WHERE pos_in_group > 1;

- data count for the date 29-May-2023 (this is the last reported date) equals to 3193 data points:

	SELECT date, COUNT(confirmed_cases), COUNT(deaths)
	FROM data_analysis.publicbigquery_covid19_usafacts_summary
	WHERE date = '2023-05-29'
	;

	> date	 	COUNT(confirmed_cases) 	COUNT(deaths)
	> 2023-05-29	3193			3193

- top 5 states with the highest deaths:

	SELECT state, SUM(deaths) AS deaths
	FROM data_analysis.publicbigquery_covid19_usafacts_summary
	WHERE date = '2023-05-29' # Last available date in the sample
	GROUP BY state
	ORDER BY SUM(deaths) DESC
	LIMIT 5;

	> state	deaths
	> CA	101918
	> TX	92378
	> FL	88505
	> NY	77558
	> PA	51144

A similar query as below can be found on the Google Cloud page as a sample qeury - it joins data from the Census Bureau's American Community Survey to determine which counties (ohter than unallocated) had the most confirmed COVID-19 cases per 100,000 residents as of 2023-05-29 (last date):

	SELECT
	  covid19.state,
	  covid19.county_name,
	  ROUND(confirmed_cases/total_pop *100000,2) AS confirmed_cases_per_100000,
	  ROUND(deaths/total_pop *100000,2) AS deaths_per_100000,
	  confirmed_cases,
	  deaths, 
	  total_pop AS county_population
	FROM `publicbigquery_covid19_usafacts_summary` covid19
	JOIN `publicbigquery_census_bureau_acs_county_2020_5yr` acs 
	ON covid19.county_fips_code = acs.geo_id 
	WHERE date = '2023-05-29' # Last date reported
	AND county_fips_code != "00000"
	AND confirmed_cases + deaths > 0
	ORDER BY confirmed_cases_per_100000 DESC, deaths_per_100000 DESC
	LIMIT 10;

	> state county_name		cases_per_100K  	deaths_per_100K cases 	deaths  county_population
	> TX	Loving County 		350427.35		854.7		410	1	117
	> TX	Delta County 		188004.55		530.6		9921	28	5277
	> TX	Jim Hogg County 	73395.03		443.42		3807	23	5187
	> GA	Chattahoochee County 	66103.15		229.23		6921	24	10470
	> TX	Dimmit County 		61043.78		508.21		6246	52	10232
	> KY	Perry County 		60873.37		799.51		15989	210	26266
	> SD	Dewey County 		60143.81		787.54		3513	46	5841
	> FL	Miami-Dade County 	57374.42		239.21		1552280	6472	2705530
	> ND	Rolette County 		57193.32		297.85		8257	43	14437
	> WI	Menominee County 	53504.16		350.42		2443	16	4566

A similar query as below can be found on the Google Cloud page as a sample query - it determines top 5 US states which had the greatest number of total confirmed COVID-19 cases per 100,000 residents that were not allocated to a specific county as of 2023-05-29 (last sample date):

	SELECT
	  covid19.county_name,
	  covid19.state,
	  total_pop AS state_population,
	  confirmed_cases,
	  ROUND(confirmed_cases/total_pop *100000,2) AS confirmed_cases_per_100000,
	  deaths, 
	  ROUND(deaths/total_pop *100000,2) AS deaths_per_100000
	FROM
	  `publicbigquery_covid19_usafacts_summary` covid19
	JOIN
	  `publicbigquery_census_bureau_acs_state_2020_5yr` acs
	ON covid19.state_fips_code = acs.geo_id
	WHERE
	  date = '2023-05-29' # Last date reported
	  AND county_fips_code = "00000" # Representation of no county in the dataset
	ORDER BY
	  confirmed_cases_per_100000 desc, deaths_per_100000 desc
	LIMIT 5;

	> county_name		state 	county_population	cases	cases_per_100K	deaths  deaths_per_100K
	> Statewide Unallocated	TN  	6772270			424396	6266.67		2521	37.23
	> Statewide Unallocated	IN  	6696890			338760	5058.47		2586	38.61
	> Statewide Unallocated	OR  	4176350			206185	4936.97		1579	37.81
	> Statewide Unallocated	NE  	1923830			89061	4629.37		2767	143.83
	> Statewide Unallocated	IL  	12716200		578191	4546.9		11375	89.45

A similar query as below can be found on the Google Cloud page as a sample query - it determines top 5 US states which had the greatest number of total confirmed COVID-19 cases per 100,000 residents excluding unallocated county as of 2023-05-29 (last date):

	SELECT
	  covid19.county_name,
	  covid19.state,
	  total_pop AS state_population,
	  confirmed_cases,
	  ROUND(confirmed_cases/total_pop *100000,2) AS confirmed_cases_per_100000,
	  deaths, 
	  ROUND(deaths/total_pop *100000,2) AS deaths_per_100000
	FROM
	  `publicbigquery_covid19_usafacts_summary` covid19
	JOIN
	  `publicbigquery_census_bureau_acs_state_2020_5yr` acs
	ON covid19.state_fips_code = acs.geo_id
	WHERE
	  date = '2023-05-29' # Last date reported
	  AND county_fips_code != "00000"
	ORDER BY
	  confirmed_cases_per_100000 desc, deaths_per_100000 desc
	LIMIT 5;

	> county_name			state 	county_population	cases	cases_per_100K	deaths  deaths_per_100K
	> Providence County 		RI	1057800			281708	26631.55	2752	260.16
	> District of Columbia 		DC	701974			169149	24096.19	1392	198.3
	> Clark County 			NV	3030280			678136	22378.65	9385	309.71
	> New Castle County 		DE	967679			189325	19564.86	1654	170.92
	> City and County of Honolulu	HI	1420070			270518	19049.57	1184	83.38


*** PowerBI Activities ***

I have built 4 pages/reports which included many different charts: line, map, matrix, card and scatter plot visuals. Those visuals mostly show the number of confirmed cases and/or deaths by state and county, as well as their cumulative values over time. On the other hand, scatter charts represent simple regression models with just two variables (for more info see the following section).
In order to emphasize the interactivity, I've added slicer visuals, i.e. filters: "Year, Month, Day" and "State" or "State, County", where seemed appropriate.

One thing that I noticed is that large number of counties is not accurately placed on a map. However, in this test case, it's not material, so the issue remains unresolved.


*** Statistical Models *** 

Source information - https://3cloudsolutions.com/resources/simple-linear-regression-in-power-bi/
'The Simple Linear Regression model allows us to summarize and examine relationships between two variables. It uses a single independent variable and a single dependent variable and finds a linear function that predicts the dependent variable values as a function of the independent variables.
The Coefficient of Correlation is a statistic we use to determine if there is a relationship between two variables. The output of this statistic equals somewhere between 1 and -1. The closer to 1 the number is, the more positively related the variables are. If X increases, Y increases. The closer to -1 the number is, the more negatively related the variables are. If X increases, Y decreases.  
The Coefficient of Determination is a related statistic that then tells us how well our model fits the data. This statistic is always between 0 and 1, and the closer to 1 the value is, the better our model fits the data set.' 

Source information - https://iterationinsights.com/article/linear-regression-in-power-bi/
'Linear Regression is a statistical model applied to businesses to help forecast events based on historical trend analysis. Simple Linear regression uses one variable, called the independent variable. The independent variable predicts the outcome of another variable called the dependent variable.
A Linear Regression Model is created by fitting a trend line to a dataset where a linear relationship already exists.
This trend line has the equation of y = mx + b and is used to make estimates.'

Linear Regression model in my analysis project: Scatter plot, trend, correlation coefficient and coefficient of determination of the model have been implemented in both Python and Power BI. This was achieved in Python with the matplotlib and scipy libraries (python script "Simple regression analysis applied on public BigQuery data - covid19" that I created for this process is available in the project folder), while Power BI has its own built-in method to calculate the correlation coefficient.

Additionally, there is an Excel file within the project folder with a step-by-step calculation of the corresponding coefficients.

I've declared my variables. Basically, I've used "confirmed_cases" as my independed variable (x) and "deaths" as my dependent variable (y).
In Power BI, there are two pages regarding regression model. One of them takes all data whereever date is 29-May-2023, while the other one takes the same data, except the outlier for which the helper_id is 1731997. One can notice that correlation coefficient and coefficient of determination (created as new measures) values for the model without extremes are 0.94 and 0.89, respectively.

