#!/usr/bin/env python

import pyproj
import math

def degminsec_to_decimal(dms):
    (degrees, minutes, seconds) = dms
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

# WGS84 datum, used by Google Earth
wgs84 = pyproj.Proj("+init=EPSG:4326")

# AFAICT, this is the right datum/projection to use for Soviet maps in the K-44
# region, covering eastern Kyrgyzstan.
# From http://spatialreference.org/ref/epsg/2542/
# Pulkovo 1942 / 3-degree Gauss-Kruger zone 26
#
# WGS84 Bounds: 76.5000, 40.1000, 79.5000, 74.0000
# Projected Bounds: 26372091.6014, 4441789.7211, 26627908.3986, 8216047.4610
# Scope: Large scale topographic mapping, cadastral and engineering survey.
# Last Revised: June 22, 2002
# Area: Asia - FSU - 76.5E to 79.5E
pulkovo  = pyproj.Proj("+init=EPSG:2542")

# From http://spatialreference.org/ref/sr-org/7809/proj4/
sk42 = pyproj.Proj("+proj=tmerc +lat_0=0 +lon_0=135 +k=1 +x_0=500000 +y_0=0 +ellps=krass +towgs84=24.0,-123.0,-94.0,0.02,-0.25,-0.13,1.1 +units=m +no_defs")

objectives = [
        ("Objective A", (42, 5, 54), (78, 53, 47.83), wgs84),
        ("Objective B", (42, 5, 23.92), (78, 52, 44.85), wgs84),
        ("Objective C", (42, 7, 2.34), (78, 54, 44.85), wgs84),
        ("Objective D", (42, 6, 58.28), (78, 52, 37.21), wgs84),
        ("Centre point of map", (42, 5, 0), (78, 52, 30), sk42),
    ]

# Definition of the easting from https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D1%80%D0%B0%D0%B7%D0%B3%D1%80%D0%B0%D1%84%D0%BA%D0%B8_%D0%B8_%D0%BD%D0%BE%D0%BC%D0%B5%D0%BD%D0%BA%D0%BB%D0%B0%D1%82%D1%83%D1%80%D1%8B_%D1%82%D0%BE%D0%BF%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D0%BA%D0%B0%D1%80%D1%82#.D0.9F.D1.80.D1.8F.D0.BC.D0.BE.D1.83.D0.B3.D0.BE.D0.BB.D1.8C.D0.BD.D0.B0.D1.8F_.28.D0.BA.D0.B8.D0.BB.D0.BE.D0.BC.D0.B5.D1.82.D1.80.D0.BE.D0.B2.D0.B0.D1.8F.29_.D1.81.D0.B5.D1.82.D0.BA.D0.B0_.D0.BA.D0.BE.D0.BE.D1.80.D0.B4.D0.B8.D0.BD.D0.B0.D1.82
# 1. The first one or two digits is the number of the zone.
#    In our case this will be 44 because our map is K-44-062-Г
# 2. The rest is the number of meters relative to the central meridian of the zone. 500,000 is the central meridian
#    with west of that being higher numbers and east of that being lower numbers
#    K44 runs from 78 degrees to 84 degrees (http://maps.vlasenko.net/smtm1000/k-44.jpg)
#    So the central meridian is 81 degrees.
#    This seems to match with checking maps with grid numbers and not just lat/lng.
#    e.g. http://maps.vlasenko.net/smtm500/k-44-1.jpg
#    This shows 81 degrees exactly lying on easting 14500. Which doesn't really match exactly with
#    what I'd expect but it does finish with 00.
#
#    Have no idea if "distance" here means great circle distance or distance travelling parallel
#    to the equator although I'd guess the latter
def distance_along_latitude(lat,lng1,lng2):
    DEGREE_LENGTH_AT_EQUATOR=111321 #111.321 km
    return (lng1-lng2)*DEGREE_LENGTH_AT_EQUATOR*math.cos(lat*math.pi/180)


for (name, lat_triple, lon_triple, projection) in objectives:
    lat = degminsec_to_decimal(lat_triple)
    lon = degminsec_to_decimal(lon_triple)
    newlon, newlat = pyproj.transform(projection, pulkovo, lon, lat)
    # Longitudes are m from *somewhere*; convert to km
    grid_x = newlon / 1000
    # Latitudes are m from the equator.
    # Scale and strip leading digits to get map y-coordinates.
    grid_y = (newlat / 1000) % 100
    print name
    print "%s N %s E" % (lat, lon)
    print grid_x, grid_y
    print
