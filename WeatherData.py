# Author: Louis Mungin

import json
from urllib2 import urlopen
from pprint import pprint
import pandas as pd
from pandas.io.json import json_normalize
import time
import csv

#This way would generalize better but has limitations due to API request limits, another method is used below

##Function takes a date in YYYYMMDD format and a city in String format (assumption: we're in VA)
#def getWeather(date,city): 
#    tryWeather = urlopen('http://api.wunderground.com/api/01b2b748b991698c/history_'+date+'/q/VA/' + city +'.json')
#    weather = tryWeather.read()
#    cleanWeather = json.loads(weather) #makes json format prettier in python
#    readyToConcat = json_normalize(cleanWeather) #pulls data into a dataframe
#    return readyToConcat #returns dataframe
#    
#toMerge = []
#
#for i in range(1,32): 
#    year = "2014"
#    month = "09"
#    if(i < 10): 
#        day= "0"+str(i)
#    else: 
#        day = str(i) 
#    toPass = ""+year+month+day
#    toMerge.append(getWeather(toPass,"Charlottesville"))
#    time.sleep(8)
#
#allAugust = pd.concat(toMerge)


#returns a month of weather
def getMonthWeather(month):
    weather = urlopen('http://www.wunderground.com/history/airport/KCHO/2014/'+ str(month) +'/1/MonthlyHistory.html?req_city=NA&req_state=NA&req_statename=NA&format=1')
    monthWeather = pd.read_csv(weather,skiprows=1)
    return monthWeather
    
#gets all weather data since March and stores dataframes in a list
weatherSinceMarch = []
for i in range(3,9): 
    thisMonth = getMonthWeather(i)
    weatherSinceMarch.append(thisMonth)

#aggregates each month's data into one large data frame
dirtyWeather = pd.concat(weatherSinceMarch)

#drops columns except the date and conditions
cleanWeather = dirtyWeather[['EDT',' Events']]

#returns a list of all dates where it rained and assigns it to a new dataframe
rainyDays = cleanWeather[cleanWeather[' Events'].fillna(" ").str.contains("Rain")]

#CSV of each day's weather
cleanWeather.to_csv("cleanweather.csv")

#CSV of rainy day's weather
cleanWeather.to_csv("rainyweather.csv")
