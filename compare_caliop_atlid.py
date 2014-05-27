#!/usr/bin/env python
#encoding utf-8

# created by V. Noel, CNRS
# on Tue May 27 11:51:13 2014

import numpy as np
import ixion_grid
import matplotlib.pyplot as plt

if __name__=='__main__':
    
    lstep = 2.
    lonbins = np.r_[-180:180.+lstep:lstep]
    latbins = np.r_[-90:90.+lstep:lstep]

    calfile = 'CALIPSO_30days_1sec.dat'
    ecfile = 'earthCARE_30days_1sec.dat'
    
    calnprof = ixion_grid.ixion_orbit_seconds_in_grid(calfile, lonbins, latbins)
    ecnprof = ixion_grid.ixion_orbit_seconds_in_grid(ecfile, lonbins, latbins)
    
    calzonal = calnprof.sum(axis=0)
    eczonal = ecnprof.sum(axis=0)
    
    plt.figure(figsize=[7,7])
    plt.subplot(1,2,1)
    plt.plot(calzonal, latbins[:-1], label='CALIOP')
    plt.plot(eczonal, latbins[:-1], label='ATLID')
    plt.legend()
    plt.xlabel('Number of profiles')
    plt.ylabel('Latitude')
    plt.title('Over 30 days')
    
    plt.subplot(1,2,2)
    plt.plot(eczonal-calzonal, latbins[:-1])
    plt.xlabel('ATLID profiles - CALIOP profiles')
    plt.ylabel('Latitude')
    plt.title('Over 30 days')
    
    plt.subplot(1,3,3)
    plt.plot(eczonal-calzonal, latbins[:-1])
    plt.xlabel('ATLID profiles - CALIOP profiles')
    plt.ylabel('Latitude')
    plt.title('Over 30 days')
    
    plt.show()