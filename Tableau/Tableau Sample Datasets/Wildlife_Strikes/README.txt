
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the Excel Wildlife Strikes file from https://public.tableau.com/app/learn/sample-data?qt-overview_resources=1#qt-overview_resources.
- Clean data, save as CSV, and use SQL queries to load the data to MySQL table(s).
- Execute some basic SQL queries.
- Build visuals in Tableau (https://public.tableau.com/app/profile/slavisadurdic/viz/WildlifestrikesinUS/US_Wildlife_Strikes).
- Run multivariate logistic regression model in Python as well as time series analysis in Tableau.


*** Python Activities ***

I have used python script "Logit Regression analysis - CSV, JSON or BigQuery - Wildlife_Strikes.py" (available in the project folder) to run statistical analysis (see Statistical Models section).


*** MySQL Activities ***

In MySQL I've performed below queries to create a table and insert the records from the CSV file:

	USE data_analysis; 
	CREATE TABLE wildlife_strikes (
		Airport_Code VARCHAR(4),
		Airport_Name VARCHAR(255), 
		Origin_State VARCHAR(50),
		Origin_State_Code VARCHAR(2),	
		Country VARCHAR(20),
		Aircraft_Type VARCHAR(20), 
		Aircraft_Number_of_engines INT,
		Collision_Date_and_Time DATETIME, 
		Time_of_day VARCHAR(50),
	    	Phase_of_flight VARCHAR(50),
	    	Amount_of_damage VARCHAR(50),
	    	Impact_to_flight VARCHAR(50),
	    	Indicated_Damage VARCHAR(50),
	    	Cost_Aircraft_time_out_of_service_hours INT,
	    	Cost_Total_$ INT,
	    	Days FLOAT,
	    	Feet_above_ground INT,
	    	Miles_from_airport INT,
	    	Animal_Category VARCHAR(50),
	    	Species_Order VARCHAR(50),
	    	Species_Group VARCHAR(255),
	    	Species VARCHAR(255),
	    	Species_ID VARCHAR(10),
	    	Number_of_Strikes INT,
	    	Record_ID INT
	);
	LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/faa_data_subset.csv"
	INTO TABLE wildlife_strikes
	FIELDS TERMINATED BY ',' 
	ENCLOSED BY '"'
	LINES TERMINATED BY '\n'
	IGNORE 1 ROWS;

Then, with below queries I have confirmed that:

- all rows have been successfully inserted into table(s).
	
	SELECT COUNT(*) FROM data_analysis.wildlife_strikes;

-- top 10 US states by $ damage cost:

	SELECT Origin_State, SUM(Cost_Total_$) AS Total_Cost
	FROM data_analysis.wildlife_strikes
	GROUP BY Origin_State
	ORDER BY SUM(Cost_Total_$) DESC
	LIMIT 10;

	> Origin_State	Total_Cost
	> New York	50278775
	> Colorado	30122696
	> California	29671432
	> Florida	26518650
	> Oregon	23203423
	> Alabama	14336223
	> Ohio		14328146
	> Utah		12242924
	> Nebraska	10611532
	> New Jersey	9175212


*** Tableau Activities ***

I have built a large number of pages/worksheets which I have combined into several dashboards. Then, I created a Tableau story page made of these dashboards. Different story captions support different project insights.
Tableau story report has been saved and published on Tableau Public page: https://public.tableau.com/app/profile/slavisadurdic/viz/WildlifestrikesinUS/US_Wildlife_Strikes 
I have used many different charts: map, scatter plot, bar, line, etc. Those visuals show number of animal strikes as well as aircraft damage costs by US states, different date and time units, animal species, and similar.
In order to make full interactivity, I've configured that some reports behave as filters.
I was able to make some conclusions based on the visuals:
1) 90% of all aircrafts due to wildlife strikes happened below or at 305 meters above ground during 2000-2015. That being said, phases of the flight that had been most affected are approach, landing roll, take-off run, and climb.
2) Normally, aircrafts were without any damage and had no impact on flights (also, 90% of the aircrafts caused no costs).
3) During the same period, only three accidents (caused by a White-tailed deer, Canada goose, and a Bald eagle) had a substantial damage or a destroyed plain vehicle worth more than 10 million dollars.
4) The number of strikes had been increasing during 2000-2015, nonetheless, Q3 appears to be a period with the largest number of wildlife-strike accidents reported. This may be due to some kind of bird migration season, or, most likely an increase of summertime flight traffic.
5) More than a third of total accidents in question happened in the following four US states: California, Texas, New York, and Florida. Again, these are most populated US states, which might be in relation with flight traffic.


*** Statistical Models *** 

> Multivariate Logistic Regression Analysis:

Although not very meaningful, I have performed multivariate logistic regression analysis in Python to demonstrate how model works. I have used sklearn python library "LogisticRegression" method to predict outcome based on several inputs (both, numeric and categorical). Also, from sklearn I have used "train_test_split" method to train and test the model. The script "Logit Regression analysis - CSV, JSON or BigQuery - Wildlife_Strikes.py" that I have created for this project is available in the project folder.

> Time Series:

In Tableau I have used the built-in forecast feature to predict number of strikes.
