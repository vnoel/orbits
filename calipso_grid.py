#!/usr/bin/env python
#encoding:utf-8

# Created by VNoel 2014-05-26 15:22

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from calipso_orbit import calipso_trajectory
from mpl_toolkits.basemap import Basemap

lbin = 2.
lonbins = np.r_[-180.:180:lbin]
latbins = np.r_[-90:90:lbin]

start = datetime(2014,1,1)
end = datetime(2014,3,31)

now = start
total_histo = None
while now < end:
    
    endperiod = now + timedelta(days=2)
    lon, lat = calipso_trajectory(now, endperiod, step_seconds=1.)
    print 'between ', now, ' and ', endperiod, ': %d profiles' % (len(lon)*20.)
    this_histo, xx, yy = np.histogram2d(lon, lat, (lonbins, latbins))
    if total_histo is None:
        total_histo = this_histo
    else:
        total_histo += this_histo
    now = endperiod

total_histo *= 20.

plt.figure(figsize=[12,5])
m = Basemap()
x, y = m(lonbins, latbins)
m.pcolormesh(x, y, total_histo.T)
m.drawcoastlines()
cb = plt.colorbar()
cb.set_label('# of profiles')
plt.title('CALIPSO from ' + str(start) + ' to ' + str(end))
plt.show()

plt.savefig('calipso_orbit_201401_201403.png')