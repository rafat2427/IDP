import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os.path

csv1 = pd.read_csv("eegIDRecord.csv")
csv_hr = pd.read_csv("HEARTRATE_AUTO_1610560932667.csv")
# print(csv1)
yourpath="Output"
parent_dir = os.path.abspath(os.path.join(yourpath, os.pardir))
path = os.path.join(parent_dir, yourpath)

try:
    os.makedirs(path, exist_ok = True)
    print("Directory '%s' created successfully" % yourpath)
except OSError as error:
    print("Directory '%s' can not be created" % yourpath)

df = pd.DataFrame(columns= ['timestampMs','date','time'])
# df = pd.DataFrame(columns= ['timestampMs','date','time','second'])


df['timestampMs'] = pd.to_datetime(csv1['timestampMs'], unit='ms')
# print (df)

df['timestampMs'] = pd.to_datetime(df.timestampMs)
## Adding Hours
hours_to_add = 6 #Defining the time zone UTC+06
df['timestampMs'] = df['timestampMs'] + timedelta(hours = hours_to_add) #Converting to local time zone
df['date'] = df['timestampMs'].dt.strftime('%m/%d/%Y')
df['time'] = df['timestampMs'].dt.strftime('%H:%M')
# print ( df['time'].dtypes)


csv1['timestampMs'] = pd.to_datetime(csv1['timestampMs'], unit='ms')
csv1['timestampMs'] = csv1['timestampMs'] + timedelta(hours = hours_to_add)
# print (csv1.head())
merged_data_eeg = pd.DataFrame
merged_data_eeg = csv1.merge(df,on=["timestampMs"])
# print(merged_data_eeg)


csv_hr['date'] = pd.to_datetime(csv_hr.date)
csv_hr['date'] = csv_hr['date'].dt.strftime('%m/%d/%Y')
print (csv_hr.head())
merged_data_all = pd.DataFrame
merged_data_all = merged_data_eeg.merge(csv_hr,on=["date","time"])
merged_data_all['timestampMs'] = merged_data_all['timestampMs'] - timedelta(hours = hours_to_add) #Converting to UTC
merged_data_all['timestampMs'] = merged_data_all.timestampMs.values.astype(np.int64)              #Converting to Timestamp ns
merged_data_all.rename(columns = {'timestampMs':'timestampNs'}, inplace = True)
print(merged_data_all.head())


merged_data_all.to_csv("Output/heart_rate.csv", index= None, columns=['time','heartRate'])
merged_data_all.to_csv("Output/alpha.csv", index= None, columns=['time','alphaLow','alphaHigh'])
merged_data_all.to_csv("Output/beta.csv", index= None, columns=['time','betaLow','betaHigh'])
merged_data_all.to_csv("Output/model_input.csv", index= None, columns=['timestampNs','heartRate','alphaLow','alphaHigh','betaLow','betaHigh','attention','meditation','blinkStrength'])
