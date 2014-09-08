__author__ = 'danny.brady'

import json
import requests


GOOGLE_REVERSE_GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="


def ReverseGeocode(lat, long):
    url = GOOGLE_REVERSE_GEOCODE_BASE_URL + str(lat) + "," + str(long)
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    if 'results' in data:
        if len(data['results']) >= 1:
            return data['results'][0]['formatted_address']

        else:
            print "No Result found for", str(lat), ",", str(long)
    else:
        print "No Result found for", str(lat), ",", str(long)
    return None


def ReverseGeocodeCityState(lat, long):
    url = GOOGLE_REVERSE_GEOCODE_BASE_URL + str(lat) + "," + str(long)
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    if 'results' in data:
        if len(data['results']) >= 1:
            for r in data['results']:
                if  "political" in r['types']:
                    return r['formatted_address']

        else:
            print "No Result found for", str(lat), ",", str(long)
    else:
        print "No Result found for", str(lat), ",", str(long)
    return None


if __name__ == "__main__":
    print "Use ReverseGeocode function to get name at coordinates"
    print ReverseGeocode(38.029985, -78.443059)
    print ReverseGeocodeCityState(38.029985, -78.443059)