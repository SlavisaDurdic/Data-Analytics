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

# Enter a name of the MySQL table
sql_table = 'publicbigquery_imdb_title_basics_full'

# Write an sql query to pool values from BigQuery
db_query = """
        SELECT * FROM `bigquery-public-data.imdb.title_basics`;
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

print('Establishing the connection with MySQL server...')
try:
    conn = mysql.connect(host='localhost', database='data_analysis', user='root', password='')
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
                    # print(f"NULL value for object sqlValues[{i}][{colName_filtered.index(col)}].")
                    data_type = f"VARCHAR(1)"
                    # continue
                if (sqlValues[i][colName_filtered.index(col)] is not None):
                    if (type(sqlValues[i][colName_filtered.index(col)]) is str):
                        data_type = f"VARCHAR({df.max(axis=1)[colName_filtered.index(col)]})"
                        break
                    else:
                        if (type(sqlValues[i][colName_filtered.index(col)]) is int):
                            data_type = 'INT'
                        if (type(sqlValues[i][colName_filtered.index(col)]) is dict):
                            data_type = 'JSON'
                        if (type(sqlValues[i][colName_filtered.index(col)]) is float):
                            data_type = 'FLOAT'
                        if (isinstance(sqlValues[i][colName_filtered.index(col)], decimal.Decimal)):
                            data_type = 'FLOAT'
                        if (type(sqlValues[i][colName_filtered.index(col)]) is datetime.date):
                            data_type = 'DATE'
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
              )
except Error as e:
    print("Error - ", e)

end = time.time()
print(f"Script ended in {end - start} seconds (i.e. ~ "
      f"{math.floor((end - start) / 3600)} hours and {round((((end - start) / 3600) - (math.floor((end - start) / 3600))) * 60)} minutes)..."
      )
