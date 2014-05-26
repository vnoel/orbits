#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel 2014-05-26 14:40

import ephem
from datetime import timedelta, datetime
import numpy as np

tle = {'CALIPSO':('CALIPSO', '1 29108U 06016B   14145.39304519  .00000706  00000-0  16656-3 0  6708', '2 29108  98.1953  89.1090 0001617  83.5574 276.5817 14.57137717429443'),}

calipso = ephem.readtle(tle['CALIPSO'][0], tle['CALIPSO'][1], tle['CALIPSO'][2])


def calipso_position(time):
    lon, lat = [], []
    for t in time:
        calipso.compute((t.year, t.month, t.day, t.hour, t.minute, t.second))
        lon.append(calipso.sublong)
        lat.append(calipso.sublat)
    lon = np.degrees(lon)
    lat = np.degrees(lat)
    return lon, lat


def calipso_trajectory(start, end, step_seconds=0.05):
    # pour avoir un point par profil CALIPSO, il faut un point tous les 1/20e de seconde.
    # ou bien un point par seconde et multiplier par 20 ! Ca ne va pas changer grand-chose.
    tstep = timedelta(seconds=step_seconds)

    now = start
    time = []
    
    while now < end:
        time.append(now)
        now += tstep

    lon, lat = calipso_position(time)
    return lon, lat


if __name__=='__main__':
    # pour tester, on calcule l'orbite de CALIPSO entre les periodes
    start = datetime(2014,5,1,00,53,50)
    end = datetime(2014,5,1,01,40,19)
    # cf. le quicklook CALIPSO du 1er mai 2014:
    # http://www-calipso.larc.nasa.gov/data/BROWSE/production/V3-30/2014-05-01/2014-05-01_00-53-53_V3.30_thmb_map.png        
    
    lon, lat = calipso_trajectory(start, end)
    print '%d profils dans la periode' % (len(lon)), start, end
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    
    m = Basemap()
    x, y = m(lon, lat)
    m.plot(x, y)
    m.drawcoastlines()
    
    plt.show()
