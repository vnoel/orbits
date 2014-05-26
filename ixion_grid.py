#!/usr/bin/env python
#encoding:utf-8

import matplotlib.pyplot as plt
import numpy as np

lstep = 2.
lonbins = np.r_[-180:180.+lstep:lstep]
latbins = np.r_[-90:90.+lstep:lstep]


def read_ixion(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    # skip header
    lines = lines[57:]
    lon, lat = [], []
    for line in lines[:-6]:
        items = line.split()
        time_hms = items[3]
        lon.append(float(items[6]))
        lat.append(float(items[9]))
    return lon, lat


if __name__=='__main__':

    ixion_file = 'earthCARE_30days_1sec.dat'
    print 'Reading ', ixion_file
    profiles_per_points = 20.
    
    lon, lat = read_ixion(ixion_file)

    print 'Read %d profiles' % (len(lon))

    h, xx, yy = np.histogram2d(lon, lat, (lonbins, latbins))
    h *= profiles_per_points

    from mpl_toolkits.basemap import Basemap    
    
    m = Basemap()
    x, y = m(lonbins, latbins)

    plt.figure(figsize=[14,6])
    m.pcolormesh(x, y, h.T)
    m.drawcoastlines()
    cb = plt.colorbar()
    cb.set_label('# of profiles')
    
    plt.title(ixion_file + ' in %dx%d grid' % (lstep))
    plt.savefig(ixion_file[:-4] + '.png')
    
    plt.show()