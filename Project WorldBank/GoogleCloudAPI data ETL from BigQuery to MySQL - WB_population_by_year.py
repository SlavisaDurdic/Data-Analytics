# MAKE SURE TO PROVIDE CORRECT INFO FOR db_query AND sql_table DATA
# ---> LINES 22 AND 25

import os
from google.cloud import bigquery
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error
import time
import datetime
import decimal
import math

start = time.time()
print(f'The script started on {datetime.datetime.now()}...')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'file.json'

client = bigquery.Client()

# Enter a name of the MySQL table, e.g. 'bigquery_imdb_title_basics'
sql_table = 'bigquery_WB_global_population_by_year'

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
df_colName = pd.DataFrame(colName)
df_sqlValues = pd.DataFrame(sqlValues)
colName_filtered = list(colName[0])
df_sqlValues.columns = list(colName[0])
df_sqlValues.insert(0, "helper_id", range(len(sqlValues)))
download_time = time.time()
print(f"The download time finished in {download_time - start} seconds "
      f"(i.e. ~ {math.floor((download_time - start) / 3600)} hours and "
      f"{round((((download_time - start) / 3600)-(math.floor((download_time - start) / 3600))) * 60)} minutes)..."
      )

# # Removing countries with integer values exceeding mysql upper limitation of 2.288.665.962 (although in the official MySQL documentation it is stated to be 2.147.483.647)
# excluding_countries = []
# excluding_countries_index = []
# for i in range(df_sqlValues.shape[0]): # Number of dataframe rows
#     for j in range(df_sqlValues.shape[1]): # Number of dataframe columns
#         if type(df_sqlValues.loc[i][j]) is not str:
#             if df_sqlValues.loc[i][j] is not None:
#                 if (df_sqlValues.loc[i][j] > 2288665962):
#                     excluding_countries.append(df_sqlValues.loc[i]['country_code'])
#                     excluding_countries_index.append(i)
# print(f'These countries contain integer values that exceed MySQl upper limit of 2.288.665.962:'
#       f' \n{set(excluding_countries)}. \nTherefore, {len(set(excluding_countries))} rows (indices: {set(excluding_countries_index)}) have been removed from the dataframe.')
# df_sqlValues = df_sqlValues.drop(set(excluding_countries_index))

# # Country code and year vectors/lists
# only_country_code = []
# only_year_values = []
# for i in range(len(sqlValues)):
#     only_year_values.append(sqlValues[i][2:])
#     only_country_code.append(sqlValues[i][1])
# print(f'Number of original country code list is {len(only_country_code)}.')

# # Removing items that exceed MySQL limitation for integers
# for i in list(set(excluding_countries)):
#     only_country_code.remove(i)
# for i in range(len(set(excluding_countries_index))):
#     j = 0
#     only_year_values.pop(sorted(list(set(excluding_countries_index)))[i]-j)
#     j = j+1
# only_year_values.pop(only_country_code.index('AND'))
# only_country_code.remove('AND')
# print(f'Number of corrected country code list is {len(only_country_code)}.')
# print(f'Number of corrected year list is {len(only_year_values)}.')

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
        # Alter the table by adding columns and determine the data types
        print("Source table data type determination and sql_table configuration...")
        str_len = []
        for col in colName_filtered:
            for i in range(len(sqlValues)):
                if (type(sqlValues[i][colName_filtered.index(col)]) is str):
                    str_len.append(len(sqlValues[i][colName_filtered.index(col)]))
                else:
                    str_len.append(0)
        df = pd.DataFrame(str_len)
        df = df.values.reshape(len(colName_filtered), len(sqlValues))
        for col in colName_filtered:
            for i in range(len(sqlValues)):
                if (sqlValues[i][colName_filtered.index(col)] is None):
                    data_type = f"VARCHAR(1)"
                if (sqlValues[i][colName_filtered.index(col)] is not None):
                    if (type(sqlValues[i][colName_filtered.index(col)]) is str):
                        data_type = f"VARCHAR({df.max(axis=1)[colName_filtered.index(col)]})"
                        break
                    else:
                        if (type(sqlValues[i][colName_filtered.index(col)]) is int):
                            data_type = 'DECIMAL' # There is a MySQL limitation with INT type
                        if (type(sqlValues[i][colName_filtered.index(col)]) is dict):
                            data_type = 'JSON'
                        if (type(sqlValues[i][colName_filtered.index(col)]) is float):
                            data_type = 'FLOAT'
                        if (isinstance(sqlValues[i][colName_filtered.index(col)], decimal.Decimal)):
                            data_type = 'FLOAT'
                        if (type(sqlValues[i][colName_filtered.index(col)]) is datetime.date):
                            data_type = 'DATE'
                        if (type(sqlValues[i][colName_filtered.index(col)]) is list):
                            data_type = 'JSON'
                        break
            cursor.execute(f"ALTER TABLE {sql_table} ADD COLUMN {col} {data_type}")
        data_type_configuration = time.time()
        print(f"It took {data_type_configuration - download_time} seconds "
              f"(i.e. ~ {math.floor((data_type_configuration - download_time) / 3600)} hours and "
              f"{round((((data_type_configuration - download_time) / 3600)-(math.floor((data_type_configuration - download_time) / 3600))) * 60)} minutes) to complete the operation..."
              )
        string_values = '%s,' * (len(df_sqlValues.columns)-1) + '%s' # Here %s means string values
        sql = f"INSERT INTO data_analysis.{sql_table} VALUES ({string_values})"
        print('Insert sql statement is configured...')
        # Loop through the data frame
        insert_values_time = time.time()
        print('Inserting records into the sql table...')
        number_of_records = 0
        for index, row in df_sqlValues.iterrows():
            cursor.execute(sql, tuple(row))
            number_of_records = number_of_records + 1
            # The connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
        print(f"{number_of_records} records are inserted...")
        print(f"It took {insert_values_time - data_type_configuration} seconds (i.e. ~ "
              f"{math.floor((insert_values_time - data_type_configuration) / 3600)} hours and "
              f"{round((((insert_values_time - data_type_configuration) / 3600)-(math.floor((insert_values_time - data_type_configuration) / 3600))) * 60)} "
              f"minutes) to complete the insert operation..."
              )#
except Error as e:
    print("Error - ", e)

end = time.time()
print(f"Script ended in {end - start} seconds (i.e. ~ "
      f"{math.floor((end - start) / 3600)} hours and {round((((end - start) / 3600) - (math.floor((end - start) / 3600))) * 60)} minutes)..."
      )
