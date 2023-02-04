import pickle
import pandas as pd
from jsd_prophet import _get_holidays
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima.arima import auto_arima



def train_sarimax(train, holidays_chosen, folder_name, exp_name, seasonality = 48):
  '''  
  p = 1
  d = 0 # D order. d = 0 because the series is stationary
  q = 3 
  P = 2
  D = 0
  Q = 2
  s = 48

  my_seasonal_order = (P, D, Q, s)
  order = (p, d, q)
  '''
  m = None
  exog_vars = None
  ##
  if (holidays_chosen):
    holidays = _get_holidays()
    train.loc[pd.to_datetime(train["LastUpdated"]).dt.date.astype(str).isin(holidays["ds"]), "holidays" ] = 1
    exog_vars = train["holidays"]
    print("exog_vars")
    print(exog_vars)

  
  print("before auto_arima")
  auto_arima_model = auto_arima(y=train["OccupancyRate"],
                                x=exog_vars, #only required if exog data is used
                                seasonal=True,
                                m=seasonality, #seasonality
                                information_criterion="aic",
                                trace=True)  
  print("after auto_arima")                                
  my_seasonal_order = auto_arima_model.seasonal_order
  order = auto_arima_model.order
  ##  
 
  
  m = SARIMAX(train["OccupancyRate"], order=order, seasonal_order=my_seasonal_order, exog=exog_vars) 
  
  print("before fit train_sarimax")
  results_fit = m.fit(full_output=True, maxiter=100) #maxiter=1) 
  print("before results_fit train_sarimax")
  #results_fit.save("../../results/" + folder_name + '/resultsfit_' + exp_name + '.pkl')

  #'''
  print("before text_file train_sarimax")  
  text_file = open("../../results/" + folder_name + '/metrics_full_' + exp_name + '.txt', "w")
  n = text_file.write(str(results_fit.summary()) + "\n" +  str(seasonality) + "-" + str(my_seasonal_order) + "-" + str(order))
  text_file.close()  
  #'''
  
#  with open("../../results/" + folder_name + '/model_' + exp_name + '.pkl', "wb") as f:
#    pickle.dump(m, f)  
  print("before return m, results_fit train_sarimax")    
  return m, results_fit


def predict_sarimax(m, results_fit, train, test, folder_name, exp_name):
  forecast = (results_fit
              .get_prediction(start=len(train.index), end=len(train.index) + len(test.index) - 1, dynamic=True )
              .summary_frame(alpha=0.20) #Confidence Level 80%
  )
  forecast.to_csv("../../results/" + folder_name + '/forecast_' + exp_name + '.csv')
  return forecast
  
