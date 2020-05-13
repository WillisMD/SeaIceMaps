# -*- coding: utf-8 -*-
"""
Opens Bremen Sea Ice Data (HDF4) into a numpy array and plots  with basemap
Created on Fri Sep 16 2016
@author: meganwillis
"""

################################
import numpy as np                         
import matplotlib.pyplot as plt            
from matplotlib import cm   
import cmocean               
import matplotlib.colors as mcolors         
from mpl_toolkits.basemap import Basemap     
from netCDF4 import Dataset  
import scipy.ndimage 
import pandas as pd   
from pyhdf.SD import *
from pyhdf.HDF import *
import pprint
#################################

p_folder = '/Users/meganwillis/Documents/Data/UBremenSeaIce_April2015/'
n_data = 'asi-AMSR2-n6250-20150420-v5.hdf'
n_grid = 'LongitudeLatitudeGrid-n6250-Arctic.hdf'
p_data = p_folder + n_data
p_grid = p_folder + n_grid


file = SD(p_data, SDC.READ)
#print(file.info()) #print the number of datasets in the file
#datasets_dic = file.datasets()
#for idx,sds in enumerate(datasets_dic.keys()):
    #print(idx, sds)

sds_obj = file.select('ASI Ice Concentration')
pprint.pprint( sds_obj.attributes() )
icedata = sds_obj.get()
#print(data)

gridfile = SD(p_grid, SDC.READ)
lat_obj = gridfile.select('Latitudes')
lat = lat_obj.get()
lon_obj = gridfile.select('Longitudes')
lon = lon_obj.get()


#define the figure
plt.clf()
fig1 = plt.plot(figsize=(10,10))
#create a basemap instance
m = Basemap(width=5500000,height=5500000, resolution='l',projection='stere',lat_0=90,lon_0=-90.)
x,y=m(lon,lat)
m.drawcoastlines(linewidth=0.5)
m.drawmapboundary(fill_color = 'white')
m.fillcontinents(color = 'lightgrey', lake_color = 'midnightblue', zorder=1) #zorder=1 puts land over the sea ice =0
parallels = np.arange(0.,81,10.) # labels = [left,right,top,bottom]
m.drawparallels(parallels,labels=[False,True,True,False])
meridians = np.arange(10.,351.,20.)
m.drawmeridians(meridians,labels=[True,False,False,True])
levels=([0,10,20,30,40,50,60,70,80,90,100])
cols=cmocean.cm.ice
#norm = mcolors.BoundaryNorm(levels,ncolors=cols.N, clip=False)
cs = m.contourf(x,y,icedata, levels=levels, cmap=cols, extend='both')
#cs.cmap.set_under('w') 
cbar=plt.colorbar(cs, format="%.2f", orientation="horizontal",fraction=.06, pad=0.08)
cbar.set_label('Sea Ice Fraction April 20, 2015')

plt.savefig(p_folder+"SeaIceMap_April202015.png", format="png", dpi=400)
