
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the "bigquery-public-data.imdb.title_basics“ and "bigquery-public-data.imdb.title_ratings" datasets available on BigQuery.
- Load the data to a MySQL table or tables.
- Execute some basic sql queries to get first insights about the data.
- Build visuals in Power BI Desktop.
- Run statistical models.


*** Python Activities ***

For the ETL processes, I have used Python programming language and accordingly the "Python Client for Google BigQuery" Google Cloud official documentation reference (https://cloud.google.com/python/docs/reference/bigquery/latest).

I've generated a python script in PyCharm integrated development environment - "GoogleCloudAPI data ETL from BigQuery to MySQL - imdb.py" (which is available in the GitHub project folder) in order to automate the process as much as possible. Users should edit lines 22 and 25 of the script, i.e. users need to 1) provide information about the MySQL table name which will be created in the database, and 2) define sql query to pull data from, say, "bigquery-public-data.imdb.title_basics" dataset on BigQuery.

You can notice different python libraries imported to my .py file, such as pandas (... to work with dataframes), mysql.connector (... to connect to and load data into a mySQL database), and decimal (due to the formating reasons).

Table "bigquery-public-data.imdb.title_basics" consists of 9 columns. I aimed to add one more, which I did, so I could execute the "CREATE TABLE" sql command in the first place. This additional column is a sort of an id column, and I named it "helper_id". The same goes for the table "bigquery-public-data.imdb.title_ratings", which consists of 3+1 columns.

The code is written in order to get everything done from scratch: create a new table and insert all records. Note: It is not configured to support incremental activities.

Once uploaded, please note that 1.325.156 and 10.006.902 records are saved in the "publicbigquery_imdb_title_ratings" and the "publicbigquery_imdb_title_basics" tables, respectively. The size of the table is 1.1 GB each.


*** MySQL Activities ***

In MySQL I've performed queries and confirmed that:

- all rows have been successfully inserted into both tables.

	SELECT COUNT(*) FROM data_analysis.publicbigquery_imdb_title_basics;
	SELECT COUNT(*) FROM data_analysis.publicbigquery_imdb_title_ratings;

- it seems that there are no duplicates (this QUERY has been performed directly on BigQuery due to the performance issues):
	
	WITH cte AS (
  		SELECT tconst, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres,
    		ROW_NUMBER() OVER(PARTITION BY tconst, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres) 		AS RN
  		FROM data_analysis.publicbigquery_imdb_title_basics
		)
	SELECT *
	FROM cte
	WHERE RN > 1;

- count of unique genres:

	SELECT COUNT(DISTINCT(genres)) as number_of_unique_genres FROM data_analysis.publicbigquery_imdb_title_basics;

	> number_of_unique_genres
	> 2339

- the last 5 commedies:

	SELECT tconst, title_type, primary_title, is_adult, start_year, end_year, runtime_minutes, genres FROM 	data_analysis.publicbigquery_imdb_title_basics
	WHERE genres = 'Comedy'
	ORDER BY start_year DESC
	LIMIT 5;

	> tconst 	title_type 	primary_title 	 		is_adult 	start_year end_year runtime_minutes 	genres
	> tt13984170	movie		C.O.M.M.U.N.I.C.A.T.I.O.N.	0		2025					Comedy
	> tt27897848	tvMovie		Way 2 Go Bistro			0		2025					Comedy
	> tt12929950	movie		Bakom varje man			0		2025					Comedy
	> tt27385073	movie		The Devil Who Threw Fire	0		2025			95		Comedy
	> tt11742154	movie		SUBWAY! the movie		0		2025					Comedy

- the average title rating:

	SELECT AVG(average_rating) as average_rating
	FROM data_analysis.publicbigquery_imdb_title_ratings;

	> average_rating
	> 6.9545820325695695

- average ratings for some genres:

	SELECT genres, AVG(average_rating) AS average_rating
	FROM data_analysis.publicbigquery_imdb_title_basics tb
	JOIN data_analysis.publicbigquery_imdb_title_ratings tr
	ON tb.tconst = tr.tconst
	WHERE genres IN ('Horror', 'Comedy', 'Action')
	GROUP BY genres
	ORDER BY AVG(average_rating) DESC;
	
	> genres 	average_rating
	> Comedy	6.905865066714559
	> Action	6.115749630377521
	> Horror	5.058645758206431


*** PowerBI Activities ***

I have built 5 pages/reports which included many different charts: card, matrix, bar, waterfall, treemap, and line visuals. Those visuals mostly show top imdb titles' average rating and runtime in minutes by genres and/or title type; quality and popularity of titles classified by decades, and similar.
In order to emphasize the interactivity, I've added slicer visuals, or I have simply filtered pages by: "genres", "start_year", and "title_type" which help in analyzing the imdb data from various aspects.
I was able to make some conclusions based on the visuals:
1) Overall, the majority of movies fall under the "Drama", "Comedy", and "Horror", respectively.
2) Similar to the previous point, the highest number of votes, on average, go to the "Comedy", "Horror", and "Drama", respectively. If we assume that there is a positive linear correlation between number of votes and people watching this, we can set user preferences about the genres.
3) With respect to above, if we want to make a movie, we can decide to go with a comedy, as a less risky option. We can see that there is a significant increase in number of comedies in the last two decades. Furthermore, it seems that the most popular comedies are those made in period 1999-2005. We can filter by these parameters to check further which movies have the best average rating (on the other hand, please note that the average rating of all comedies is 5.73, lower than the global title average of 6.95). For example, we can decide to make a movie similar to one of the 10 bellow titles:
	- A Most Particularly Peculiar Bank Heist
	- Gangstacity
	- Down Into Happiness
	- Murir Tin
	- Humanoid
	- A Joyce Story
	- Love Lessons
	- Unsung
	- Soliloquy
	- Unsong Heroes


*** Statistical Models *** 

I have performed hypothesis testing over imdb sample data in Python, defining the null hypothesis as shown bellow.

> Null hypothesis (H0): Average rating of all titles is precisely 7;
> Alternative hypothesis (H1): Average rating of all titles is different from 7;

There is a python script "Hypothesis testing applied on public BigQuery data - imdb" that I created and that can be found in the project folder. The decision on accepting or rejecting the HO was based on a critical value method, and the final output is that with the confidence level of 95% we have enough evidence in the sample to reject the null hypothesis.

