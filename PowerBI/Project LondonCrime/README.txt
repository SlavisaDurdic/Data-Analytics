
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the "bigquery-public-data.london_crime.crime_by_lsoa" dataset available on BigQuery.
- Load the data to a MySQL table or tables.
- Execute some basic sql queries to get first insights about the data.
- Build visuals in Power BI Desktop.
- Run time series analysis in Power BI Desktop.
- Test hypothesis in Python.


*** Python Activities ***

For the ETL processes, I have used Python programming language and accordingly the "Python Client for Google BigQuery" Google Cloud official documentation reference (https://cloud.google.com/python/docs/reference/bigquery/latest).

I've generated a python script in PyCharm integrated development environment - "GoogleCloudAPI data ETL from BigQuery to MySQL - LondonCrime.py" (which is available in the GitHub project folder) in order to automate the process as much as possible. Users should edit code lines specified in the script itself, i.e. users need to 1) provide information about the MySQL table name which will be created in the database, and 2) define sql query to pull data from BigQuery.

You can notice different python libraries imported to my .py file, such as pandas (... to work with dataframes), mysql.connector (... to connect to and load data into a mySQL database), and decimal (due to the formating reasons).

Table "bigquery-public-data.london_crime.crime_by_lsoa" consists of 7 columns. I aimed to add one more, which I did, so I could execute the "CREATE TABLE" sql command in the first place. This additional column is a sort of an id column, and I named it "helper_id".

The code is written in order to get everything done from scratch: create a new table and insert all records. Note: It is not configured to support incremental activities.

Once uploaded, please note that 4.496.868 records are saved in the "bigquery_london_crime_crime_by_lsoa" table. The size of the table is 472 MB.


*** MySQL Activities ***

In MySQL I've performed queries and confirmed that:

- all rows have been successfully inserted into the table.

	SELECT COUNT(*) FROM data_analysis.bigquery_london_crime_crime_by_lsoa;;

- it seems that there are no duplicates (this QUERY has been performed directly on BigQuery due to the performance issues):
	
	WITH cte AS (
  		SELECT lsoa_code, borough, major_category, minor_category, value, year, month,
    		ROW_NUMBER() OVER(PARTITION BY lsoa_code, borough, major_category, minor_category, value, year, month) AS RN
  		FROM data_analysis.bigquery_london_crime_crime_by_lsoa
		)
	SELECT *
	FROM cte
	WHERE RN > 1;

- "Theft and Handling" and "Violence Against the Person" make the top crime major categories by average number of crime:

	SELECT major_category, minor_category, avg(value) AS average_crime
	FROM data_analysis.bigquery_london_crime_crime_by_lsoa
	GROUP BY major_category, minor_category
	ORDER BY average_crime DESC, major_category, minor_category;

	> major_category 		minor_category 		average_crime
	> Theft and Handling		Other Theft		1.8382
	> Violence Against the Person	Harassment		1.1817
	> Violence Against the Person	Common Assault		1.0194
	> Theft and Handling		Theft From Shops	0.9332
	> Theft and Handling		Theft From Motor Vehicle0.8819
	> Violence Against the Person	Assault with Injury	0.8271

- the daily average crime rate for period 2014-2016:

	SELECT SUM(value)/(3*365) as average_crime_value
	FROM data_analysis.bigquery_london_crime_crime_by_lsoa;

	> average_crime_value
	> 1943.3132


*** PowerBI Activities ***

I have built 4 pages/reports which included many different charts: card, bar, treemap, and line visuals. Those visuals mostly show a number of committed crime in London during the period 2014-2016 (timeline), crime by London borough and major category, and details about the crime by major and minor categories.
In order to emphasize the interactivity, I've added slicer visual "year" which helped in analyzing the London crime data.
I have also configured the mobile layout - a report view for mobile devices.
I was able to make some conclusions based on the visuals:
1) During the period 2014-2016, crime in London had an upward sloping trend. The 2-year crime rate was 8.22%.
2) It seems that there is a seasonality pattern behavior. Namely, the peak of committed crime seems to be in months October-December, while in February the number of crime appears to be at its lowest.
3) Westminster, Lambeth, and Southwark are top 3 boroughs by number of crime during the observed period 2014-2016.
4) Theft and Handling dominated as a crime category in all London districts, followed by the Violence Against the Person and then the Burglary.
5) Based on a hypothesis testing that I performed, with a confidence level of 95%, we can’t reject the hypothesis that the mean value of committed crime in Westminster is higher than the mean value of committed crime in Lambeth borough.


*** Statistical Models *** 

> Time Series:
I have performed time series analysis in Power BI.
First, I had to create a new column "MonthName" and to convert month numbers to month names (i.e. from 1 to January, from 2 to February, etc.). Additionally, one more column "Date" has been created as a concatenation of fields "year" and "MonthName". I used this new column to model time series and make monthly and yearly projections.

> Hypothesis Testing:
I have performed hypothesis testing of two samples over London crime dataset in Python, in order to test if Westminster mean is equal to or higher than Lambeth mean of committed crime, i.e. defining the null hypothesis as shown bellow.

> Null hypothesis (H0): Westminster mean >= Lambeth mean;
> Alternative hypothesis (H1): Westminster mean < Lambeth mean;

There is a python script "Hypothesis testing applied on public BigQuery data - LondonCrime" that I created and that can be found in the project folder. The decision on accepting or rejecting the HO was based on a critical value method, and the final output is that with the confidence level of 95% we don't have enough evidence in the sample to reject the null hypothesis.

