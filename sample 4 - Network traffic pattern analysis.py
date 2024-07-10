# -*- coding: utf-8 -*-
"""

NETWORK TRAFFIC PATTERN ANALYSIS 
@author: puser
"""

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Database connection string
DATABASE_URI = 'postgresql://username:password@localhost:5432/your_database'

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Connect to the database
connection = engine.connect()

# Retrieve data from the SQL table
query = 'SELECT * FROM network_traffic'
network_traffic_df = pd.read_sql(query, connection)

# Close the database connection
connection.close()

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

