import pandas as pd
from prophet import Prophet
import argparse
import os
import matplotlib.pyplot as plt

from jsd_draw import plot_prediction_prophet, plot_prediction_html
from jsd_prophet import train_prophet, predict_prophet
from jsd_metrics import report_metrics
from jsd_data import load_dataset
from jsd_neural_prophet import train_neural_prophet, predict_neural_prophet
from jsd_sarimax import train_sarimax, predict_sarimax
#from jsd_lstm import train_lstm, predict_lstm
from jsd_rnn import train_rnn, predict_rnn


if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("-i", "--interval", required=True, help="Interval chosen.", type=int)
  ap.add_argument("-a", "--algorithm", required=True, help="Algorithm chosen. Type String.")
  ap.add_argument("-c", "--city", required=True, help="City chosen. Type String.")  
  ap.add_argument("-p", "--parking", required=True, help="Parking chosen. Type String.")
  ap.add_argument("-d", "--day_of_the_week", required=True, help="Parking chosen (0-6 days of week. 7 for full week).", type=int)            
  ap.add_argument("-ho", "--holidays", required=True, help="Add holidays or not.", type=int)
  #ap.add_argument("-v", "--cross_validation", required=True, help="Id of cross validation set used (from 0 to 4).", type=int)  
  ap.add_argument("-v", "--cross_validation", required=True, help="Id of cross validation set used (oneweek, twoweeks, threeweeks, month).")  
  ap.add_argument("-w", "--window_size", required=True, help="Window Size chosen.", type=int) 

  args = ap.parse_args()
  argparse_dict = vars(args)
  print(argparse_dict)

  interval_chosen = int(args.interval)
  algorithm_chosen = args.algorithm
  parking_chosen = args.parking
  day_of_week_chosen = int(args.day_of_the_week)  
  holidays_chosen = int(args.holidays)    
  cross_validation_chosen = args.cross_validation   #cross_validation_chosen = int(args.cross_validation)   
  city_chosen = args.city
  window_size_chosen = int(args.window_size)

  
  
  train, test = load_dataset(city_chosen, parking_chosen, day_of_week_chosen, cross_validation_chosen)
  
  folder_name = city_chosen + "/" + algorithm_chosen + "/" + parking_chosen + "/cross_val_" + str(cross_validation_chosen) + "/holidays_" + str(holidays_chosen) + "/dayofweek_" + str(day_of_week_chosen)
  exp_name = city_chosen + "_" + algorithm_chosen + "_" + parking_chosen + "_cross_val_" + str(cross_validation_chosen) + "_holidays_" + str(holidays_chosen) + "_dayofweek_" + str(day_of_week_chosen)
  if not os.path.exists("../../results/" + folder_name):
    os.makedirs("../../results/" + folder_name )  
  if (algorithm_chosen == "prophet"):

    m = train_prophet(train, holidays_chosen, folder_name, exp_name, city_chosen)
    forecast = predict_prophet(m, train, test, interval_chosen, folder_name, exp_name, city_chosen)
    plot_prediction_prophet(train["OccupancyRate"], test["OccupancyRate"], forecast["yhat"], forecast["yhat_upper"], forecast["yhat_lower"], folder_name, exp_name)
    plot_prediction_html(train["OccupancyRate"], test["OccupancyRate"], forecast.iloc[len(train.index):,]["yhat"], folder_name, exp_name)
    metrics_str = report_metrics(test["OccupancyRate"].squeeze(), forecast.iloc[len(train.index):,]["yhat"].squeeze(), folder_name, exp_name)
    print(metrics_str)
  elif (algorithm_chosen == "neural_prophet"):
    m = train_neural_prophet(train, holidays_chosen, folder_name, exp_name, city_chosen, interval_chosen)
    forecast = predict_neural_prophet(m, train, test, interval_chosen, folder_name, exp_name, city_chosen)
    print(forecast)
    forecast.index = forecast.index + len(train.index)
    plot_prediction_prophet(train["OccupancyRate"], test["OccupancyRate"], forecast["yhat1"], forecast["yhat1 80.0%"], forecast["yhat1 20.0%"], folder_name, exp_name)
    #plot_prediction_html(train["OccupancyRate"], test["OccupancyRate"], forecast["yhat1"], folder_name, exp_name)
    print("printing metrics")
    metrics_str = report_metrics(test["OccupancyRate"].squeeze(), forecast["yhat1"].squeeze(), folder_name, exp_name)
    print(metrics_str)
  elif (algorithm_chosen == "sarimax"):
    print("before fit")
    m, results_fit = train_sarimax(train, holidays_chosen, folder_name, exp_name)
    print("after fit")    
    print("before predict")    
    forecast = predict_sarimax(m, results_fit, train, test, folder_name, exp_name)
    print("after predict")        
    print(forecast)
    forecast = forecast.reset_index()
    forecast.index = forecast.index + len(train.index)
    print("before plot prediction")     
    plot_prediction_prophet(train["OccupancyRate"], test["OccupancyRate"], forecast['mean'], forecast['mean_ci_upper'], forecast['mean_ci_lower'], folder_name, exp_name)
    #plot_prediction_html(train["OccupancyRate"], test["OccupancyRate"], forecast['mean'], folder_name, exp_name)
    print("after plot prediction")         
    print("printing metrics")
    metrics_str = report_metrics(test["OccupancyRate"].squeeze(), forecast["mean"].squeeze(), folder_name, exp_name)
    print(metrics_str)    
  elif (algorithm_chosen == "SimpleRNN" or algorithm_chosen == "LSTM" or algorithm_chosen == "GRU"): 
    m = train_rnn(algorithm_chosen, train, folder_name, exp_name, window_size_chosen)
    forecast = predict_rnn(m, train, test, folder_name, exp_name, window_size_chosen)
    forecast = forecast.reset_index(drop=True)
    forecast.index = forecast.index + len(train.index)    
    print("forecast = " + str(forecast))
    plot_prediction_prophet(train["OccupancyRate"], test["OccupancyRate"], forecast, None, None, folder_name, exp_name)
    print("-------------------")
    print("Zforecast = " + str(forecast))
    print("test['OccupancyRate'] = " + str(test["OccupancyRate"]))
    #plot_prediction_html(train["OccupancyRate"], test["OccupancyRate"], forecast.to_numpy(), folder_name, exp_name)
    metrics_str = report_metrics(test["OccupancyRate"].squeeze(), forecast.squeeze(), folder_name, exp_name)
    print(metrics_str)
    '''
    m = train_lstm(algorithm_chosen, train, folder_name, exp_name, window_size_chosen)
    forecast = predict_lstm(algorithm_chosen, m, train, test, folder_name, exp_name, window_size_chosen)
    plot_prediction_prophet(train["OccupancyRate"], test["OccupancyRate"], forecast, None, None, folder_name, exp_name)
    metrics_str = report_metrics(test["OccupancyRate"].squeeze(), forecast.iloc[len(train.index):,].squeeze(), folder_name, exp_name)
    print(metrics_str)    
    '''
    
