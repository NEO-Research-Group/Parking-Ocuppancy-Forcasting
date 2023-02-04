import pandas as pd



def load_dataset(city_chosen, parking_chosen, day_of_week_chosen, cross_validation_chosen):
  train = pd.read_csv('../../datasets/' + city_chosen + '/train_' + parking_chosen + '_' + str(cross_validation_chosen) + '.csv')
  test = pd.read_csv('../../datasets/' + city_chosen + '/test_' + parking_chosen + '_' + str(cross_validation_chosen) + '.csv')


  if (day_of_week_chosen >= 0 and day_of_week_chosen <= 6):
    train = train[pd.to_datetime(train.LastUpdated).dt.dayofweek == day_of_week_chosen]
    test = test[pd.to_datetime(test.LastUpdated).dt.dayofweek == day_of_week_chosen]
  
  train = train.reset_index()
  test = test.reset_index()
  test.index = test.index + len(train)
  print(train)
  del train[train.columns[0]]
  del train[train.columns[0]]
  del test[test.columns[0]]
  del test[test.columns[0]]

  return train, test  
