
TASK i.e. WHAT HAVE I DONE?

- Collect data from the “US_crime_original.xls” file and transform it into a usable form.
- Use SQL queries to load the data to a MySQL table or tables.
- Execute some basic sql queries to get first insights about the data.
- Build visuals in Power BI Desktop.
- Run regression analysis in Python.


*** Python Activities ***

I used python script "Simple regression analysis - US crime data.py" (available in the project folder) to run regression analysis (see Statistical Models section).


*** MySQL Activities ***

In MySQL I've performed queries to create a table and load the values from a csv file:

	USE data_analysis;
	CREATE TABLE US_crime (
		area VARCHAR(255),    
		event_year VARCHAR(50),   
		population DECIMAL,    
		violent_crime DECIMAL,  
		murder_and_nonnegligent_manslaughte DECIMAL,    
		rape_revised_definition DECIMAL,    
		rape_legacy_definition DECIMAL,    
		robbery DECIMAL,    
		aggravated_assault DECIMAL,    
		property_crime DECIMAL,    
		burglary DECIMAL,    
		larceny_theft DECIMAL,    
		motor_vehicle_theft DECIMAL
		);
	LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\US_crime.csv’
	INTO TABLE US_crime
	FIELDS TERMINATED BY ',’ 
	ENCLOSED BY '“’
	LINES TERMINATED BY '\n’
	IGNORE 1 ROWS;


With below queries I have confirmed that:

- all rows have been successfully inserted into the table.

	SELECT COUNT(*) FROM data_analysis.us_crime;

- it seems that there are no duplicates:
	
	WITH cte AS (
  		SELECT area, event_year, population, violent_crime, murder_and_nonnegligent_manslaughte, rape_legacy_definition, rape_revised_definition, robbery, aggravated_assault, property_crime, burglary, larceny_theft, motor_vehicle_theft,
    		ROW_NUMBER() OVER(PARTITION BY area, event_year, population, violent_crime, murder_and_nonnegligent_manslaughte, rape_legacy_definition, rape_revised_definition, robbery, aggravated_assault, property_crime, burglary, larceny_theft, motor_vehicle_theft) AS RN
  		FROM data_analysis.us_crime
		)
	SELECT *
	FROM cte
	WHERE RN > 1;

- California and Texas as the most populated areas also make the top crime US states in terms of daily average number of crime:

	SELECT area, AVG(population), SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft) AS total_crime, (SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft))/avg(population) AS avg_person_crime, (SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft))/(2*365) AS daily_avg_crime
	FROM data_analysis.us_crime
	GROUP BY area
	ORDER BY daily_avg_crime DESC, avg_person_crime DESC, total_crime DESC, area;

	> area				AVG(population)		total_crime	avg_person_crime	daily_avg_crime
	> United States Total6, 7, 8, 9	322012065.5000		37107773	0.1152			50832.5658
	> West6				76245644.0000		9780226		0.1283			13397.5699
	> South6, 7 ,8			121039206.0000		7839268		0.0648			10738.7233
	> South6, 7 ,9			122319574.0000		7777465		0.0636			10654.0616
	> Midwest6			67889908.0000		7245573		0.1067			9925.4425
	> Pacific6			52571831.5000		6690549		0.1273			9165.1356
	> West South Central6		39219968.5000		5305258		0.1353			7267.4767
	> California			39121978.5000		4756816		0.1216			6516.1863
	> Northeast6			56197123.5000		4465241		0.0795			6116.7685
	> South Atlantic6, 7, 8 	63192408.0000		3970121		0.0628			5438.5219
	> South Atlantic6, 7, 9		63923309.0000		3918856		0.0613			5368.2959
	> Texas				27646117.5000		3583631		0.1296			4909.0836

- on the other hand, New Mexico and Louisiana are top two states with respect to a number of committed crime per person:

	SELECT area, AVG(population), SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft) AS total_crime, (SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft))/avg(population) AS avg_person_crime, (SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft))/(2*365) AS daily_avg_crime
	FROM data_analysis.us_crime
	GROUP BY area
	ORDER BY avg_person_crime DESC;

	> area				AVG(population)		total_crime	avg_person_crime	daily_avg_crime
	> New Mexico6			2080671.5000		377203		0.1813			516.7164
	> Louisiana			4675313.0000		730170		0.1562			1000.2329
	> Alaska			739801.5000		115483		0.1561			158.1959
	> Arkansas			2983050.5000		457558		0.1534			626.7918
     	> South Carolina		4927976.5000		749632		0.1521			1026.8932

- the daily average crime for 2Y period 2015-2016 at the country level:

	SELECT (SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft))/(2*365) AS daily_avg_crime
	FROM data_analysis.us_crime
	WHERE area = 'United States Total6, 7, 8, 9';

	> daily_avg_crime_value
	> 50832.5658

- the daily average crime for 2Y period for state California and 3Y period 2015-2016 for London, respectively:

	SELECT (SUM(violent_crime)+SUM(murder_and_nonnegligent_manslaughte)+SUM(rape_legacy_definition)+SUM(rape_revised_definition)+SUM(robbery)+SUM(aggravated_assault)+SUM(property_crime)+SUM(burglary)+SUM(larceny_theft)+SUM(motor_vehicle_theft))/(2*365) AS daily_avg_crime
	FROM data_analysis.us_crime
	WHERE area LIKE '%California%'
	UNION
	SELECT SUM(value)/(3*365) as daily_avg_crime
	FROM data_analysis.bigquery_london_crime_crime_by_lsoa;

	> daily_avg_crime
	> 6516.1863
	> 1943.3132


*** PowerBI Activities ***

I have built 2 pages/reports which included many different charts: pie, matrix, and bar visuals. Those visuals mostly show a number of committed crime in the US during the 2Y period 2015-2016 by type and US states.
In order to emphasize the interactivity, I've added slicer visual "event_year" which helped in analyzing the US crime data.
I have also configured the mobile layout - a report view for mobile devices.
I was able to make some conclusions based on the visuals:
1) Overall, crime situation remained the same in 2016 compared to statistics from year 2015.
2) Almost 74% of crime fall under “property crime” and “larceny theft”.
3) California, Texas, and Florida were the US states with the most criminal activities reported in the given period.
4) New Mexico, Louisiana, Alaska, Arkansas, and South Carolina on the other hand had the highest number of crime committed per person.
5) California appears to be a less dangerous place than London, as its daily average of crime was ~6500 for about 40MM of people, while London's daily average of crime was ~2000 for about 9MM of people.


*** Statistical Models *** 

> Regression Model:

I have performed regression analysis in Python by using scatter plot (Violent crime vs. Murder...) and trend line charts from matplotlib python library. Additionally, I have used stats from scipy python library to get Correlation Coefficient and Coefficient of Determination. The script "Simple regression analysis - US crime data.py" that I have created for this project is available in the project folder. Model results are Correlation coefficient = 0.9946739411964045, and Coefficient of determination = 0.9893762492951884.
