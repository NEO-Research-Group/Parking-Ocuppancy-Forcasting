import os
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

import matplotlib.ticker as ticker

import seaborn as sns
sns.set_style('whitegrid')

from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from pandas.plotting import autocorrelation_plot


'''
def plot_parking_occupancy(df, name):
  """Plot parking occupancy
  """
  plt.figure(figsize=(30,20))
  plt.title('All data')
  plt.xlabel('Date')
  plt.ylabel('Percent Occupied')
  plt.plot(df["LastUpdated"], df["OccupancyRate"], label='Percent Occupied')
  plt.legend()

  plt.xticks(fontsize=8, rotation=90)


  plt.savefig('./plots/parking_occupancy_' + name + '.png')
  plt.cla()
  plt.clf()
'''


def plot_seasonality2(df, name, city):
  fig = plt.figure(figsize=(48,32))
  ax1 = fig.add_subplot(211)
  fig = plot_acf(df, lags=300, ax=ax1) #fig = plot_acf(series, lags=40, ax=ax1)
  ax2 = fig.add_subplot(212)
  fig = plot_pacf(df, lags=300, ax=ax2) #fig = plot_pacf(series, lags=40, ax=ax2)
  plt.savefig('./plots/' + city + '/seasonality2_' + name + '.png')
  plt.cla()
  plt.clf()

def plot_seasonality1(df, name, city):
  plt.figure(figsize=(48,6))
  plt.plot(df)
  plt.plot(df.shift(48))
  plt.xlabel('Date', fontsize=14);
  plt.savefig('./plots/' + city + '/seasonality1_' + name + '.png')
  plt.cla()
  plt.clf()



def plot_twodays_evolution(df, name, chosen_column, chosen_date_1, chosen_date_2, city):
  plt.plot([],[])
  rate = df[df[chosen_column] == name]
  rate = rate[rate['Date'] == chosen_date_1]['OccupancyRate']
  time = df[df[chosen_column] == name] 
  time=pd.to_datetime(time[time['Date'] == chosen_date_1]['Time'],format='%H:%M:%S')
  plt.plot(time,rate,label=chosen_date_1)

  rate = df[df[chosen_column] == name]
  rate = rate[rate['Date'] == chosen_date_2]['OccupancyRate']
  time = df[df[chosen_column] == name] 
  time=pd.to_datetime(time[time['Date'] == chosen_date_2]['Time'],format='%H:%M:%S')
  plt.plot(time,rate,label=chosen_date_2)

  plt.gcf().autofmt_xdate()
  myFmt = mdates.DateFormatter('%H:%M')
  plt.gca().xaxis.set_major_formatter(myFmt)
  plt.xlabel('Time')
  plt.ylabel('Occupancy Rate')
  plt.legend()
  plt.savefig('./plots/' + city + '/ocr_twodays_evolution_' + name + '.png')
  plt.cla()
  plt.clf()




def plot_ocr_perhour(df, name, chosen_column, city):

  rate = df[df[chosen_column] == name]['OccupancyRate']
  time=pd.to_datetime(df[df[chosen_column] == name]['Time'],format='%H:%M:%S')
  plt.scatter(time,rate,label=name)
  plt.gcf().autofmt_xdate()
  myFmt = mdates.DateFormatter('%H:%M')
  plt.gca().xaxis.set_major_formatter(myFmt)    
  plt.xlabel('Time')
  plt.ylabel('Occupancy Rate')
  plt.savefig('./plots/' + city + '/ocr_perhour_' + name + '.png')
  plt.cla()
  plt.clf()


def plot_ocr_line(df, name, chosen_column, city):
  """Plot line with evolution over time.
  """
  #plt.figure(figsize=(15,6)) #(246,96))
  plt.figure(figsize=(60,24)) #(246,96))
  rate = df['OccupancyRate']
  time=pd.to_datetime(df['Date'])
  plt.plot(time,rate)
  plt.gcf().autofmt_xdate()
  plt.xlabel('Date')
  plt.ylabel('Occupancy Rate')
  plt.legend()
  plt.savefig('./plots/' + city + '/ocr_line_' + name + '.png')
  plt.cla()
  plt.clf()
  #plt.show()

def plot_ocr_hour_scatter(df, name, chosen_column, city):
  """Plot scatter plot per hour.
  """
  plt.plot([],[])
  park_name = df[chosen_column].unique()
  for i in range(len(park_name)):
      s = park_name[i]
      rate = df[df[chosen_column] == s]['OccupancyRate']
      time=pd.to_datetime(df[df[chosen_column] == s]['Time'],format='%H:%M:%S')
      plt.scatter(time,rate,label=s)

  plt.gcf().autofmt_xdate()
  myFmt = mdates.DateFormatter('%H:%M')
  plt.gca().xaxis.set_major_formatter(myFmt)    
  plt.xlabel('Time')
  plt.ylabel('Occupancy Rate')
  plt.legend()

  plt.savefig('./plots/' + city + '/ocr_hour_scatter_' + name + '.png')
  plt.cla()
  plt.clf()

