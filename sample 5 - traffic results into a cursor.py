# -*- coding: utf-8 -*-
"""
@author: puser
Fetch records into a cursor
"""

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Database connection parameters
db_params = {
    'dbname': 'your_database',
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the database
connection = psycopg2.connect(**db_params)

# Create a cursor
cursor = connection.cursor()

# Execute a SQL query
cursor.execute('SELECT * FROM network_traffic')

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Get column names from the cursor description
columns = [desc[0] for desc in cursor.description]

# Close the cursor and connection
cursor.close()
connection.close()

# Convert the fetched data to a DataFrame
network_traffic_df = pd.DataFrame(rows, columns=columns)

# Convert the timestamp column to datetime
network_traffic_df['timestamp'] = pd.to_datetime(network_traffic_df['timestamp'])

# Set the timestamp as the index
network_traffic_df.set_index('timestamp', inplace=True)

# Resample the data to hourly traffic volume
hourly_traffic = network_traffic_df['traffic_volume'].resample('H').sum()

# Plot the hourly traffic volume
plt.figure(figsize=(14, 7))
hourly_traffic.plot()
plt.title('Hourly Network Traffic Volume')
plt.xlabel('Time')
plt.ylabel('Traffic Volume')
plt.show()

# Resample the data to daily traffic volume
daily_traffic = network_traffic_df['traffic_volume'].resample('D').sum()

# Plot the daily traffic volume
plt.figure(figsize=(14, 7))
daily_traffic.plot()
plt.title('Daily Network Traffic Volume')
plt.xlabel('Date')
plt.ylabel('Traffic Volume')
plt.show()

