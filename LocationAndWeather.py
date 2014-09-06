# -*- coding: utf-8 -*-
__author__ = "Danny Brady"

import pandas as pd
from datetime import timedelta
import dateutil
from math import radians, cos, sin, asin, sqrt
from collections import namedtuple


Range = namedtuple("Range", ['l', 'h'])
WalkingRange = Range(1.5, 5)
DrivingRange = Range(8, 80)

Activity = namedtuple("Activity", ['StartTime', 'EndTime', 'AvgSpeed', 'StartCoordinates', 'EndCoordinates'])


def LocationCSVtoDF(path):
    """Read in csv data converted from kml file"""
    print "Reading in file:", path, "....",
    df = pd.read_csv(path)
    df.datetime = df.datetime.apply(lambda dt: dateutil.parser.parse(dt).astimezone(dateutil.tz.tzlocal()))
    df.set_index("datetime", inplace=True)
    print "DONE"
    return df


def Haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km * 1000


def AddLocationFeatures(df):
    print "Adding location features...",
    df['time'] = df.index
    df['delta_seconds'] = (df['time']-df['time'].shift()).astype('timedelta64[s]').fillna(0)
    df.drop("time", axis=1, inplace=True)
    df['prevLong'] = (df['long'].shift())
    df['prevLat'] = (df['lat'].shift())
    df = df.dropna()
    df['distance_meters'] = df.apply(lambda r: Haversine(r.long, r.lat, r.prevLong, r.prevLat), 1)
    miles_per_meter = 0.000621371
    seconds_per_hour = 60*60
    df['mph'] = df.apply(lambda r: r['distance_meters'] * miles_per_meter / r['delta_seconds'] * seconds_per_hour, 1)
    print "DONE"
    return df


def CleanData(df):
    """Clean the data, there are strange data points"""
    print "Cleaning data...",
    df = df[df.mph <= 100]
    df = df[(df['delta_seconds'] <= 600)]
    df = df[df['delta_seconds'] > 10]
    print "DONE"
    return df


def getActivityPeriods(data, minMinutesBetween, minPeriodMinutes, speedRange):
    """
    Takes the data and tries to figure out period of time when
    an activity was taking place at a given speed range
    like walking or driving
    """
    results = []
    activity_data = data[(data.mph >= speedRange.l) & (data.mph <= speedRange.h)]
    min_minutes_between_delta = timedelta(minutes=minMinutesBetween)
    min_period_delta = timedelta(minutes=minMinutesBetween)
    period_start = period_start_coord = last_period = last_period_coord = None
    for i, row in activity_data.iterrows():
        if period_start is None:
            period_start = i
            period_start_coord = (row[['long', 'lat']])
            last_period = i
            last_period_coord = (row[['long', 'lat']])
            continue
        if i - last_period <= min_minutes_between_delta:
            last_period = i
            last_period_coord = (row[['long', 'lat']])
        else:
            if last_period - period_start >= min_period_delta:
                results.append(Activity(period_start, last_period, activity_data[period_start:last_period]['mph'].mean(),
                                        period_start_coord, last_period_coord))
            period_start = i
            period_start_coord = (row[['long', 'lat']])
            last_period = i
            last_period_coord = (row[['long', 'lat']])
            
    if last_period - period_start >= min_period_delta:
                results.append(Activity(period_start, last_period, activity_data[period_start:last_period]['mph'].mean(),
                                        period_start_coord, last_period_coord))
    
    return results


if __name__ == "__main__":
    df = LocationCSVtoDF("/users/danny/google drive/msds/data hacking/brady_location.csv")
    df = AddLocationFeatures(df)
    df = CleanData(df)
    periods = getActivityPeriods(df, 5, 5, WalkingRange)
    for p in periods:
        print "S:", p.StartTime, "F:", p.EndTime, "Avg", p.AvgSpeed
