#COGEMOS EL VALOR MÁS CERCANO
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
pd.options.display.max_rows = 500
def date_range(*args):
    if len(args) != 3:
        return range(*args)
    start, stop, step = args
    if start < stop:
        cmp = lambda a, b: a < b
        inc = lambda a: a + step
    else:
        cmp = lambda a, b: a > b
        inc = lambda a: a - step
    output = [start]
    while cmp(start, stop):
        start = inc(start)
        output.append(start)
    return output

#Intervalo que se va a utilizar para redondear las fechas en minutos (Ej: 30 min)
interval = 30
city = "birmingham"

dataset_url = '../datasets/' + city + '/csv_raw.csv'


temp_data = pd.read_csv(dataset_url)

temp_data["LastUpdated"] = temp_data["LastUpdated"].astype('datetime64')
temp_data.sort_values(['LastUpdated', 'SystemCodeNumber'], ascending=[True, True])


########################
if (city == "birmingham"):
  temp_data["Name"] = temp_data["SystemCodeNumber"]
  all_ids = temp_data["SystemCodeNumber"].unique()

  for theid in all_ids:
    temp_data.loc[temp_data.SystemCodeNumber == theid, 'Capacity'] = temp_data.loc[temp_data.SystemCodeNumber == theid, 'Capacity'].max()

  # Ids con capacidad equivocada los eliminamos
  temp_data = temp_data.loc[temp_data.Capacity >=0]
  
  temp_data['OccupancyRate'] = temp_data['Occupancy'] / temp_data['Capacity']
  
  # Ids con OccupancyRate equivocada los eliminamos
  temp_data = temp_data.loc[temp_data.OccupancyRate >= 0]
  temp_data = temp_data.loc[temp_data.OccupancyRate <= 1]

########################


#Redondeamos fechas con un intervalo (quedan huecos así que luego rellenamos los huecos con la fecha más cercana disponible).
temp_data["TimeRounded"] = temp_data["LastUpdated"].round(str(interval) + 'min')
temp_data["TimeRounded"] = temp_data["TimeRounded"].astype('datetime64')


temp_data["OldLastUpdated"] = temp_data["LastUpdated"]


#ELIMINAMOS DUPLICADOS
temp_data = temp_data.drop_duplicates(subset=['SystemCodeNumber', 'LastUpdated'], keep='first')


#Rellenamos los huecos con la fecha más cercana disponible
ids_parking = temp_data['SystemCodeNumber'].unique()
final_temp = pd.DataFrame()
for id in ids_parking:
  parking_data = temp_data.loc[(temp_data['SystemCodeNumber'] == id)]
  
  #Cogemos fecha máxima y mínima.
  min_date = parking_data['LastUpdated'].min()
  min_year = min_date.year
  min_month = min_date.month
  min_day = min_date.day

  max_date = parking_data['LastUpdated'].max()
  max_year = max_date.year
  max_month = max_date.month
  max_day = max_date.day

  #Eliminamos datos que se pasen de la fecha máxima. Por ejemplo si cogemos los días del 1 al 30, al redondear puede pasar al siguiente mes cosa que no queremos.  
  parking_data = parking_data.loc[parking_data["TimeRounded"] <  (max_date + pd.to_timedelta(1, unit='D')).replace(hour=0, minute=0, second=0, microsecond=0) ]
    

  min_date = min_date.replace(hour = 0, minute = 0, second = 0)
  max_date = max_date.replace(hour = 23, minute = 60 - interval, second = 0)

  list_round_dates = list(date_range(min_date, max_date, timedelta(minutes=interval)))

  df_round_dates = pd.DataFrame({"TimeRounded" :list_round_dates })  
  
  empty_dates = df_round_dates[ ~df_round_dates['TimeRounded'].isin(parking_data['TimeRounded'])] 
  parking_data = parking_data.set_index("LastUpdated") 
  print(empty_dates)
  
  for current_date in empty_dates["TimeRounded"]:
    print(current_date)
         
    closest_date = parking_data.index[parking_data.index.get_loc(current_date, method='nearest')]
    #print("current_date = " + str(current_date) + " " + "closest_date = " + str(closest_date))
    
    selected_row = temp_data.loc[(temp_data['SystemCodeNumber'] == id) & (temp_data['LastUpdated'] == closest_date)].copy() 
    modified_date = closest_date.replace(day = current_date.day, hour=current_date.hour, minute=current_date.minute, second=current_date.second)

    selected_row["TimeRounded"] = modified_date
    final_temp = final_temp.append(selected_row)
        
  parking_data = parking_data.reset_index(drop=True)




print(df_round_dates[ ~df_round_dates['TimeRounded'].isin(temp_data['TimeRounded']) ].shape[0] )
print(df_round_dates[ df_round_dates['TimeRounded'].isin(temp_data['TimeRounded']) ].shape[0] )


temp_data = temp_data.append(final_temp)

print(df_round_dates[ ~df_round_dates['TimeRounded'].isin(temp_data['TimeRounded']) ].shape[0] )
print(df_round_dates[ df_round_dates['TimeRounded'].isin(temp_data['TimeRounded']) ].shape[0] )


temp_data = temp_data.sort_values(['TimeRounded', 'OldLastUpdated'], ascending=[True, True])


#ELIMINAMOS DUPLICADOS
temp_data = temp_data.drop_duplicates(subset=['SystemCodeNumber', 'TimeRounded'], keep='first')

print(df_round_dates[ ~df_round_dates['TimeRounded'].isin(temp_data['TimeRounded']) ].shape[0] )
print(df_round_dates[ df_round_dates['TimeRounded'].isin(temp_data['TimeRounded']) ].shape[0] )


#################
#temp_data['DayOfWeek'] = temp_data.TimeRounded.dt.dayofweek


temp_data['LastUpdated'] = temp_data['TimeRounded']

#Removing TimeRounded column (now LastUpdated is the timerounded column)
temp_data = temp_data.drop('TimeRounded', axis=1)



if (city == "malaga"):
  del temp_data[temp_data.columns[0]]




print(temp_data)
temp_data.describe()
temp_data.to_csv("../datasets/" + city + "/csv_clean.csv")
