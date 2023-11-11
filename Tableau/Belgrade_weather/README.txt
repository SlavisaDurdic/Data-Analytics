
TASK i.e. WHAT HAVE I DONE?

- Get data via API from: https://www.7timer.info/.
- Save data in .json format.
- Connect to the JSON file from Tableau.
- Build visuals in Tableau (https://public.tableau.com/app/profile/slavisadurdic/viz/BelgradeWeatherData/BelgradeWeatherData).


*** Tableau Activities ***

Instruction on how to use API for 7Timer! data is documented on website page: https://www.7timer.info/doc.php
For the analysis the machine-readable API has been used. Longitude and latitude parameters in API url have been defined to refer to Belgrade weather forecasts, i.e., http://www.7timer.info/bin/api.pl?lon=20.439&lat=44.836&product=astro&output=json
I have used the PostMan to make GET API calls, and I have saved the output as JSON data. Finally, I have connected to the file from Tableau to build visuals.
I have built a large number of pages/worksheets out of which I have created a dashboard.
Tableau dashboard has been saved and published on Tableau Public page: https://public.tableau.com/app/profile/slavisadurdic/viz/BelgradeWeatherData/BelgradeWeatherData 
I have mainly used line charts to display time series data. Those visuals show Belgrade weather forecast for a 3-day period, such as cloud cover, relative humidity, wind speed and direction, lift index, etc.
I created few calculated fields in order to get a datetime field I needed. Calculated Fields:
1) Time_calc_field
2) Date_calc_field
3) DateTime_calc_field
In addition to the mobile layout - a report view for mobile devices, I have also configured desktop and tablet layouts.
In Tableau Public server I configured this dashboard to show all worksheets created.
I was able to make some conclusions based on the visuals (for the observed time period and location):
1) As temperature goes down, cloudiness decreases too, and vice versa.
2) As temperature goes down, lifted index increases, and vice versa.
3) As temperature goes down, relative humidity decreases too, and vice versa.
