from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Type
from datetime import datetime
from typing import Dict

temperature =  Type[float]
heat_load = Type[float]


example_input = {'2021-05-23T20:00:00+00:00':25.6,'2021-05-23T21:00:00+00:00':10.4,'2021-05-23T22:00:00+00:00':-10.2}

def forecast_heat_load(input_dict: Dict[datetime, temperature]) -> Dict[datetime, heat_load]:
   
    
    # Do your forecast here

    forecast = pd.DataFrame.from_dict(data = input_dict, orient= 'index', columns=['forecast_temp'])

    ### use coefficient calculated from the previous data analysis    
    
    reg_coefficient = -517.0339
    reg_intercept = 13246.21239
    forecast['forecast_load'] = forecast['forecast_temp'].apply(lambda x: reg_coefficient*x + reg_intercept)

    output_dict = forecast['forecast_load'].to_dict

    ### uncomment to plot estimated load
    
    #plt.plot(forecast.index, forecast['forecast_load'], color='red')
    #plt.show()
    

    return output_dict
