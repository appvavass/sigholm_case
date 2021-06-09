from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Type
from datetime import datetime
from typing import Dict
import json

temperature =  Type[float]
heat_load = Type[float]

#this function filters out the negative load
def filter(x):
    if x <= 0:
        return 0
    else:
        return x

def forecast_heat_load(input_dict: Dict[datetime, temperature]) -> Dict[datetime, heat_load]:
   
    
    # Do your forecast here

    forecast = pd.DataFrame.from_dict(data = input_dict, orient= 'index', columns=['forecast_temp'])
    forecast.index = pd.to_datetime(forecast.index) 

    ### use coefficients calculated from the previous data analysis    
    reg_coefficient = -517.0339
    reg_intercept = 13246.21239
    forecast['forecast_load'] = forecast['forecast_temp'].apply(lambda x: reg_coefficient*x + reg_intercept)
    
    forecast['forecast_load'] = forecast['forecast_load'].apply(filter)
    output_dict = forecast['forecast_load'].to_dict()
    
    return output_dict


### this function is using both hour of the day ant temperature

def forecast_heat_load_advanced(input_dict: Dict[datetime, temperature]) -> Dict[datetime, heat_load]:
   
    forecast = pd.DataFrame.from_dict(data = input_dict, orient= 'index', columns=['forecast_temp'])
    forecast.index = pd.to_datetime(forecast.index) 
    forecast['forecast_hour']  = forecast.index.hour
    
    ### use coefficient calculated from the previous data analysis 
    reg_coefficient_hour = 50.87867
    reg_coefficient_temperature = -526.198558
    reg_intercept = 12720.53972
    
    forecast['x1']  = forecast['forecast_hour'].apply(lambda x: x*reg_coefficient_hour + reg_intercept)
    forecast['x2'] = forecast['forecast_temp'].apply(lambda x: x*reg_coefficient_temperature)
    forecast['forecast_load']  = forecast['x1']+forecast['x2']
    forecast['forecast_load'] = forecast['forecast_load'].apply(filter)

    output_dict = forecast['forecast_load'].to_dict()

    return output_dict

raw_data  = open('temperature_forecast.json')
temp_forecast = json.load(raw_data)

### answer
simple = forecast_heat_load(temp_forecast) 
advanced = forecast_heat_load_advanced(temp_forecast) 


### some plotting

df1 = pd.DataFrame.from_dict(data = simple, orient = 'index', columns=['temp'])
df2 = pd.DataFrame.from_dict(data = advanced, orient = 'index', columns=['temp'])

fig, ax1 = plt.subplots()
ax1.plot_date(df1.index,df1['temp'], 'g-')
ax1.plot_date(df2.index,df2['temp'], 'r--')
plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 45)
ax1.set_xlabel('Date')
ax1.set_ylabel('Load [MW]')
plt.legend(['Simple model','Advanced model'])
plt.show()
