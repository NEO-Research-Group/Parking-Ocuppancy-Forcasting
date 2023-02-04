from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
from calendar import monthrange
from datetime import timedelta, time
import datetime
city = "malaga"#"malaga" # "birmingham"
data_per_day = 48 #48 # 18
choose_split = "month" # "week" "twoweeks" "threeweeks" "month"



df = pd.read_csv('../datasets/' + city + '/csv_clean2.csv')
df.LastUpdated = df.LastUpdated.astype('datetime64')
#'''   
if (city=="birmingham"): 
  df = df.loc[ (df["LastUpdated"].dt.time > time(7,30)) & (df["LastUpdated"].dt.time < time(17,0)) ] 
#'''


chosen_column = 'Name' 
park_names = df[chosen_column].unique()

for i in range(len(park_names)):
  name = park_names[i]
  temp = df.loc[(df[chosen_column] == name) ]
  temp = temp.reset_index()[['LastUpdated', 'OccupancyRate']]
  if not isinstance(name, str):
    name = str(name)
    
        
  #total_days = temp.shape[0] / data_per_day
  #print(total_days) 
  
  split_location = None
  if (choose_split == "week"):
    split_location = int(7 * data_per_day)
  elif (choose_split == "twoweeks"):
    split_location = int(14 * data_per_day)    
  elif (choose_split == "threeweeks"):
    split_location = int(21 * data_per_day)      
  elif (choose_split == "month"):
    last_date = temp["LastUpdated"].max() #datetime.datetime.fromisoformat(temp["LastUpdated"].max())
    last_month = last_date.month
    last_year = last_date.year 
    n_days_in_last_month = monthrange(last_year, last_month)[1]
    split_location = int(n_days_in_last_month * data_per_day)
 
  train = temp[:-split_location]
  test = temp[len(train):]
  
    
  train.to_csv("../datasets/" + city + "/train_" + name + "_" + choose_split + ".csv") 
  test.to_csv("../datasets/" + city + "/test_" + name + "_" + choose_split + ".csv")   
  