def plot_ocr_mean_barplot(df, name, chosen_column, city):
  """Plot barplot mean occupancy rate.
  """
  xData = df.groupby(chosen_column)['OccupancyRate'].mean()
  key_list = list(xData.keys()) 
  val_list = []
  for x in key_list:
      val_list.append(xData[x])
  df = pd.DataFrame(list(zip(key_list, val_list)), 
                 columns =['Park ID', 'Mean Occupancy Rate']) 
  ax = sns.barplot(y='Park ID',x='Mean Occupancy Rate',data=df,orient="h")
  ax.set(ylabel="Car Park ID", xlabel = "Mean Occupancy Rate")
  ax.tick_params(axis='y', labelsize=7)

  fig = ax.figure
  fig.savefig('./plots/' + city + '/ocr_mean_barplot_' + name + '.png', dpi=fig.dpi)
  plt.cla()
  plt.clf()


def plot_dow_barplot_count(df, name, city):
  """Plot number of samples per day of week.
  """
  figure(figsize=(16, 16), dpi=80)

  ax = sns.catplot(x='DayOfWeek',kind='count',data=df,orient="h")
  ax.fig.autofmt_xdate()
  ax.set(xlabel="Week Days", ylabel = "Count")

  fig = ax.figure
  fig.savefig('./plots/' + city + '/dow_count_' + name + '.png', dpi=fig.dpi)
  plt.cla()
  plt.clf()

def plot_dow_boxplot(df, name, city):
  """Plot boxplot per each day of week.
  """
  figure(figsize=(16, 16), dpi=80)
  ax = sns.catplot(x = "DayOfWeek",y="OccupancyRate",kind='box',data=df)
  ax.set(xlabel="Week Days", ylabel = "Occupancy Rate")
  ax.set(ylim=(0, 1))
  plt.legend(title='', loc='upper right', labels=[name])
  fig = ax.figure
  fig.savefig('./plots/' + city + '/dow_boxplot_' + name + '.png', dpi=fig.dpi)
  plt.cla()
  plt.clf()

def plot_heatmap(df, name, chosen_column, city):
  """Plot heatmap with evolution over time.
  """
  figure(figsize=(16, 16), dpi=80)

  heatmap_data = pd.pivot_table(df, values='OccupancyRate', 
                       index=[chosen_column], 
                       columns='Date')
  ax = sns.heatmap(heatmap_data , cmap="BuGn")
  ax.set(ylabel="Car Park ID", xlabel = "Date")

  fig = ax.figure
  fig.savefig('./plots/' + city + '/occupancy_heatmap_' + name + '.png', dpi=fig.dpi)
  plt.cla()
  plt.clf()

def plot_all(city):
  df = pd.read_csv('./datasets/' + city + '/csv_clean2.csv')
  df.LastUpdated = df.LastUpdated.astype('datetime64')
  df.OldLastUpdated = df.OldLastUpdated.astype('datetime64')
  df["Date"] = df['LastUpdated'].dt.date
  df["Time"] = df['LastUpdated'].dt.time
  df["DayOfWeek"] = df['LastUpdated'].dt.dayofweek
  chosen_column = 'Name' #'SystemCodeNumber'
  park_names = df[chosen_column].unique()

  chosen_date_1 = '2022-07-20' 
  chosen_date_2 = '2022-07-21' 

  if not os.path.exists('./plots/' + city):
    os.makedirs('./plots/' + city)
  #'''
  plot_heatmap(df, "all", chosen_column, city)
  plot_ocr_mean_barplot(df, "all", chosen_column, city)
  plot_ocr_hour_scatter(df, "all", chosen_column, city)
  #'''
  for i in range(len(park_names)):
    name = park_names[i]
    temp = df.loc[(df[chosen_column] == name) ]
    if not isinstance(name, str):
      name = str(name)
    '''
    plot_dow_boxplot(temp, name, city)
    plot_dow_barplot_count(temp, name, city)    
    plot_ocr_line(temp, name, chosen_column, city)
    ####plot_parking_occupancy(temp, name, city)
    plot_ocr_perhour(temp, name, chosen_column, city)
    plot_twodays_evolution(temp, name, chosen_column, chosen_date_1, chosen_date_2, city)
    '''
    '''
    plot_seasonality1(temp['OccupancyRate'], name, city)
    try:
      plot_seasonality2(temp['OccupancyRate'], name, city)
    except:
      pass
    '''      
  plt.close()

city = "birmingham"
plot_all(city)





