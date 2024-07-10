# -*- coding: utf-8 -*-
"""

@author: puser
Forecasting no of telco subscribers over the period. 
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
import statsmodels.api as sm
from fbprophet import Prophet

class TelcoForecast:
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path)
        self.model = None

    def preprocess_data(self):
        # Assuming the data has a DateTime column and a 'Subscribers' column
        self.data['DateTime'] = pd.to_datetime(self.data['DateTime'])
        self.data = self.data.set_index('DateTime')
        
        # Plotting the data
        plt.figure(figsize=(10, 6))
        plt.plot(self.data.index, self.data['Subscribers'], label='Subscribers')
        plt.xlabel('Date')
        plt.ylabel('Number of Subscribers')
        plt.title('Telco Subscribers Over Time')
        plt.legend()
        plt.show()

    def train_test_split(self, test_size=0.2):
        # Splitting the data into train and test sets
        split_index = int(len(self.data) * (1 - test_size))
        self.train_data = self.data.iloc[:split_index]
        self.test_data = self.data.iloc[split_index:]
    
    def train_model(self):
        # Using Prophet for time series forecasting
        self.train_data.reset_index(inplace=True)
        self.train_data.rename(columns={'DateTime': 'ds', 'Subscribers': 'y'}, inplace=True)
        
        self.model = Prophet()
        self.model.fit(self.train_data)

    def make_forecast(self, periods):
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        
        # Plotting the forecast
        self.model.plot(forecast)
        plt.title('Forecasted Telco Subscribers')
        plt.xlabel('Date')
        plt.ylabel('Number of Subscribers')
        plt.show()
        
        return forecast

    def evaluate_model(self):
        # Evaluating the model using Mean Squared Error on test data
        self.test_data.reset_index(inplace=True)
        self.test_data.rename(columns={'DateTime': 'ds', 'Subscribers': 'y'}, inplace=True)
        
        forecast = self.make_forecast(periods=len(self.test_data))
        forecast_test = forecast.tail(len(self.test_data))
        
        mse = mean_squared_error(self.test_data['y'], forecast_test['yhat'])
        print(f'Mean Squared Error: {mse}')

# Create an instance of the TelcoForecast class
forecast_model = TelcoForecast('telco_subscribers.xlsx')

# Preprocess the data
forecast_model.preprocess_data()

# Split the data into training and testing sets
forecast_model.train_test_split()

# Train the model
forecast_model.train_model()

# Make a forecast
forecast = forecast_model.make_forecast(periods=12)

# Evaluate the model
forecast_model.evaluate_model()


