# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 10:32:20 2025

@author: lazar
"""


import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ---- import data from csv files ---------#

# 1) Import daily cases and deaths
all_data=[]
with open('daily_casesUK.csv', newline='') as csvfile:
    daily_dataUK = csv.reader(csvfile,delimiter=',')
    for row in daily_dataUK:
        all_data.append(row)
        
# Clean data and create numpy arrays by splitting across commas

# get time/dates for measurements
time= all_data[1][0].strip().split('","')
# get daily cases and convert to float from string        
cases= all_data[1][1].strip().split(',')
cases= np.array([float(cases[x]) for x in range(len(cases))])
# get daily deaths
deaths= all_data[1][2].strip().split(',')
# clean error in deaths data to match the number of values in the other lists
deaths=deaths[:1519]
deaths[1518]=0
# convert to float from string
deaths= np.array([float(deaths[x]) for x in range(len(deaths))])
        
# 2) Import vaccination rates for over 12 year olds
date=[]
vac1_rates=[]
vac2_rates=[]
vac3_rates=[]
with open('vacc.csv') as csvfile:
    vac_rates = csv.reader(csvfile)
    for row in vac_rates:
        date.append(row[0])
        vac1_rates.append(row[1])
        vac2_rates.append(row[2])
        vac3_rates.append(row[3])

# remove first and last row and convert to arrays
vac1_rates=np.array([float(vac1_rates[x]) for x in range(1, len(vac1_rates)-1)])
vac2_rates=np.array([float(vac2_rates[x]) for x in range(1, len(vac2_rates)-1)])
vac3_rates=np.array([float(vac3_rates[x]) for x in range(1, len(vac3_rates)-1)])

# convert dates from vaccination rates to match date format of daily data
# Original date string
formatted_date=[]
for i in range(1,len(date)-1):
    # Convert to datetime object
    date_conv = datetime.strptime(date[i], "%d/%m/%Y")
    
    # Format to desired string format
    formatted_date.append(date_conv.strftime("%b %d, %Y"))

# visualize cases with bar charts
plt.figure(figsize=(11.60,5.50))
plt.rc('font', size= 12)
plt.grid(axis='y',color = 'k', linestyle = '--', linewidth = 0.5,alpha=0.5)
#plt.bar(time,cases,linewidth=0,width=1)#,alpha=0.7)
#plt.scatter(time,cases, s=5)
plt.plot(time,cases,linewidth=1.5)
xlabels= time[0:len(time):100]
plt.xticks(ticks=np.linspace(0,len(cases),len(xlabels)),
           labels=xlabels, rotation=70)
#plt.xlabel('Time')
plt.ylabel('Novel COVID-19 Daily Cases')
plt.title('Daily New Cases in the UK')
plt.ylim(0,300000)
ylabels= ['0','100k','200k','300k']
plt.yticks(ticks=np.linspace(0,300000,4),labels=ylabels)
#plt.savefig('bar_cases_better.png', dpi=100)
plt.tight_layout()
plt.show() 


# visualize deaths with bar charts
plt.figure(figsize=(11.60,5.50))
plt.grid(axis='y',color = 'k', linestyle = '--', linewidth = 0.5)
plt.bar(time,deaths,linewidth=0,width=1,alpha=0.7)
xlabels= time[0:len(time):100]
plt.xticks(ticks=np.linspace(0,len(cases),len(xlabels)),
           labels=xlabels, rotation=70)

#plt.yticks(ticks=np.linspace(0,300000,4),labels=ylabels)
#plt.savefig('bar_cases.png', dpi=100)
plt.ylabel('Novel COVID-19 Daily Deaths')
plt.tight_layout()
plt.show() 


# line plots with moving averages

mov_avg3= np.ones(3,)/3  # for 3 days
mov_avg7= np.ones(7,)/7  # for 7 days

cases_sm3=np.convolve(cases,mov_avg3,mode='same')
cases_sm7=np.convolve(cases,mov_avg7,mode='same')

plt.figure(figsize=(11.60,5.50))
plt.rc('font', size= 12)
plt.grid(axis='y',color = 'k', linestyle = '--', linewidth = 0.5,alpha=0.5)
plt.bar(time,cases,linewidth=0,width=1,alpha=0.7,label= 'counts')
#plt.scatter(time,cases, s=5)
#plt.plot(time,cases_sm3,c='red',linewidth=2,
#         alpha=0.5,label='3-day moving average')
plt.plot(time,cases_sm7,c='red',linewidth=3,
        alpha=0.6,label='7-day moving average')
xlabels= time[0:len(time):100]
plt.xticks(ticks=np.linspace(0,len(cases),len(xlabels)),
           labels=xlabels, rotation=70)
#plt.xlabel('Time')
plt.ylabel('Novel COVID-19 Daily Cases')
plt.title('Daily New Cases in the UK')
plt.ylim(0,300000)
ylabels= ['0','100k','200k','300k']
plt.yticks(ticks=np.linspace(0,300000,4),labels=ylabels)
#plt.savefig('bar_cases_better.png', dpi=100)
plt.legend()
plt.tight_layout()
plt.show() 


# highlight lockdowns with shaded rectangles
lock1='Mar 16, 2020'
ease1='Jun 23, 2020'
lock2= 'Nov 05, 2020'
ease2= 'Dec 02, 2020'
lock3= 'Jan 05, 2021'
ease3= 'Mar 08, 2021'

# covid variants
v_alpha='Sep 01, 2020'
v_beta= 'Dec 01, 2020'
v_gamma= 'Feb 01, 2021'
v_delta= 'Mar 01, 2021'
v_omicron= 'Nov 01, 2021'

plt.figure(figsize=(11.60,5.50))
plt.rc('font', size= 12)
plt.grid(axis='y',color = 'k', linestyle = '--', linewidth = 0.5,alpha=0.5)
plt.bar(time,cases,linewidth=0,width=1,alpha=0.6,label= 'counts')
#plt.scatter(time,cases, s=5)
#plt.plot(time,cases_sm3,c='red',linewidth=2,
#         alpha=0.5,label='3-day moving average')
ceil_y=150000
plt.axvspan(xmin=time.index(lock1), xmax=time.index(ease1), facecolor='k',
            ymin=0,ymax=ceil_y,alpha=0.4,label='Lockdowns')
plt.axvspan(xmin=time.index(lock2), xmax=time.index(ease2),facecolor='k', 
            ymin=0,ymax=ceil_y,alpha=0.4)
plt.axvspan(xmin= time.index(lock3), xmax=time.index(ease3),facecolor='k',
            ymin=0,ymax=ceil_y,alpha=0.4)
plt.plot(time,cases_sm7,c='red',linewidth=3,
        alpha=0.7,label='7-day moving average')

plt.axvline(x=time.index(v_alpha),linestyle='--',linewidth=2.5,c='k',
            label='Covid-19 variants')
plt.axvline(x=time.index(v_beta),linestyle='--',linewidth=2.5,c='k')
plt.axvline(x=time.index(v_gamma),linestyle='--',linewidth=2.5,c='k')
plt.axvline(x=time.index(v_delta),linestyle='--',linewidth=2.5,c='k')
plt.axvline(x=time.index(v_omicron),linestyle='--',linewidth=2.5,c='k')

xlabels= time[0:len(time):100]
plt.xticks(ticks=np.linspace(0,len(cases),len(xlabels)),
           labels=xlabels, rotation=70)
#plt.xlabel('Time')
plt.ylabel('Novel COVID-19 Daily Cases')
plt.title('Daily New Cases in the UK')
plt.ylim(0,300000)
ylabels= ['0','100k','200k','300k']
plt.yticks(ticks=np.linspace(0,300000,4),labels=ylabels)
#plt.savefig('bar_cases_better.png', dpi=100)
plt.legend()
plt.tight_layout()
plt.show() 


# plot vaccination rates
plt.figure(figsize=(11.60,5.50))
plt.rc('font', size= 12)
plt.grid(axis='y',color = 'k', linestyle = '--', linewidth = 0.5,alpha=0.5)
plt.plot(formatted_date,vac1_rates,c='blue',linewidth=2.5,
         label='1st dose')
plt.plot(formatted_date,vac2_rates,c='red',linewidth=2.5,
         label='2nd dose')
plt.plot(formatted_date,vac3_rates,c='green',linewidth=2.5,
         label='three or more')
xlabels= formatted_date[0:len(formatted_date):30]
plt.xticks(ticks=np.linspace(0,len(vac1_rates),len(xlabels)),
           labels=xlabels, rotation=70)
plt.ylabel('% of people vaccinated')
plt.tight_layout()
plt.legend()


# plot vaccination rates with double y axis
f_date=np.arange(330,330+600,2)
fig, ax1 = plt.subplots(figsize=(11.60,5.50))
plt.rc('font', size= 12)

# lockdowns
# ceil_y=1600
# ax1.axvspan(xmin=time.index(lock1), xmax=time.index(ease1), facecolor='k',
#             ymin=0,ymax=ceil_y,alpha=0.4,label='Lockdowns')
# ax1.axvspan(xmin=time.index(lock2), xmax=time.index(ease2),facecolor='k', 
#             ymin=0,ymax=ceil_y,alpha=0.4)
# ax1.axvspan(xmin= time.index(lock3), xmax=time.index(ease3),facecolor='k',
#             ymin=0,ymax=ceil_y,alpha=0.4)

# bar plot with daily deaths
ax1.bar(np.arange(0,len(time)),deaths,linewidth=0,width=1,
         alpha=0.7,label= 'deaths')
ax2= ax1.twinx()


# line plots with vaccination rates
ax2.plot(f_date,vac1_rates,c='orange',linewidth=2.5,
         label='1st dose')
ax2.axhline(y = vac1_rates[-1], xmin=f_date[-1]/1519,
           xmax=1, alpha=0.5,
           color= 'orange',linewidth=2.5,linestyle='dashed')
ax2.plot(f_date,vac2_rates,c='red',linewidth=2.5,
         label='2nd dose')
ax2.axhline(y = vac2_rates[-1], xmin=f_date[-1]/1519,
           xmax=1, alpha=0.5,
           color= 'red',linewidth=2.5,linestyle='dashed')
ax2.plot(f_date,vac3_rates,c='green',linewidth=2.5,
         label='three or more')
ax2.axhline(y = vac3_rates[-1], xmin=f_date[-1]/1519,
           xmax=1, alpha=0.5,
           color= 'green',linewidth=2.5,linestyle='dashed')



ax1.set_ylabel('Novel COVID-19 Daily Deaths')
xlabels= time[0:len(time):100]
ax1.set_xticks(np.linspace(0,len(time),len(xlabels)))
ax1.set_xticklabels(labels=xlabels, rotation=70)
ax2.set_ylabel('% of people vaccinated')
plt.tight_layout()
ax1.legend(loc='lower right')
ax2.legend(loc='center right')
