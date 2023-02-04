from neuralprophet import NeuralProphet
from neuralprophet.utils import save
import pickle
from jsd_prophet import _get_holidays

def train_neural_prophet(train, holidays_chosen, folder_name, exp_name, city_chosen, interval = 30):
  train = train.rename({'LastUpdated': 'ds', 'OccupancyRate': 'y'}, axis='columns')

  quantile_lo, quantile_hi = 0.20, 0.80
  quantiles = [quantile_lo, quantile_hi]

  m = None
  if (holidays_chosen):
    if (city_chosen.casefold() == "malaga".casefold()):
      holidays = _get_holidays() #TODO - We are not adding this ...
      m = NeuralProphet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False, quantiles = quantiles)
      m = m.add_country_holidays("ES", mode="additive", lower_window=0, upper_window=0) 
    elif (city_chosen.casefold() == "birmingham".casefold()):
      m = NeuralProphet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False, quantiles = quantiles)
      m = m.add_country_holidays("UK", mode="additive", lower_window=0, upper_window=0)         
    else:
      print("city_chosen = " + city_chosen)
      print("ERROR: jsd_neural_prophet line 22 No city chosen")
      exit()  
  else:
    m = NeuralProphet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False, quantiles = quantiles)
    
  m.add_seasonality(name='ddd', period=1, fourier_order=10) 
  print(train)
  metrics_str = m.fit(train, freq=str(interval)+'min', epochs=5000) #1000
  print(metrics_str)
  text_file = open("../../results/" + folder_name + '/metrics_full_' + exp_name + '.txt', "w")
  n = text_file.write(str(metrics_str))
  text_file.close()
    
  #save(m, "../../results/" + folder_name + '/model_' + exp_name + '.json')  # Save model
  #with open("../../results/" + folder_name + '/model_' + exp_name + '.pkl', "wb") as f:
  #  pickle.dump(m, f)    
  train = train.rename({'ds': 'LastUpdated', 'y': 'OccupancyRate'}, axis='columns')  
  return m
  
  
                        
def predict_neural_prophet(m, train, test, interval, folder_name, exp_name, city_chosen):
  train = train.rename({'LastUpdated': 'ds', 'OccupancyRate': 'y'}, axis='columns')
  future = m.make_future_dataframe(train, periods=len(test.index))#len(test.index))
  
  #BIRMINGHAM Select from 8:00 to 16:30
  #if (city_chosen.casefold() == "birmingham".casefold()):
  #  periods = test.shape[0] + int((test.shape[0]/48) * 30)
  #  future = m.make_future_dataframe(periods=test.shape[0], freq=str(interval)+'min')
  #  future = future.loc[ (future["ds"].dt.time > time(7,30)) & (future["ds"].dt.time < time(17,0)) ] 
  #  future = future.reset_index()  
  
  
  forecast = m.predict(future)
  forecast.to_csv("../../results/" + folder_name + '/forecast_' + exp_name + '.csv')

  m.plot_components(forecast).savefig("../../results/" + folder_name + '/components_' + exp_name + '.png')
  m.plot(forecast).savefig("../../results/" + folder_name + '/forecast_' + exp_name + '.png')
  m.plot_parameters().savefig("../../results/" + folder_name + '/parameters_' + exp_name + '.png')

  train = train.rename({'ds': 'LastUpdated', 'y': 'OccupancyRate'}, axis='columns')  
  return forecast  
