# Data-Analytics
My portfolio of public dataset analysis/analytics.

This GitHub repository contains four folders: Scripts, PowerBI, Tableau, and Looker Studio.\
Under the **Scripts** folder you can find last-updated python scripts for the ETL process and statistical modeling.\
Under **PowerBI**, **Tableau**, and **Looker Studio** folders (each representing a different BI tool) you can find many *PROJECT* folders. Each project folder is created for a specific dataset analysis, and mainly consists of:

- readme text file with detailed description about the project,
- Microsoft Power Point file with up to 15 slides that summarizes the project,
- Power BI file(s) or Tableau or Looker Studio link (specified within the project's readme file) as a BI tool for visualizing data,
- python script used to pull data from BigQuery (or CSV) and load it into MySQL database,
- other files, such as python files for hypothesis testing, regression analysis, or similar.
  
******

## PROJECT CLASSIFICATION

Analyzed topics can be classified as below:
> Business:

- Superstore Sales [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Superstore)
- Financials [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20PowerBI%20Financials)
- Startup Venture Funding [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Technology%20-%20Startup%20Venture%20Funding)
- Microsoft Financial Report [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/MSFT)
 
> Entertainment:

- Eurovision 1998 to 2010 [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Eurovision)
- Star Wars Character Details [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Star_Wars)
- IMDB [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20IMDB)

> Sports:

- ATP Top-Ranked Singles Tennis Players [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/ATP)

> Public Data:

- FAA Wildlife Strikes, 2015 [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Wildlife_Strikes)
- U.S. Home Sales, 1963-2016 [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Government%20-%20Home%20Sales)
- London crime [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20LondonCrime)
- US crime [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20US_crime)
- World Bank population [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20WorldBank)

> Education:

- University Advancement, Donations, and Giving [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/US_College_Donations)

> Science:

- Significant Volcanic Eruptions [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Science%20-%20Volcano%20Eruptions)

> Health:

- U.S. County Health Rankings (... not started yet)
- Covid19 [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20Covid19)

## DATA COLLECTION

Data has been collected in different formats:
- Excel (for example, Superstore and Eurovision are projects that use this data type)
- CSV (for example, ATP is a project that uses this data type)
- JSON (for example, Star Wars is a project that uses this data type)
- PDF (for example, MSFT Income Statement is a project that uses this data type)
- BigQuery (PowerBI datasets are based on BigQuery tables)
- MySQL database (served as a destination database for PowerBI datasets, but also used for Tableau dataset analyses)

## DATA CLEANSING

Not all datasets were ready for use, so more or less of data cleaning was required now and then, which has been done via different tools:
- Excel / CSV (US crime, Wildlife Strikes)
- Python (World Bank population)
- Tableau (MSFT Income Statement) / PowerBI (London crime) / Looker Studio (Startup Venture Funding)

## DATA ANALYSIS AND VISUALIZATION

For data analysis and visualization PowerBI, Tableau, Looker Studio, and/or MySQL and Python have been used.
While analyzing data, STATISTICAL modeling technics listed below has been performed:

- Simple regression model (covid19, Financials PowerBI sample, US crime, Eurovision, Star Wars)
- Time series (PowerBI: London crime, WB population; Tableau: Wildlife Strikes)
- Cluster analysis (Star Wars)
- Multivariate logistic model (Wildlife Strikes)
- Mean hypothesis testing: one sample (IMDB) / two samples (London crime) / more than two samples (1-factor ANOVA for Financials PowerBI sample)
- Proportion hypothesis testing: one sample (University donations)
- Goodness of fit hypothesis testing (Superstore)

## MISCELLANEOUS

MySQL - often used in my projects as an additional tool to analyze data. Below is the information for which projects certain SQL queries have been used:
- LOAD DATA INFILE (US crime, Eurovision, ATP, Wildlife Strikes)
- JSON_EXTRACT (Star Wars)
- joins (Covid19)
- CASE WHEN THEN ELSE (Eurovision, University donations)
- IF (Star Wars)
- ROUND, CONVERT... (Star Wars, University donations)
- stored procedure (Eurovision)

