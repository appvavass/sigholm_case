import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

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
hist_df['time'] = pd.to_datetime(hist_df['time'])  ##convert to datetime

### export cleaned dataframe
hist_df.to_csv('cleaned_data.csv')

### exploring the data #########################################################
plt.figure()
plt.scatter(hist_df['load'],hist_df['temperature'],marker = '*')
plt.title('Raw data')
plt.xlabel('Load [MW]')
plt.ylabel('Temperature [°C]')
### removing the outlayers to improve dataset for better prediction ############

hist_df_filtered  = hist_df[hist_df['load']>2300]

plt.figure()
plt.scatter(hist_df_filtered['load'],hist_df_filtered['temperature'])
plt.title('Filtered data')
plt.xlabel('Load [MW]')
plt.ylabel('Temperature [°C]')

### preparing a linear regression model

dep_var = hist_df_filtered['load'].values.reshape(-1,1)
indep_var = hist_df_filtered['temperature'].values.reshape(-1,1)

linear_regressor = LinearRegression()
linear_regressor.fit(indep_var,dep_var)

### calculating coefficients for the predicting function to be used
print(linear_regressor.coef_, linear_regressor.intercept_)


### plotting model vs observation to assess quality
load_predict = linear_regressor.predict(indep_var)

plt.figure()
plt.scatter(indep_var,dep_var)
plt.plot(indep_var, load_predict, color = 'red')
plt.title('Linear regression model')
plt.xlabel('Temperature [°C]')
plt.ylabel('Load [MW]')
plt.show()

