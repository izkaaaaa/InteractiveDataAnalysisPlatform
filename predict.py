import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime
import statsmodels.api as sm


def prediction_function(df,d=1,p=5,q=0):
    #前十票房
    Top_10_Gross_list=df['Top_10_Gross'].tolist()
    arima=sm.tsa.SARIMAX(Top_10_Gross_list, order=(p,d,q)) #p=5,d=1,q=0
    Top_10_Gross_model_results=arima.fit()

    forecast_Top_10_Gross = Top_10_Gross_model_results.get_forecast(steps=10) #预测未来10个时间点
    Top_10_Gross_predictions = forecast_Top_10_Gross.predicted_mean.tolist()

    #总票房
    Overall_Gross_list = df['Overall_Gross'].tolist()
    arima = sm.tsa.SARIMAX(Overall_Gross_list, order=(p, d, q))  # p=5,d=1,q=0
    Overall_Gross_model_results = arima.fit()

    forecast_Overall_Gross = Overall_Gross_model_results.get_forecast(steps=10)  # 预测未来10个时间点
    Overall_Gross_predictions = forecast_Overall_Gross.predicted_mean.tolist()

    #发行数量
    Releases_list = df['Releases'].tolist()
    arima = sm.tsa.SARIMAX(Releases_list, order=(p, d, q))  # p=5,d=1,q=0
    Releases_model_result = arima.fit()

    forecast_Releases = Releases_model_result.get_forecast(steps=10)  # 预测未来10个时间点
    Releases_predictions = forecast_Releases.predicted_mean.tolist()

    return {
        'Top_10_Gross': Top_10_Gross_predictions,
        'Overall_Gross': Overall_Gross_predictions,
        'Releases': Releases_predictions
    }


