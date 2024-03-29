## Repository Description:

This GitHub repository hosts a collection of data analyses performed on publicly available datasets, covering a diverse range of topics and utilizing various data formats and sources. The repository is organized into four main folders: Scripts, PowerBI, Tableau, and Looker Studio.

**Scripts Folder:**

- Contains Python scripts used for ETL processes and statistical modeling.
- Provides a historical record of the last-updated scripts.

**PowerBI, Tableau, and Looker Studio Folders:**

- Each folder represents a different Business Intelligence (BI) tool.
- Project folders within these directories are created for specific dataset analyses, featuring detailed descriptions, presentation slides, BI tool links, data extraction scripts, and other relevant files.

This repository serves as a comprehensive resource for data enthusiasts, showcasing real-world applications of data analysis across different domains and technologies. Feel free to explore the folders and projects to gain insights into the methodologies and techniques employed in each analysis.

## Project Classification:

Projects are categorized into business, entertainment, public data, and science topics, with specific examples listed under each category. Each project includes BI tool views for easy exploration.

- Business:

> Superstore Sales [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/Tableau%20Sample%20Datasets/Superstore) \
> Financials [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20PowerBI%20Financials) \
> Startup Venture Funding [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Tableau%20Datasets%20used%20for%20Looker/Technology%20-%20Startup%20Venture%20Funding) \
> Microsoft Financial Report [View this report in Tableau](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Tableau/MSFT) \
> Apple Stock Data [View this report in Looker Studio](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/Looker%20Studio/Apple_Stocks)
> Superstore [View this report in Power BI](https://github.com/SlavisaDurdic/Data-Analytics/tree/main/PowerBI/Project%20Superstore)
 
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

## Data Collection and Cleaning:

Data is sourced from various formats, including Excel, CSV, JSON, PDF, URL, REST API, Yahoo Finance, BigQuery, and MySQL. Data cleansing is performed using tools like Excel, CSV, Python, Tableau, PowerBI Power Query, and Looker Studio.

Datasources:
- Excel (for example, Superstore and Eurovision are projects that use this data type)
- CSV (for example, ATP and Apple Stock Data are projects that use this data type)
- JSON (for example, Star Wars and Belgrade Weather are projects that uses this data type)
- PDF (for example, MSFT Income Statement is a project that uses this data type)
- URL (for example, Animal Speed is a project that uses data from this datasource)
- REST API (for example, Belgrade Weather is a project that uses data from this datasource)
- Yahoo Finance via yfinance python library (for example, Apple Stock Data is a project that uses this datasource)
- BigQuery (PowerBI datasets are based on BigQuery tables)
- MySQL database (served as a destination database for PowerBI datasets, but also used for Tableau and Looker dataset analyses)

Data Cleansing:
- Excel / CSV (US crime, Wildlife Strikes)
- Python (World Bank population, Apple Stock Data)
- Tableau (MSFT Income Statement, Belgrade Weather) / PowerBI Power Query (London crime, Animal Speed) / Looker Studio (Startup Venture Funding)

## Data Analysis and Visualization:

Statistical modeling techniques are applied using PowerBI, Tableau, Looker Studio, MySQL, and Python.
Examples of techniques include simple regression, time series analysis, cluster analysis, multivariate logistic and linear models, hypothesis testing, and advanced quantitative methods (ACF, PACF, EWMA, ARIMA, GARCH, Regression/Correlation Analysis, Machine Learning models, Black-Scholes model, Monte Carlo simulation).

- Simple regression model (covid19, Financials PowerBI sample, US crime, Eurovision, Star Wars)
- Time series (PowerBI: London crime, WB population; Tableau: Wildlife Strikes)
- Cluster analysis (Star Wars)
- Multivariate logistic model (Wildlife Strikes)
- Multivariate linear model (Global Burden of Disease)
- Mean hypothesis testing: one sample (IMDB) / two samples (London crime) / more than two samples (1-factor ANOVA for Financials PowerBI sample)
- Proportion hypothesis testing: one sample (University donations)
- Goodness of fit hypothesis testing (Superstore)
- Advanced quantitative technics such as ACF, PACF, EWMA, ARIMA, GARCH, Regression/Correlation Analysis, Machine Learning models, Black-Scholes model, and Monte Carlo simulation (Apple Stock Data)

## Miscellaneous:

MySQL is frequently utilized as an additional tool for data analysis.
Specific SQL queries are mentioned for projects where MySQL was applied, including LOAD DATA INFILE, JSON_EXTRACT, joins, CASE WHEN THEN ELSE, IF, ROW_NUMBER, LAG, and various functions like ROUND, CONVERT, COALESCE, etc.

- LOAD DATA INFILE (US crime, Eurovision, ATP, Wildlife Strikes)
- JSON_EXTRACT (Star Wars)
- joins (Covid19)
- CASE WHEN THEN ELSE (Eurovision, University donations)
- IF (Star Wars),
- (Window) ROW_NUMBER (Covid19, US Crime, College Donations, Eurovision),
- (Window) LAG (Apple Stock Data),
- ROUND, CONVERT, COALESCE,... (Star Wars, University donations, Apple Stock Data)
- stored procedure (Eurovision)

