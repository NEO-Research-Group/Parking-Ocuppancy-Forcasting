from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
from datetime import datetime, timedelta, time




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
    
interval = 30

city = "birmingham" # "malaga"
minstd = None
if (city == "birmingham"):
  minstd = 0.05
elif (city == "malaga"):
  minstd = 0.005
else:
  print("ERROR: no city selected")
  exit()



df = pd.read_csv('../datasets/' + city + '/csv_clean.csv')
df.LastUpdated = df.LastUpdated.astype('datetime64')
df.OldLastUpdated = df.OldLastUpdated.astype('datetime64')


df = df.loc[df["SystemCodeNumber"] != "NIA North"]
df = df.loc[df["SystemCodeNumber"] != "BHMBRTARC01"]



all_ids = df["SystemCodeNumber"].unique()

print(all_ids)
for theid in all_ids:
  print("theid = " + str(theid))
  days_low_std = df.loc[df["SystemCodeNumber"] == theid]
  days_low_std["Date"] = days_low_std['LastUpdated'].dt.date
  thestd = days_low_std.groupby("Date")['OccupancyRate'].std()
  thestd = thestd.reset_index()
  thestd = thestd.loc[thestd['OccupancyRate'] < minstd ]
  print("thestd = " + str(thestd))

  thedates = thestd["Date"]


  for dd in thedates:
    #Take next day to copy from
    next_day = (dd + timedelta(days = 7))

    while pd.Timestamp(next_day) in list(map(lambda d : pd.Timestamp(d), thedates)): #list( map( thedates, pd.Timestamp(d) )):
      #print("while " + str(next_day))
      next_day = (next_day + timedelta(days = 7))
    
    if pd.Timestamp(next_day) > pd.Timestamp(days_low_std['LastUpdated'].max()):
      next_day = (dd - timedelta(days = 7))
      while next_day in thedates:
        next_day = (next_day - timedelta(days = 7))    
        
    if ( pd.Timestamp(next_day) < pd.Timestamp(days_low_std['LastUpdated'].min()) or pd.Timestamp(next_day) > pd.Timestamp(days_low_std['LastUpdated'].max()) ):
      print("ERROR")
      continue
      #exit()
    next_day = datetime(next_day.year, next_day.month, next_day.day)
    next_day = next_day.replace(hour = 0, minute = 0, second = 0)


    min_date = datetime(dd.year, dd.month, dd.day)
    min_date = min_date.replace(hour = 0, minute = 0, second = 0)
    max_date = min_date + timedelta(minutes = 1440 - interval)

    list_round_dates = list(date_range(min_date, max_date, timedelta(minutes = 30)))
    #print(list_round_dates)
    #'''
    for tt in list_round_dates:
      next_day = next_day.replace(hour = tt.hour, minute = tt.minute, second = tt.second)
      #if (tt.hour == 0 and tt.minute == 0 and tt.second == 0):
      #  print("theid = " + str(theid) + " day = " + str(tt) + " next_day = "  + str(next_day))

      try:
        days_low_std.loc[days_low_std["LastUpdated"] == tt, "OccupancyRate" ] = days_low_std.loc[days_low_std["LastUpdated"] == next_day]["OccupancyRate"].iloc[0]
      except:
        print("ERROR: Next day does not exists.")      
        print(next_day)
        exit()

         

      #print(days_low_std)
    #'''      
  df.loc[df["SystemCodeNumber"] == theid] = days_low_std
  #exit()

#'''   
if (city=="birmingham"):
  df["SystemCodeNumber"] = df["Name"]    
  df = df.loc[ (df["LastUpdated"].dt.time > time(7,30)) & (df["LastUpdated"].dt.time < time(17,0)) ] 
#'''

print(df.groupby("Name").max())
print(df.groupby("Name").min())
print(df.describe())
print(df["Name"].unique())
print(len(df["Name"].unique()))

df.to_csv("../datasets/" + city + "/csv_clean2.csv")

