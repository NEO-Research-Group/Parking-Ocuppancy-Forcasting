from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import pandas as pd
from datetime import datetime, timedelta, time

def _get_holidays():
  local_holidays = pd.DataFrame({
    'holiday': 'local_holidays',
    'ds': pd.to_datetime(['2022-08-19', '2022-09-08']),
    'lower_window': 0,
    'upper_window': 0,
  })


  national_and_regional_holidays = pd.DataFrame({
    'holiday': 'national_and_regional_holidays',
    'ds': pd.to_datetime(['2022-01-01', '2022-01-06', '2022-02-28',
                          '2022-04-14', '2022-04-25', '2022-05-02',
                          '2022-08-15', '2022-10-12', '2022-11-01',
                          '2022-12-06', '2022-12-08', '2022-12-26']),
    'lower_window': 0,
    'upper_window': 0,
  })

  sundays = pd.DataFrame({
    'holiday': 'sundays',
    'ds': pd.to_datetime(['2022-01-02', '2022-01-09', '2022-01-16', 
                          '2022-01-23', '2022-01-30', '2022-02-06', 
                          '2022-02-13', '2022-02-20', '2022-02-27', 
                          '2022-03-06', '2022-03-13', '2022-03-20',
                          '2022-03-27', '2022-04-03', '2022-04-10',
                          '2022-04-17', '2022-04-24', '2022-05-01',
                          '2022-05-08', '2022-05-15', '2022-05-22',
                          '2022-05-29', '2022-06-05', '2022-06-12',
                          '2022-06-19', '2022-06-26', '2022-07-03',
                          '2022-07-10', '2022-07-17', '2022-07-24',
                          '2022-07-31', '2022-08-07', '2022-08-14',
                          '2022-08-21', '2022-08-28', '2022-09-04',
                          '2022-09-11', '2022-09-18', '2022-09-25',
                          '2022-10-02', '2022-10-09', '2022-10-16',
                          '2022-10-23', '2022-10-30', '2022-11-06',
                          '2022-11-13', '2022-11-20', '2022-11-27',
                          '2022-12-04', '2022-12-11', '2022-12-18',
                          '2022-12-25',]),
    'lower_window': 0,
    'upper_window': 0,
  })
  return pd.concat((local_holidays, national_and_regional_holidays, sundays))


def train_prophet(train, holidays_chosen, folder_name, exp_name, city_chosen):
  train = train.rename({'LastUpdated': 'ds', 'OccupancyRate': 'y'}, axis='columns')

  m = None
  #'''
  if (holidays_chosen):
    if (city_chosen.casefold() == "malaga".casefold()):
      holidays = _get_holidays()
      m = Prophet(interval_width=0.80, holidays=holidays, daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False) #Prophet(daily_seasonality = True)
      m.add_country_holidays(country_name='ES')
    elif (city_chosen.casefold() == "birmingham".casefold()):
      m = Prophet(interval_width=0.80, daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False) #Prophet(daily_seasonality = True)
      m.add_country_holidays(country_name='UK')            
    else:
      print("city_chosen = " + city_chosen)    
      print("ERROR: jsd_prophet line 65 No city chosen")
      exit()
  else:
    m = Prophet(interval_width=0.80, daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False) 
   
  m.add_seasonality(name='ddd', period=1, fourier_order=10)   #period is number of days
  #m.add_seasonality(name='ddd', period=seasonality, fourier_order=10) #period=1
  #'''
  #m = Prophet() 
  m.fit(train)
  
  with open("../../results/" + folder_name + '/model_' + exp_name + '.json', 'w') as fout:
    from prophet.serialize import model_to_json, model_from_json
    fout.write(model_to_json(m))  # Save model
    
  train = train.rename({'ds': 'LastUpdated', 'y': 'OccupancyRate'}, axis='columns')  
  return m


def predict_prophet(m, train, test, interval, folder_name, exp_name, city_chosen):
  future = m.make_future_dataframe(periods=test.shape[0], freq=str(interval)+'min')


  #BIRMINGHAM Select from 8:00 to 16:30
  if (city_chosen.casefold() == "birmingham".casefold()):
    periods = test.shape[0] + int((test.shape[0]/48) * 30)
    future = m.make_future_dataframe(periods=test.shape[0], freq=str(interval)+'min')
    future = future.loc[ (future["ds"].dt.time > time(7,30)) & (future["ds"].dt.time < time(17,0)) ] 
    future = future.reset_index()

  future = pd.concat([train.copy(), test.copy()])
  future.columns = future.columns.str.replace('LastUpdated', 'ds')
  future = future.drop('OccupancyRate', axis=1)

  forecast = m.predict(future)
  forecast.to_csv("../../results/" + folder_name + '/forecast_' + exp_name + '.csv')

  m.plot_components(forecast).savefig("../../results/" + folder_name + '/components_' + exp_name + '.png')
  m.plot(forecast).savefig("../../results/" + folder_name + '/forecast_' + exp_name + '.png')
  #m.plot_parameters().savefig("../../results/" + exp_name + '/parameters_' + exp_name + '.png')
  
  plot_components_plotly(m, forecast).write_html("../../results/" + folder_name + '/components_plotly_' + exp_name + '.html') 
  return forecast
  
