#!/usr/bin/env python

import pyproj


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
