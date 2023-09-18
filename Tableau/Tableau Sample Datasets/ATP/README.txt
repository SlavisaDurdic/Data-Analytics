
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the Excel file from https://public.tableau.com/app/learn/sample-data?qt-overview_resources=1#qt-overview_resources.
- Use SQL queries to load the data to MySQL table(s).
- Execute some basic SQL queries.
- Build visuals in Tableau (https://public.tableau.com/app/profile/slavisadurdic/viz/ATPRankingSingles/ATPDashboard).


*** MySQL Activities ***

In MySQL I've performed queries to create a table and load the values from a csv file:

	USE data_analysis;
	CREATE TABLE atp (	
	    player VARCHAR(50),     DOB VARCHAR(50),
	    cumulative_weeks INT,    w_date VARCHAR(50),
	    sex VARCHAR(10),	weeks INT,
	    age_days INT,    age_years INT,
	    age_decimal DECIMAL(5,2)
	);
	LOAD DATA INFILE "atp_number_1.csv"
	INTO TABLE atp
	FIELDS TERMINATED BY ',' 
	LINES TERMINATED BY '\n'
	IGNORE 1 ROWS;

With below queries I have confirmed that:

- all rows have been successfully inserted into table(s).
	
	SELECT COUNT(*) FROM data_analysis.atp;

- there are no duplicates as no value has been returned:
	
	WITH cte AS (
  		SELECT player, DOB, cumulative_weeks, w_date, sex, weeks, age_days, age_years, age_decimal,
    		ROW_NUMBER() OVER(PARTITION BY player, DOB, cumulative_weeks, w_date, sex, weeks, age_days, age_years, age_decimal) AS RN
  		FROM data_analysis.atp
		)
	SELECT *
	FROM cte
	WHERE RN > 1;

- 10 youngest number one tennis players from 1973 to 2018:

	SELECT player, sex, MIN(age_decimal) FROM atp GROUP BY player, sex ORDER BY MIN(age_decimal) LIMIT 10;

	> player		sex	MIN(age_decimal)
	> Martina Hingis 	Female 	16.50
	> Monica Seles		Female	17.27
	> Tracy Austin		Female	17.32
	> Steffi Graf		Female	18.17
	> Maria Sharapova	Female	18.34
	> Kim Clijsters		Female	20.18
	> Ana Ivanovic		Female	20.20
	> Caroline Wozniacki	Female	20.25
	> Lleyton Hewitt	Male	20.76
	> Serena Williams	Female	20.78

- 10 tennis players from 1973 to 2018 with a best score of consecutive weeks as ATP number one:

	SELECT player, sex, MAX(weeks) FROM atp GROUP BY player, sex ORDER BY MAX(weeks) DESC LIMIT 10;

	> player		sex	MAX(weeks)
	> Roger Federer		Male	237
	> Steffi Graf		Female	186
	> Serena Williams	Female	186
	> Jimmy Connors		Male	160
	> Ivan Lendl		Male	157
	> Martina Navratilova	Female	156
	> Novak Djokovic	Male	122
	> Chris Evert		Female	113
	> Pete Sampras		Male	102
	> Monica Seles		Female	91


*** Tableau Activities ***

I have built a large number of pages/worksheets which I have combined into one dashboard. Tableau dashboard has been saved and published on Tableau Public page: https://public.tableau.com/app/profile/slavisadurdic/viz/ATPRankingSingles/ATPDashboard 
I have used many different charts: table, bar, line, area, and treemap. Those visuals show ATP top-ranked singles tennis players for the period 1973-2018 by average age, level of competitiveness or dominance of certain tennis players over time, as well as number of total and consecutive weeks as world's best tennis player. Visuals can be filtered by Sex, but data can also be broken down further by players listed on visuals.
I was able to make some conclusions based on the visuals:
1) The youngest ATP (male) number one tennis player between 1973 and 2018 was Lleyton Hewitt (age 20.76), while the youngest WTA (female) number one tennis player for the same period was Martina Hingis (age 16.5).
2) Average age of all tennis players ranked as number one for the period 1973-2018 was 24.7.
3) Roger Federer was the best tennis player during the observed period in terms of number of consecutive weeks (=237) holding first place on the list.
4) Steffi Graf was the best tennis player during the observed period in terms of total number of weeks (=337) holding first place on the list.
5) WTA number one position was unstable most in year 1995 (3 players interchangeably switched No. 1 position for 8 times), while ATP number one position was disturbed most in year 1983 (3 players interchangeably switched No. 1 position for 10 times).
