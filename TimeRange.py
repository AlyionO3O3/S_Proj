#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 02:58:05 2022

@author: alyion
"""
import os
import pandas as pd
from datetime import datetime as d
import time
from tqdm import tqdm


def time_range(df):
    timerange = []
    for i in range(len(df)):
        on = df["On"][i].hour*60 + df["On"][i].minute
        if df["Off"][i].hour == 0:
            off = 1440
        else:
            off = df["Off"][i].hour*60 + df["Off"][i].minute
        timerange.append([on,off])
    df["Range"] = timerange

def doctor_time(df):
    DocCol = []
    SurCol = []
    DurCol = []
    for i in tqdm(df.Doctor.unique(), desc= "Data Processing, please hold..."):
        x = set()
        for j in df[df.Doctor == i].index:
            y = range(df.Range[j][0],df.Range[j][1])
            if j == df[df.Doctor == i].index[0]:
                set(y)
                x = x.union(y)
            elif df.Date[j] > df.Date[j-1]:
                date = df.Date[j-1]
                Total_time = len(x)
                DocCol.append(i)
                DurCol.append(Total_time)
                SurCol.append(date)
                x = set()
                set(y)
                x = x.union(y)
            else:
                set(y)
                x = x.union(y)
        Total_time = len(x)
        date = df.Date[j]
        Total_time = len(x)
        DocCol.append(i)
        DurCol.append(Total_time)
        SurCol.append(date)
        x = set()
    new_df = pd.DataFrame({'Doctor': DocCol, 'Surgery Date': SurCol, 'Duration':DurCol})
    new_df.to_csv("開刀時間.csv",header=True)

####################
####################

test_df = pd.read_csv("正式.csv",header=0)

start = time.time()
test_df = test_df[['手術主治醫師', '手術日期', '下刀', '手術結束']]
test_df.columns = ["Doctor", "Date", "On", "Off"]
test_df["Date"] = test_df.apply(lambda r: d.strptime(r["Date"], '%Y/%m/%d').date(), axis=1)
test_df["On"] = test_df.apply(lambda r: d.strptime(r["On"], '%Y/%m/%d %H:%M').time(), axis=1)
test_df["Off"] = test_df.apply(lambda r: d.strptime(r["Off"], '%Y/%m/%d %H:%M').time(), axis=1)


time_range(test_df)
doctor_time(test_df)


end = time.time()
optime = end - start
print(f"You used {optime} seconds for this run.")


    
    
    
    
    