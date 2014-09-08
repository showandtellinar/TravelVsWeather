__author__ = 'Danny Brady'
import re
import pandas as pd
import dateutil


def ParseKMLtoDataFrame(path):
    print "Converting file to DataFrame...",
    last_time = None
    rows = []
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            dt_m = re.match(r"<when>(?P<datetime>.*?)</when>", line)
            if dt_m is not None:
                last_time = dt_m.group("datetime")
                continue
            coor_m = re.match(r"<gx:coord>(?P<long>.*?) (?P<lat>.*?) .*</gx:coord>", line)
            if coor_m is not None:
                rows.append({"datetime" : last_time, "long" : float(coor_m.group("long")), "lat" : float(coor_m.group("lat"))})
                continue
    df = pd.DataFrame(rows)
    df.datetime = df.datetime.apply(lambda dt: dateutil.parser.parse(dt).astimezone(dateutil.tz.tzlocal()))
    df.set_index("datetime", inplace=True)
    print "Done"
    return df