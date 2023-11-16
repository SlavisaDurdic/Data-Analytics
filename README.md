# INSTRUCTIONS

Data analyses have been performed on publicly available datasets.

The GitHub repository contains four folders: Scripts, PowerBI, Tableau, and Looker Studio.\
Under the **Scripts** folder you can find some of the python scripts (last-updated) that have been used for the ETL processes and statistical modeling.\
Under **PowerBI**, **Tableau**, and **Looker Studio** folders (each representing a different BI tool) you can find many *project* folders. Each project folder is created for a specific dataset analysis, and mainly consists of:

- readme text file with detailed description about the project,
- Microsoft Power Point file with up to 15 slides that summarizes the project,
- Tableau or Looker Studio link (provided within the project's readme file) or Power BI file(s) - as a BI tool for visualizing data,
- python script used to pull data from BigQuery (or CSV) and load it into MySQL database,
- other files, such as python files for hypothesis testing, regression analysis, or similar.
  
******

## PROJECT CLASSIFICATION

I have divided analyzed topics into several categories, as shown below:

- Business:

> Superstore Sales [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Superstore) \
> Financials [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20PowerBI%20Financials) \
> Startup Venture Funding [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Technology%20-%20Startup%20Venture%20Funding) \
> Microsoft Financial Report [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/MSFT) \
> Apple Stock Data [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Apple_Stocks)
 
- Entertainment:

> Eurovision 1998 to 2010 [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Eurovision) \
> Star Wars Character Details [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Star_Wars) \
> IMDB [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20IMDB) \
> ATP Top-Ranked Singles Tennis Players [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/ATP)

- Public Data:

> FAA Wildlife Strikes, 2015 [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Wildlife_Strikes) \
> U.S. Home Sales, 1963-2016 [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Government%20-%20Home%20Sales) \
> London crime [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20LondonCrime) \
> US crime [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20US_crime) \
> World Bank population [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20WorldBank)

- Science:

> Significant Volcanic Eruptions [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Science%20-%20Volcano%20Eruptions) \
> Animal Speed [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20AnimalSpeed) \
> Belgrade Weather [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Belgrade_weather) \
> Global Burden of Disease [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Health%20-%20Global%20Burden%20of%20Disease) \
> Covid19 [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20Covid19) \
> University Advancement, Donations, and Giving [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/US_College_Donations)

## DATA COLLECTION

Data has been collected in/from different formats/sources:

- Excel (for example, Superstore and Eurovision are projects that use this data type)
- CSV (for example, ATP and Apple Stock Data are projects that use this data type)
- JSON (for example, Star Wars and Belgrade Weather are projects that uses this data type)
- PDF (for example, MSFT Income Statement is a project that uses this data type)
- URL (for example, Animal Speed is a project that uses data from this datasource)
- REST API (for example, Belgrade Weather is a project that uses data from this datasource)
- Yahoo Finance via yfinance python library (for example, Apple Stock Data is a project that uses this datasource)
- BigQuery (PowerBI datasets are based on BigQuery tables)
- MySQL database (served as a destination database for PowerBI datasets, but also used for Tableau and Looker dataset analyses)

## DATA CLEANSING

Not all datasets were ready for use, so more or less of data cleaning was required now and then, which has been done via different tools:

- Excel / CSV (US crime, Wildlife Strikes)
- Python (World Bank population, Apple Stock Data)
- Tableau (MSFT Income Statement, Belgrade Weather) / PowerBI Power Query (London crime, Animal Speed) / Looker Studio (Startup Venture Funding)

## DATA ANALYSIS AND VISUALIZATION

PowerBI, Tableau, Looker Studio, and/or MySQL and Python have been used for data analysis and visualization.
With respect to that, *statistical* modeling technics, listed below, have been performed:

- Simple regression model (covid19, Financials PowerBI sample, US crime, Eurovision, Star Wars)
- Time series (PowerBI: London crime, WB population; Tableau: Wildlife Strikes)
- Cluster analysis (Star Wars)
- Multivariate logistic model (Wildlife Strikes)
- Multivariate linear model (Global Burden of Disease)
- Mean hypothesis testing: one sample (IMDB) / two samples (London crime) / more than two samples (1-factor ANOVA for Financials PowerBI sample)
- Proportion hypothesis testing: one sample (University donations)
- Goodness of fit hypothesis testing (Superstore)
- Advanced quantitative technics such as ACF, PACF, EWMA, ARIMA, GARCH, Regression/Correlation Analysis, Machine Learning models, Black-Scholes model, and Monte Carlo simulation (Apple Stock Data)

## MISCELLANEOUS

MySQL - often used in my projects as an additional tool to analyze data. Below is the information for which projects certain SQL queries have been used:

- LOAD DATA INFILE (US crime, Eurovision, ATP, Wildlife Strikes)
- JSON_EXTRACT (Star Wars)
- joins (Covid19)
- CASE WHEN THEN ELSE (Eurovision, University donations)
- IF (Star Wars),
- (Window) ROW_NUMBER (Covid19, US Crime, College Donations, Eurovision),
- (Window) LAG (Apple Stock Data),
- ROUND, CONVERT, COALESCE,... (Star Wars, University donations, Apple Stock Data)
- stored procedure (Eurovision)

