
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the "bigquery-public-data.world_bank_global_population.population_by_country" dataset available on BigQuery.
- Load the data to a MySQL table or tables.
- Build visuals in Power BI Desktop.
- Build Power Point presentation.
- Provide project insights.


*** Python Activities ***

For the ETL processes, I have used Python programming language and accordingly the "Python Client for Google BigQuery" Google Cloud official documentation reference (https://cloud.google.com/python/docs/reference/bigquery/latest).

I've generated a python scripts in PyCharm integrated development environment - "GoogleCloudAPI data ETL from BigQuery to MySQL - WB_population_by_year.py" and "GoogleCloudAPI data ETL from BigQuery to MySQL - WB_population_by_country.py" (which are available in the GitHub project folder) in order to automate the process as much as possible. Users should edit lines 22 and 25 of the script (or lines 20 and 23, depending on the script), i.e. users need to 1) provide information about the MySQL table name which will be created in the database, and 2) define sql query to pull data from a dataset on BigQuery. "GoogleCloudAPI data ETL from BigQuery to MySQL - WB_population_by_country.py" script is created in order to basically transpose information from the original table, i.e. to convert country data listed as rows into the columns. 

You can notice different python libraries imported to my .py file, such as pandas (... to work with dataframes), mysql.connector (... to connect to and load data into a mySQL database), and decimal (due to the formating reasons).

Table "bigquery_WB_global_population_by_year" consists of 63 columns. I aimed to add one more, which I did, so I could execute the "CREATE TABLE" sql command in the first place. This additional column is a sort of an id column, and I named it "helper_id". The same goes for the table "bigquery_WB_global_population_by_country", which consists of 264+1 columns (transposed rows).

The code is written in order to get everything done from scratch: create a new table and insert all records. Note: It is not configured to support incremental activities.


*** MySQL Activities ***

I haven't performed any queries for this project.


*** PowerBI Activities ***

I have built 3 pages/reports which included many different charts: card, bar, and line visuals. Those visuals mostly show population movement by country and year, comparison analysis of the two largest countries in the world, and population situation in Serbia over time.

I was able to make some conclusions based on the visuals, i.e. project insights:
1) World population more than doubled in last 50 years.
2) China and India make 1/3 of the world population.
3) Given the population growth rate and population stats in year 2018 (less than 3% of difference), India will surpass China in few years.
4) Population in Serbia constantly decline for the last 30 years (exception is period 1990-1994).


*** Statistical Models *** 

I haven't performed any statistical analysis for this project other than a simple forecasting of population in Serbia in Power BI Desktop app.

