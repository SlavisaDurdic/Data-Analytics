# MAKE SURE TO PROVIDE CORRECT INFO FOR symbol, start_date, end_date, and sql_table
# ---> LINES 33-35, 44 AND 48

import yfinance as yf
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from configparser import ConfigParser

# Function to download data from Yahoo Finance
def download_yahoo_finance_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Function to load data into MySQL table
def load_data_into_mysql(data, table_name, database_config):
    engine = create_engine(f"mysql+mysqlconnector://{database_config['user']}:{database_config['password']}@{database_config['host']}:{database_config['port']}/{database_config['database']}")
    data.to_sql(name=table_name, con=engine, if_exists='replace', index=True)

# Read database configuration from the config file
def read_database_config(filename='config.ini', section='database'):
    parser = ConfigParser()
    parser.read(filename)

    # Return a dictionary of the database parameters
    return {k: v for k, v in parser.items(section)}

# Function to save data to a CSV file
def save_data_to_csv(data, file_path):
    data.to_csv(file_path, index=True)

# Stock symbol and date range
symbol = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'

# Download data from Yahoo Finance
stock_data = download_yahoo_finance_data(symbol, start_date, end_date)

# Read database configuration from the config file
database_config = read_database_config()

# Load data into MySQL table
table_name = 'appl_stock_data'
load_data_into_mysql(stock_data, table_name, database_config)

# Save data to CSV file
csv_file_path = 'apple_stock_data.csv'
save_data_to_csv(stock_data, csv_file_path)