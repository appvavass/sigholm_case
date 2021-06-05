import matplotlib
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

### small example input dictionary
example_input = {'2021-05-23T20:00:00+00:00':25.6,'2021-05-23T21:00:00+00:00':10.4,'2021-05-23T22:00:00+00:00':-10.2}


conn = sqlite3.connect('city_archive.db')

### read data from database and create a dataframe with date-temperature-load entries

SQL_query_temp = 'SELECT time, value FROM temperature'
SQL_query_load = 'SELECT time, value FROM heat_load'

df_temp  = pd.read_sql(SQL_query_temp, conn)
df_temp.columns = ['time','temperature']

df_load = pd.read_sql(SQL_query_load, conn)
df_load.columns = ['time','load']

df_load.drop_duplicates(inplace=True)
df_temp.drop_duplicates(inplace=True)

hist_df = df_load.merge(df_temp, left_on= 'time', right_on = 'time')
hist_df['time'] = pd.to_datetime(hist_df['time'])  ##convert to date_time

### exploring the data #########################################################

plt.scatter(hist_df['load'],hist_df['temperature'],marker = '*')
plt.show()

### removing the outlayers to improve dataset for better prediction ############

hist_df_filtered  = hist_df[hist_df['load']>2300]
plt.scatter(hist_df_filtered['load'],hist_df_filtered['temperature'])
plt.show()

### preparing a linear regression model

dep_var = hist_df_filtered['load'].values.reshape(-1,1)
indep_var = hist_df_filtered['temperature'].values.reshape(-1,1)

linear_regressor = LinearRegression()
linear_regressor.fit(indep_var,dep_var)

load_predict = linear_regressor.predict(indep_var)

plt.scatter(indep_var,dep_var)
plt.plot(indep_var, load_predict, color = 'red')
plt.show()

forecast = pd.DataFrame.from_dict(data = example_input, orient= 'index', columns=['forecast_temp'])

temp_forecast  = forecast['forecast_temp'].values.reshape(-1,1)
forecast['forecast_load'] = linear_regressor.predict(temp_forecast)

plt.plot(forecast.index, forecast['forecast_load'], color = 'red')
plt.show()

output_dict = forecast['forecast_load'].to_dict
