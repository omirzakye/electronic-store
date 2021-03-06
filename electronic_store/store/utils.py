# Helper functions
from django.contrib.gis.geoip2 import GeoIP2


def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, long = g.lat_lon(ip)
    return country, city, lat, long


def get_center_coordinates(latA, longA, latB=None, longB=None):
    cord = (latA, longA)
    if latB:
        cord = [(latA+latB)/2, (longA+longB)/2]
    return cord


def get_zoom(distance):
    if distance <= 100:
        return 8
    elif 100 < distance <= 5000:
        return 4
    else:
        return 2
