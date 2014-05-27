#!/usr/bin/env python
#encoding:utf-8

import matplotlib.pyplot as plt
import numpy as np

def read_ixion(filename):

    nheader = {'CALIPSO':77, 'earthCARE':57}
    ilons = {'earthCARE':6, 'CALIPSO':5}
    ilats = {'earthCARE':9, 'CALIPSO':8}

    f = open(filename, 'r')
    lines = f.readlines()
    
    # skip header
    satellite = filename.split('_')[0]
    lines = lines[nheader[satellite]:]
    ilon = ilons[satellite]
    ilat = ilats[satellite]
    
    lon, lat = [], []
    for line in lines[:-6]:
        items = line.split()
        time_hms = items[3]
        lon.append(float(items[ilon]))
        lat.append(float(items[ilat]))
    return lon, lat


def ixion_orbit_seconds_in_grid(ixion_filename, lonbins, latbins):
    
    lon, lat = read_ixion(ixion_filename)
    print ixion_filename + ' - Read %d coordinates' % (len(lon))
    h, xx, yy = np.histogram2d(lon, lat, (lonbins, latbins))
    return h


if __name__=='__main__':

    lstep = 2.
    lonbins = np.r_[-180:180.+lstep:lstep]
    latbins = np.r_[-90:90.+lstep:lstep]

    ixion_file = 'earthCARE_30days_1sec.dat'
    h = ixion_orbit_seconds_in_grid(ixion_file, lonbins, latbins)
    h *= 25.

    from mpl_toolkits.basemap import Basemap    
    
    m = Basemap()
    x, y = m(lonbins, latbins)

    plt.figure(figsize=[14,6])
    m.pcolormesh(x, y, h.T)
    m.drawcoastlines()
    cb = plt.colorbar()
    cb.set_label('# of profiles')
    plt.clim(0,8000)
    plt.title(ixion_file + ' in %dx%d grid' % (lstep, lstep))
    plt.savefig(ixion_file[:-4] + '_grid.png')
    
    plt.figure(figsize=[8,14])
    plt.plot(np.sum(h, axis=0), latbins[:-1])
    plt.grid()
    plt.ylabel('Latitude')
    plt.xlabel('Number of profiles')
    plt.title(ixion_file + ' in %dx%d grid' % (lstep, lstep))
    plt.savefig(ixion_file[:-4] + '_zonal.png')
    
    plt.show()