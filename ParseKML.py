__author__ = 'Danny Brady'
import re
import pandas as pd
import dateutil


def ParseKMLStringToDataFrame(kmlString):
    last_time = None
    rows = []
    for line in kmlString.rstrip().split('\n'):
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


def ParseKMLtoDataFrame(path):
    print "Converting file to DataFrame...",
    with open(path) as f:
        lines = f.read()
        return ParseKMLStringToDataFrame(lines)
        
        
if __name__ == "__main__":
    print ParseKMLtoDataFrame("C:\\Users\\Danny\\Google Drive\\MSDS\Data Hacking\\history-08-24-2014.kml")