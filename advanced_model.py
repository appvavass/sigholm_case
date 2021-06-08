import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

### read data from csv
df = pd.read_csv('cleaned_data.csv')
df['time'] = pd.to_datetime(df['time'])
df= df.set_index('time')
df['hour']  = df.index.hour

##create a dataframe where the average load for each hour  through the day is considered
hourly_avg_load = df.groupby(by=[df.index.hour]).mean()

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(hourly_avg_load.index, hourly_avg_load['load'], 'g-')
ax2.plot(hourly_avg_load.index, hourly_avg_load['temperature'], 'r--')
ax1.set_xlabel('Hour of the day')
ax1.set_ylabel('Load', color='g')
ax2.set_ylabel('Temperature', color='r')
#plt.show()
### the load is higher in late afternoon even if the temperature is the same

### filter out bad data
df_filtered  = df[df['load']>2300]

dep_var = df_filtered['load'].values.reshape(-1,1)
indep_var = df_filtered[['temperature','hour']].values.reshape(-1,2)

linear_regressor = LinearRegression()
linear_regressor.fit(indep_var,dep_var)

print('Regression coefficients:',linear_regressor.coef_, '\nintercept:',linear_regressor.intercept_)


