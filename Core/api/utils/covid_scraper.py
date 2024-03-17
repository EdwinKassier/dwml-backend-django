import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import ast
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from sklearn.ensemble import AdaBoostRegressor
from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error


class CovidScraper:

  def __init__(self, country, date, apiCall):
    self.country = country
    self.target_date = date
    self.api_call = apiCall
    self.clean_data = None
    self.model = None
    self.predicted_data = None

  
  def driver_logic(self):

    self.get_raw_data()
    self.train_model()
    self.predict()
    if not self.api_call:
      self.chart()
    else:
      return self.predicted_data.to_json(orient="records")

  # Extract
  def get_raw_data(self):

    url = f'https://www.worldometers.info/coronavirus/country/{self.country}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if "Highcharts.chart('graph-cases-daily'" in str(script):
            jsonStr = str(script)
            
            dates = re.search(r'(xAxis: {[\s\S\W\w]*)(categories: )(\[[\w\W\s\W]*\"\])', jsonStr)
            dates = dates.group(3).replace('[','').replace(']','')
            dates = ast.literal_eval(dates)
            dates = [ x for x in dates]
            
            data = re.search(r"(name: '7-day moving average')[\s\S\W\w]*(data:[\s\S\W\w]*\d\])", jsonStr, re.IGNORECASE)
            data = data.group(2).split('data:')[-1].strip().replace('[','').replace(']','').split(',')


    df = pd.DataFrame({'Date':dates, '7DA':data})

    # Cleaning Step - Transform

    # Allow us to differentiate the values in training set
    df['Predicted'] = False

    # Converting all daily case numbers to numbers
    df['7DA'] = pd.to_numeric(df['7DA'], errors='coerce')
    df = df.dropna(subset=['7DA'])
    df['7DA'] = df['7DA'].astype(int)

    # Convert all dates to date time
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Filter out non zero values
    df = df[df["7DA"] > 0]

    # Remove all dates after target date
    df = df[df['Date'] <= self.target_date]

    self.clean_data = df

  # Learn
  def train_model(self):

    df = self.clean_data

    try:
      
      # Convert date to float for processing
      df['Date'] = df['Date'].astype('int64').astype(float)

      # We are using the full available data set to give maximum
      y = df['7DA'].values.reshape(-1, 1)
      X = df['Date'].values.reshape(-1, 1)

      ada_boost = AdaBoostRegressor()
      ada_boost.fit(X, y)

      self.model = ada_boost

    except Exception as e:
      print(e)

  # Predict
  def predict(self):

    df = self.clean_data

    # Number of future dates to generate
    x = 7

    start_date = datetime.strptime(self.target_date, '%Y-%m-%d')  # Use the last date in your existing DataFrame
    future_dates = [start_date + timedelta(days=i) for i in range(1, x+1)]

    # Create a DataFrame with future dates and 7DA set to null
    future_data = {
        'Date': future_dates,
        '7DA': [None] * x
    }
    future_df = pd.DataFrame(future_data)

    future_df['Date'] = future_df['Date'].astype('int64').astype(float)

    X_pred = future_df['Date'].values.reshape(-1, 1)

    y_pred = self.model.predict(X_pred)

    df_preds = pd.DataFrame({'Date':future_dates,'7DA': [round(x) for x in y_pred.squeeze()],'Predicted':True})

    df_preds['Date'] = pd.to_numeric(df_preds['Date'], errors='coerce')

    frames = [df, df_preds]

    result = pd.concat(frames)

    # Clean up and consistency for charting

    result['Date'] = pd.to_numeric(result['Date'], errors='coerce')

    result['Date'] = pd.to_datetime(result['Date'], errors='coerce')

    result.reset_index(drop=True, inplace=True)

    self.predicted_data = result

  def chart(self):

    target_data = self.predicted_data

    plt.figure(figsize=(12, 6))  # Increase figure size
    sns.lineplot(x = "Date", y = "7DA", hue="Predicted", data=target_data.tail(50), dashes=False) # We are tailing the data to better show the predictive result
    plt.xticks(rotation=45)  # Rotate x-axis labels
    plt.tight_layout()  # Adjust layout

    plt.show()
