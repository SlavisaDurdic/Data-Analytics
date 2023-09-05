
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the Excel file from https://public.tableau.com/app/learn/sample-data?qt-overview_resources=1#qt-overview_resources.
- Use SQL queries to load the data to MySQL table(s).
- Execute some basic SQL queries.
- Build visuals in Tableau (https://public.tableau.com/app/profile/slavisadurdic/viz/EurovisionSampleDataset/StoriesofEurovision).
- Run regression analysis in Python.


*** Python Activities ***

I used python script "Simple regression analysis - CSV or BigQuery - eurovision.py" (available in the project folder) to run statistical analysis (see Statistical Models section).


*** MySQL Activities ***

In MySQL I've performed queries to create a table and load the values from a csv file:

	USE data_analysis;
	CREATE TABLE eurovision (	
	    id INT,    year VARCHAR(255),
	    country VARCHAR(255),    region VARCHAR(255),
	    artist VARCHAR(255),    song VARCHAR(255),
	    artist_gender VARCHAR(255),    group_solo VARCHAR(255),
	    place INT,    points INT,
	    home_away_country VARCHAR(255),    home_away_region VARCHAR(255),
	    is_final BOOLEAN,    semi_final_number VARCHAR(255),
	    song_in_english BOOLEAN,    song_quality VARCHAR(255),
	    normalized_points VARCHAR(255),    energy VARCHAR(255),
	    duration VARCHAR(255),    acousticness VARCHAR(255),
	    danceability VARCHAR(255),    tempo VARCHAR(255),
	    speechiness VARCHAR(255),    key_field VARCHAR(255),
	    liveness VARCHAR(255),    time_signature VARCHAR(255),
	    mode_field VARCHAR(255),    loudness VARCHAR(255),
	    valence VARCHAR(255),    happiness VARCHAR(255)
	);
	LOAD DATA INFILE ‘eurovision.csv’
	INTO TABLE eurovision 
	FIELDS TERMINATED BY ',’ 
	LINES TERMINATED BY '\n’
	IGNORE 1 ROWS;

With below queries I have confirmed that:

- all rows have been successfully inserted into table(s).
	
	SELECT COUNT(*) FROM data_analysis.eurovision;

- there are no duplicates as no value has been returned:
	
	WITH cte AS (
  		SELECT id,year,country,region,artist,song,artist_gender,group_solo,place,points,home_away_country,home_away_region,is_final,semi_final_number,song_in_english,song_quality,normalized_points,energy,duration,acousticness,danceability,tempo,speechiness,key,liveness,time_signature,mode,loudness,valence,happiness,
    		ROW_NUMBER() OVER(PARTITION BY id,year,country,region,artist,song,artist_gender,group_solo,place,points,home_away_country,home_away_region,is_final,semi_final_number,song_in_english,song_quality,normalized_points,energy,duration,acousticness,danceability,tempo,speechiness,key,liveness,time_signature,mode,loudness,valence,happiness) 		AS RN
  		FROM data_analysis.eurovision
		)
	SELECT *
	FROM cte
	WHERE RN > 1;

- NULLS, i.e., missing data has been inserted into the table as empty strings (''). Let's take for example column 'energy' - there are 166 fields with no data:

	SELECT SUM(energy), AVG(energy), COUNT(energy),
		SUM(CASE WHEN energy = '' THEN 1 ELSE 0 END) AS energy_nulls,
		SUM(energy)/SUM(CASE WHEN energy = '' THEN 0 ELSE 1 END) AS energy_real_average
	FROM data_analysis.eurovision;

- Eurovision winners from 1998 to 2012:

	SELECT year, country, artist, song, song_in_english, song_quality, points, normalized_points, energy
	FROM data_analysis.eurovision
	WHERE place = 1 AND is_final = TRUE
	ORDER BY year ASC;
> year 	country   	artist 				song 			song_in_english song_quality 	points 	normalized_points 	energy
> 1998	Israel    	Dana International		Diva			0		7.43620234	172	0.11862069		0.917373616
> 1999	Sweden		Charlotte Nilsson		Take Me to Your Heaven	1		7.010302826	163	0.122188906	
> 2000	Denmark		Olsen Brothers			Fly on the Wings of Love1		7.721898656	195	0.140086207		0.808926966
> 2001	Estonia		Tanel Padar Dave Benton 2XL	Everybody		1		8.741044234	198	0.148425787		
> 2002	Latvia		Marie N				I Wanna			1		7.414184709	176	0.126436782		0.592708255
> 2003	Turkey		Sertab Erener			Everyway That I Can	1		6.950406189	167	0.110742706		0.85871643
> 2004	Ukraine		Ruslana				Wild Dances		1		8.127321796	280	0.134099617		0.775246205
> 2005	Greece		Helena Paparizou		My Number One		1		5.918859955	230	0.101679929		0.747970671
> 2006	Finland		Lordi				Hard Rock Hallelujah	1		7.912414527	292	0.132486388		0.948509358
> 2007	Serbia		Marija ?erifovi?		Molitva			0		6.113882935	268	0.11001642		0.959497665
> 2008	Russia		Dima Bilan			Believe			1		6.096743694	266	0.109061748		0.514368
> 2009	Norway		Alexander Rybak 		Fairytale		1		9.475032644	387	0.158866995		0.686648351
> 2010	Germany		Lena				Satellite		1		6.526584934	246	0.108897742		0.776138483
> 2011	Azerbaijan	Ell & Nikki			Running Scared		1		5.197069278	221	0.08861267		0.745659542
> 2012	Sweden		Loreen				Euphoria		1		9.116166197	372	0.15270936		0.649941718

Just as an example, below query creates a stored procedure in MySQl which goas is to return N-number of Eurovision song winners rated by song quality (there are 15 winners in total, so it is the maximum number of row results that query can provide, even if the input value is higher than 15):

	DELIMITER //
	CREATE DEFINER=`root`@`localhost` PROCEDURE `eurovision_top_n_winners_by_quality`(IN n INT)
	BEGIN
		SELECT year, country, artist, artist_gender, group_solo, song, song_in_english, song_quality, points, normalized_points, energy
		FROM data_analysis.eurovision
		WHERE place = 1 AND is_final = TRUE
		ORDER BY song_quality DESC
	    LIMIT n;
	END //
	DELIMITER ;
	-- Call stored procedure (input parameter = 5)
	CALL data_analysis.eurovision_top_n_winners_by_quality(5);


*** Tableau Activities ***

I have built a large number of pages/worksheets which I have combined into two dashboards. Then, I created a Tableau story page made of these two dashboards.
Tableau story report has been saved and published on Tableau Public page: https://public.tableau.com/app/profile/slavisadurdic/viz/EurovisionSampleDataset/StoriesofEurovision 
I have used many different charts: pie, map, scatter plot, bar, etc. Those visuals show Eurovision song contest winners for the period 1998-2012 as well as average country placement, native vs. English language structure, artist gender structure, top artists/countries by points and some other metrics.
In order to observe data changes/evolution/insights and so, I've activated filters "Year" and "Artist" (this one determined by a parameter "Top N artists") for some of my reports.
I was able to make some conclusions based on the visuals:
1) Sweden appears to be the only country that managed to repeat the success during the analyzed period - Sweden took first place in year 1999 and 2012.
2) Generally, Eurovision songs have been sung in English - btw. there are only two winning songs sung in their native language (Israel: year 1999, and Serbia: year 2007).
3) Interestingly, Azerbaijan, Italy, and Serbia turned out to be the best performing countries in term of the average placement.
4) Song quality from Echonest, together with many other metrics, remained stable during the observed period.
5) Singers are more or less equally distributed by gender, as well as finalists by stage energy and danceability.


*** Statistical Models *** 

> Regression Analysis:

I have performed regression analysis in Python by using scatter plot (Place vs. Song.Quality) and trend line charts from matplotlib python library. Additionally, I have used stats from scipy python library to get Correlation Coefficient and Coefficient of Determination. The script "Simple regression analysis - CSV or BigQuery - eurovision.py" that I have created for this project is available in the project folder. Model results are Correlation coefficient = -0.901079563161771, and Coefficient of determination = 0.8119443791478079.


