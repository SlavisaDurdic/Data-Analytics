
TASK i.e. WHAT HAVE I DONE?

- Collect data by downloading the json Star Wars file from https://public.tableau.com/app/learn/sample-data?qt-overview_resources=1#qt-overview_resources.
- Load the JSON data to MySQL table(s).
- Execute some basic SQL queries.
- Build visuals in Tableau (https://public.tableau.com/app/profile/slavisadurdic/viz/StarWars_16943302674260/StarWars).
- Run regression analysis in Python as well as regression and cluster analyses in Tableau.


*** Python Activities ***

I have used python script "Regression analysis - CSV, JSON or BigQuery - StarWars.py" (available in the project folder) to run statistical analysis (see Statistical Models section).


*** MySQL Activities ***

In MySQL I've performed below queries and I have confirmed that:

- all rows have been successfully inserted into table(s).
	
	SELECT COUNT(*) FROM data_analysis.star_wars_characters;

- there are no duplicates as no value has been returned:
	
	WITH cte AS (
  		SELECT fields, model, pk,
    		ROW_NUMBER() OVER(PARTITION BY fields, model, pk) AS RN
  		FROM data_analysis.star_wars_characters
		)
	SELECT *
	FROM cte
	WHERE RN > 1;

- MAX and AVG values of "mass" and "height" actor attributes, grouped and ordered by eye_color:

	SELECT 
	    JSON_EXTRACT(fields, '$.eye_color') AS eye_color,
	    MAX(IF(JSON_EXTRACT(fields, '$.height')="unknown",0,CONVERT(JSON_EXTRACT(fields, '$.height'),DECIMAL))) AS max_height,
	    ROUND(AVG(JSON_EXTRACT(fields, '$.height')),4) AS average_height, -- average function works well with strings
	    IF(
			MAX(IF(JSON_EXTRACT(fields, '$.mass')="unknown",0,CONVERT(JSON_EXTRACT(fields, '$.mass'),DECIMAL)))=0,
	        "unknown", MAX(IF(JSON_EXTRACT(fields, '$.mass')="unknown",0,CONVERT(JSON_EXTRACT(fields, '$.mass'),DECIMAL)))
		) AS max_mass,
	    IF(
			ROUND(AVG(JSON_EXTRACT(fields, '$.mass')),4)=0,"unknown",ROUND(AVG(JSON_EXTRACT(fields, '$.mass')),4)
		) AS average_mass
	FROM data_analysis.star_wars_characters
	GROUP BY eye_color
	ORDER BY 1 DESC;
> eye_color 	max_height 	average_height 	max_mass 	average_mass
> "yellow"	264		177.8182	136		66.3636
> "white"	178		178		48		48
> "unknown"	193		136		48		31.5
> "red, blue"	96		96		unknown		unknown
> "red"		200		154.8		140		81.4
> "pink"	180		180		unknown		unknown
> "orange"	224		180.5		83		42.125
> "hazel"	178		174		77		66
> "green, yellow"216		216		159		159
> "gold"	191		191		unknown		unknown
> "brown"	193		158.95		85		42.96
> "blue-gray"	182		182		77		77
> "blue"	234		182.2105	136		54.6421
> "black"	229		185		88		59.3333


*** Tableau Activities ***

I have built a large number of pages/worksheets which I have combined into two dashboards. Then, I created a Tableau story page made of these two dashboards.
Tableau story report has been saved and published on Tableau Public page: https://public.tableau.com/app/profile/slavisadurdic/viz/StarWars_16943302674260/StarWars 
I have used many different charts: pie, scatter plot, bar, etc. Those visuals show dataset attribute distributions by genre, height, mass, eye color, as well as cluster analyses.
In order to make full interactivity, I've configured all reports as filters.
I was able to make some conclusions based on the visuals:
1) More than 73% of all Star Wars actors are men.
2) Mass and Height follow normal distribution.
3) Regression model is best described with power function (positive correlation, coefficient of determination is ~74%).


*** Statistical Models *** 

> Regression Analysis:

I have performed regression analysis in Python by using scatter plot (Mass vs. Height) as well as trend lenear and polynomial line charts from matplotlib, stats and numpy python libraries. I have used stats from scipy python library also to get linear model Correlation Coefficient and Coefficient of Determination. Additionally, I have used sklearn.metrics to get Coefficient of Determination of the applied polynomial model. Linear model results are Correlation coefficient = 0.7508581845938891, and Coefficient of determination = 0.5637880133716309. On the other hand, polynomial model slightly fit better as its Coefficient of determination is 0.5758349670407678. The script "Regression analysis - CSV, JSON or BigQuery - StarWars.py" that I have created for this project is available in the project folder.
I have also created scatter plot reports in Tableau to show relationship between Mass and Height. It seems that power function fits model better than any other function (linear, exponential, polynomial, logaritmic).

> Cluster Analysis:

I run Tableau built-in cluster analyses by specifying K-means (2 and 3).


