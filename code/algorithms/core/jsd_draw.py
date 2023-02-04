import matplotlib.pyplot as plt
import plotly.graph_objects as go



def plot_prediction_html(dataset_train, dataset_test, prediction, folder_name, exp_name):
  trace1 = go.Scatter(
      x = list(range(len(dataset_train))),
      y = dataset_train,
      mode = 'lines',
      name = 'Train'
  )
  trace2 = go.Scatter(
      x = list(range(len(dataset_train), len(dataset_train) + len(dataset_test))),
      y = prediction,
      mode = 'lines',
      name = 'Prediction'
  )
  trace3 = go.Scatter(
      x = list(range(len(dataset_train), len(dataset_train) + len(dataset_test))),
      y = dataset_test,
      mode='lines',
      name = 'Test'
  )
  layout = go.Layout(
      title = "Prediction",
      xaxis = {'title' : "Date"},
      yaxis = {'title' : "Values"}
  )
  fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
  #fig.show()
  fig.write_html("../../results/" + folder_name + '/forecast_' + exp_name + '.html')


def plot_prediction_prophet(train, test, forecast, forecast_upper, forecast_lower, folder_name, exp_name):
  '''
  yhat = results_AR["yhat"].to_numpy() - 0.5
  yhat_upper = results_AR["yhat_upper"].to_numpy() - 0.5
  yhat_lower = results_AR["yhat_lower"].to_numpy() - 0.5
  newyhat = np.where(abs(yhat_upper) > abs(yhat_lower), yhat_upper, yhat_lower)
  newyhat = newyhat + 0.5
  results_AR["newyhat"] = newyhat
  '''


  fig, ax = plt.subplots(figsize=(20,10))
  ax = train.plot(label='Training Actual Occupancy Rate')
  ax.set(
      title='True and Predicted Values, with Confidence Intervals',
      xlabel='Date',
      ylabel='Actual / Predicted Values'
  )
  forecast.plot(ax=ax, style='gray', label='Predicted Mean')
  if (forecast_upper is not None and forecast_lower is not None):
    ax.fill_between(
        forecast.index, forecast_lower, forecast_upper,
        color='gray', alpha=0.2
    )

  test.plot(label='Testing Actual Occupancy Rate')
  legend = ax.legend(loc='upper left')
  '''
  ax.set_xlim([datetime.date(2020, 12, 31), datetime.date(2021, 1, 8)])
  plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30)) 
  plt.gca().xaxis.set_tick_params(rotation = 30)
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d')) 
  '''
  plt.savefig("../../results/" + folder_name + '/forecast_test_' + exp_name + '.png')
  plt.cla()
  plt.clf()


  '''  
  plt.figure(figsize=(16,6))
  plt.title('FBPROPHET Model')
  plt.plot(train, label='Training Actual Occupancy Rate')
  plt.xlabel('Date')
  plt.ylabel('Percent Occupied')
  forecast = forecast[len(train):]
  plt.plot(test, label='Testing Actual Occupancy Rate')
  plt.plot(forecast, color='gray', label='FBPROPHET Predicted Occupancy Rate Full')
  '''

  '''
  plt.plot(results_AR["yhat_upper"], color='purple', label='Upper FBPROPHET Predicted Occupancy Rate Full')
  plt.plot(results_AR["yhat_lower"], color='green', label='Lower FBPROPHET Predicted Occupancy Rate Full')
  '''
  '''    
  #plt.plot(results_AR["newyhat"], color='gray', label='FBPROPHET Predicted Occupancy Rate Full')
  plt.legend()

  plt.savefig("../../results/" + folder_name + '/forecast_test_' + exp_name + '.png')
  plt.cla()
  plt.clf()
  '''  
