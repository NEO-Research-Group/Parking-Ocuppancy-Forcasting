import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import datetime
from datetime import timedelta 
import math

final_dataset = pd.DataFrame()

file_errors = []

year = "2022"
months = listdir(year)
months.sort()
for month in months:
  days = listdir(year + "/" + month)
  days.sort()
  for day in days:
    location = year + "/" + month + "/" + day
    fdate = year + "-" + month + "-" + day
    onlyfiles = [f for f in listdir(location) if isfile(join(location, f))]
    onlyfiles.sort()

    print("trying " + (str(year) + '-' + str(month) + '-'  + str(day)))
    for f in onlyfiles:
      if "csv" in f:
        flocation = year + "/" + month + "/" + day + "/" + f
      
        hour = f.split("-")[2].split(".")[0]
        temp = hour.split("_")
        hour = temp[0]
        minutes = temp[1]
       
        minutes = str(minutes)
        hour = str(hour)
        fhour = "" + hour + ":" + minutes + ":00"

        try:
          read_file = pd.read_csv(flocation)
          #Eliminamos filas de las que no tenemos información de plazas libres
          read_file = read_file.loc[(read_file['libres'] >= 0 )]

          capacity = read_file["capacidad"].replace("None", "-1").astype(int) 
          poiID = read_file["poiID"].astype(int) 


          filedf = {'SystemCodeNumber': poiID, 'Name': read_file["nombre"], 'Latitude': read_file["latitude"], 'Longitude': read_file["longitude"], 'Altitude': read_file["altitud"], 'Capacity': capacity, 'LastUpdated': "" + fdate + " " + fhour, 'Free': read_file["libres"]}
          filedf = pd.DataFrame(filedf)
          final_dataset = final_dataset.append(filedf) 
        except Exception as e:
          file_errors.append(flocation)
          print("error en el archivo " + flocation + " - error: " + str(e))


print("File Errors:")
print(file_errors)


all_ids = final_dataset["SystemCodeNumber"].unique()
print(all_ids)

for theid in all_ids:
  final_dataset.loc[final_dataset.SystemCodeNumber == theid, 'Capacity'] = final_dataset.loc[final_dataset.SystemCodeNumber == theid, 'Capacity'].max()


# Ids con capacidad equivocada los eliminamos
final_dataset = final_dataset.loc[final_dataset.Capacity >=0]


final_dataset['Occupancy'] = final_dataset['Capacity'] - final_dataset['Free']
final_dataset['OccupancyRate'] = final_dataset['Occupancy'] / final_dataset['Capacity']


print(final_dataset)


if not os.path.exists('./datasets/malaga/'):
   os.makedirs('./datasets/malaga/')
   
final_dataset.to_csv("./datasets/malaga/csv_raw.csv")

