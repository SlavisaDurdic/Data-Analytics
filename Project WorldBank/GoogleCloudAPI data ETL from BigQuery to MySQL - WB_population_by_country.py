# MAKE SURE TO PROVIDE CORRECT INFO FOR db_query AND sql_table DATA
# ---> LINES 20 AND 23

import os
from google.cloud import bigquery
import mysql.connector as mysql
from mysql.connector import Error
import time
import datetime
import math

start = time.time()
print(f'The script started on {datetime.datetime.now()}...')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'

client = bigquery.Client()

# Enter a name of the MySQL table, e.g. 'bigquery_imdb_title_basics'
sql_table = 'bigquery_WB_global_population_by_country'

# Write an sql query to pool values from BigQuery
db_query = """
        SELECT * FROM `bigquery-public-data.world_bank_global_population.population_by_country`;
     """

query_job = client.query(db_query)  # API request
rows = query_job.result()  # Waits for query to finish

print('Downloading values and populating the lists...')
colName = []
sqlValues = []
for row in list(rows):
    colName.append(row.keys())
    sqlValues.append(row.values())
colName_filtered = list(colName[0])
download_time = time.time()
print(f"The download time finished in {download_time - start} seconds "
      f"(i.e. ~ {math.floor((download_time - start) / 3600)} hours and "
      f"{round((((download_time - start) / 3600)-(math.floor((download_time - start) / 3600))) * 60)} minutes)..."
      )

# Generating the date column
date = []
for i in range(1960,2020,1):
    date.append(i)

# Country code and year vectors
only_country_code = []
only_year_values = []
for i in range(len(sqlValues)):
    only_year_values.append(sqlValues[i][2:])
    only_country_code.append(sqlValues[i][1])

print(f'Number of original country code list = {len(only_country_code)}')
print(f'Number of original year list = {len(only_year_values)}')

only_year_values.pop(only_country_code.index('AND'))
only_country_code.remove('AND')
print(f'Number of corrected country code list = {len(only_country_code)}')
print(f'Number of corrected year list = {len(only_year_values)}')

print(f'Number of year list at index [0], i.e. number of years = {len(only_year_values[0])}')

print('Establishing the connection with MySQL server...')

try:
    conn = mysql.connect(host='localhost', database='<database>', user='<user>', password='<password>')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute(f'DROP TABLE IF EXISTS {sql_table};') # This implies the table creation from scratch
        print('Creating table...')
        cursor.execute(f"CREATE TABLE {sql_table}(helper_id INT NOT NULL);") # This column serves as a dummy value
        print("Adding columns to the table...")
        cursor.execute(f"ALTER TABLE {sql_table} ADD COLUMN date INT")
        for col in only_country_code:
            cursor.execute(f"ALTER TABLE {sql_table} ADD COLUMN {col} DECIMAL")
        insert_values_time = time.time()
        print('Inserting records into the sql table...')
        number_of_records = 0
        for j in range(len(only_year_values[0])):
            values = []
            values.append(j)
            values.append(date[j])
            for i in only_country_code:
                if only_year_values[only_country_code.index(i)][j] is None:
                    values.append(0)
                else:
                    values.append(only_year_values[only_country_code.index(i)][j])
            cursor.execute(f"INSERT INTO data_analysis.{sql_table} VALUES {tuple(values)}")
            number_of_records = number_of_records + 1
            # The connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
        print(f"{number_of_records} records are inserted...")
except Error as e:
    print("Error - ", e)

end = time.time()
print(f"The insert activity finished in {end - insert_values_time} seconds "
      f"(i.e. ~ {math.floor((end - insert_values_time) / 3600)} hours and "
      f"{round((((end - insert_values_time) / 3600)-(math.floor((end - insert_values_time) / 3600))) * 60)} minutes)..."
      )
print(f"Script ended in {end - start} seconds (i.e. ~ "
      f"{math.floor((end - start) / 3600)} hours and {round((((end - start) / 3600) - (math.floor((end - start) / 3600))) * 60)} minutes)..."
      )