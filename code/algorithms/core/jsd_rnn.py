import pandas as pd
import numpy as np
import json
import tensorflow as tf
from keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.metrics import RootMeanSquaredError, MeanAbsoluteError, MeanSquaredError, MeanSquaredLogarithmicError
from tensorflow.keras.models import Sequential
from keras.layers import Dense, SimpleRNN, LSTM, GRU
import tensorflow_datasets as tfds
from keras.preprocessing.sequence import TimeseriesGenerator
from jsd_draw import plot_prediction_prophet, plot_prediction_html



def windowed_dataset(series, look_back, batch_size): 
	dataset = tf.data.Dataset.from_tensor_slices(series)
	dataset = dataset.window(look_back + 1, shift=1, drop_remainder=True)
	dataset = dataset.flat_map(lambda window: window.batch(look_back + 1))
	dataset = dataset.map(lambda window: (window[:-1], window[-1]))
	dataset = dataset.batch(batch_size, drop_remainder=True).prefetch(1) #, 
	return dataset	
	

params = {
  "loss": "mean_absolute_error", #"mean_squared_error",
  "optimizer": "adam",
  "dropout": 0.2,
  "lstm_units": 60, #50, #60, #60
  "epochs": 5000,#1000,#1000, #30,
  "batch_size": 64,#32, #128,
  "es_patience" : 10,
  "n_features" : 1
}



def get_model(model_type, units, theshape, verbose=False):
  m = None
  if (model_type == "SimpleRNN"):
    m = SimpleRNN
  elif (model_type == "LSTM"):
    m = LSTM    
  elif (model_type == "GRU"):
    m = GRU     
  else:
    print("model_type = " + model_type)
    print("ERROR: model_type does not exists")
    exit()    
  model = Sequential()
  '''
  #Adding the first LSTM layer and some Dropout regularisation
  model.add(LSTM(units = units, return_sequences = True, input_shape = theshape))
  model.add(Dropout(params["dropout"]))
  # Adding a second LSTM layer and some Dropout regularisation
  model.add(LSTM(units = units, return_sequences = True))
  model.add(Dropout(params["dropout"]))
  # Adding a third LSTM layer and some Dropout regularisation
  model.add(LSTM(units = units, return_sequences = True))
  model.add(Dropout(params["dropout"]))
  # Adding a fourth LSTM layer and some Dropout regularisation
  model.add(LSTM(units = units))
  model.add(Dropout(params["dropout"]))
  # Adding the output layer
  model.add(Dense(units = 1))
  '''
  
  model.add(m (units = units, return_sequences = True, input_shape = theshape)) #, stateful = True
  #model.add(m (units = units, return_sequences = True, batch_input_shape = theshape, stateful = True))  
  #model.add(m (units = units, return_sequences = True, batch_input_shape = theshape, stateful = True)) #, input_shape = theshape #[nbatch, x_train_np.shape[1], x_train_np.shape[2]]
  model.add(Dropout(params["dropout"]))
  model.add(m (units = units))
  model.add(Dropout(params["dropout"]))
  model.add(Dense(units = 1))
  # Compile Model
  #model.compile(loss='mse', optimizer='adam')
  
  model.compile(loss=params["loss"], optimizer=params["optimizer"], metrics=[RootMeanSquaredError(), MeanAbsoluteError(), MeanSquaredError(), MeanSquaredLogarithmicError()])    
  return model


def _predict(train_dataset, num_prediction, model, look_back):
    prediction_list = train_dataset[-look_back:]
    
    for _ in range(num_prediction):
        x = prediction_list[-look_back:]
        x = x.reshape((1, look_back, 1))
        out = model.predict(x)[0][0]
        prediction_list = np.append(prediction_list, out) #pd.concat([prediction_list, out]) #np.append(prediction_list, out)
    prediction_list = prediction_list[look_back-1:]
        
    return prediction_list



def train_rnn(model_type, train, folder_name, exp_name, look_back = 48):
  mytrain = train.copy()
  
  train_dataset = windowed_dataset(mytrain['OccupancyRate'], look_back, params["batch_size"])

  model = get_model(model_type, params["lstm_units"], (look_back, params["n_features"]), verbose=False) #SimpleRNN, GRU
  #model = get_model(model_type, params["lstm_units"], (params["batch_size"], look_back, params["n_features"]), verbose=False)
  
  #early_stopping_callback = tf.keras.callbacks.EarlyStopping(monitor='val_root_mean_squared_error', mode='min', patience=params["es_patience"])
  
  history = model.fit(
    train_dataset,
	  #validation_data=(X_validation, y_validation),
	  epochs=params["epochs"],
	  batch_size=params["batch_size"],
	  shuffle=False,
	  verbose=1
	  #,
	  #callbacks=[early_stopping_callback]
  )
  model.reset_states()
  
  model.save_weights("../../results/" + folder_name + '/model_' + exp_name + '.h5')
    
  with open("../../results/" + folder_name + '/history_' + exp_name + '.json', 'w') as f:
    f.write(json.dumps(history.history))  # Save model 

  return model



def predict_rnn(m, train, test, folder_name, exp_name, look_back = 48):
  mytrain = train.copy()['OccupancyRate'].to_numpy()  
  mytest = test.copy()['OccupancyRate'].to_numpy()  
  num_prediction = len(mytest) - 1 #- 1
  print("num_prediction = " + str(num_prediction))
  forecast = _predict(mytrain, num_prediction, m, look_back)
  
   
  #plot_prediction_html(train["OccupancyRate"], test["OccupancyRate"], forecast, folder_name, exp_name)
  forecast = pd.DataFrame(forecast.tolist(), columns=["OccupancyRate"])

  forecast.to_csv("../../results/" + folder_name + '/forecast_' + exp_name + '.csv')
  
  #m.plot(forecast).savefig("../../results/" + folder_name + '/forecast_' + exp_name + '.png')
 
  return forecast
  
