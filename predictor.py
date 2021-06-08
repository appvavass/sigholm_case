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

def forecast_heat_load(input_dict: Dict[datetime, temperature]) -> Dict[datetime, heat_load]:
   
    
    # Do your forecast here

    forecast = pd.DataFrame.from_dict(data = input_dict, orient= 'index', columns=['forecast_temp'])
    forecast.index = pd.to_datetime(forecast.index) ## convert to datetime 

    ### use coefficient calculated from the previous data analysis    
    
    reg_coefficient = -517.0339
    reg_intercept = 13246.21239
    forecast['forecast_load'] = forecast['forecast_temp'].apply(lambda x: reg_coefficient*x + reg_intercept)

    output_dict = forecast['forecast_load'].to_dict

    ### uncomment  this section to plot estimated load:
    
    plt.plot_date(forecast.index, forecast['forecast_load'],'r-')
    plt.xlabel('Date')
    plt.ylabel('Load [MW]')
    plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 45)
    plt.show()
    ######### end of section

    return output_dict

### execute the forecast 

raw_data  = open('temperature_forecast.json')
temp_forecast = json.load(raw_data)

forecast_heat_load(temp_forecast)