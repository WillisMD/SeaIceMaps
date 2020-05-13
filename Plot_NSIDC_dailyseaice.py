# -*- coding: utf-8 -*-
"""
Imports and Plots NSIDC sea ice for each day from a netCDF file
Created on Fri September 9,2016
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
#################################

#########################
####-INPUT PATHS:########
#########################
#'/Users/meganwillis/Documents/Data/NSIDC_July2014_seaice'
n_dailydata = 'NSIDC-0051_91602_daily.sub.nc'
sivar = 'Sea_Ice_Concentration_with_Final_Version'
#n_monthlydata = 'NSIDC-0051_91602.sub.nc'

####################################################
######-------- Function Definitions--------#########
####################################################

def getvar_nc(pfilex,variable): #pfilex is the path to the file, variable is a string (the name of the variable)
    # function to get variables from the WRF output file (NETCDF3_64BIT_OFFSET)
    ff = Dataset(pfilex,'r') #ff is an instance of a netCDF file object
    # if you want to check which variables are in the file, uncomment the following:
    #print ff.visititems(print) -- this prints a lot of things...
    #print(ff.variables.keys())
    #print(ff.variables['variable'])
    temp = np.array(ff[variable])
    data = temp.astype(float)#read as int, but needs to be a float
    #ff.close()
    return data #returns whatever variable as an np array


####################################################
######----------------MAIN-----------------#########
#################################################### 
#get the grid and sea ice concentrations
lat = getvar_nc(n_dailydata, 'latitude')
lon = getvar_nc(n_dailydata, 'longitude')
times = getvar_nc(n_dailydata, 'time')# this is a time in days from 1601-01-01
Ntimes = len(times)

ff = Dataset(n_dailydata, mode='r')   
for i in range(0,Ntimes):
    day = i+1
    
    seaice = np.array(ff[sivar][i,:,:])
    
    it = np.nditer(seaice, flags = ['multi_index'], op_flags = ['readwrite']) #iterate over the elements of the np.array   
    for i in it: #for each element in the iterator (it's an array, I think)
        if seaice[it.multi_index] == 251. or seaice[it.multi_index]==252. or seaice[it.multi_index]==253. or seaice[it.multi_index]==255.: #remove various flags
            seaice[it.multi_index] = 0 #set it to zero for plotting, should be nan for calculations
        elif seaice[it.multi_index] == 254.:
            seaice[it.multi_index] = 0 #set the land to zero just for plotting, should be nan for calculations
        
    seaice_norm = seaice/250  #sea ice fraction goes from 0 to 1        
    
    #define the figure
    plt.clf()
    fig = plt.plot(figsize=(10,10))
    
    #create a basemap instance
    m = Basemap(width=4000000,height=3500000, resolution='l',projection='stere',lat_0=73,lon_0=-90.)
    x,y=m(lon,lat)
    m.drawcoastlines(linewidth=0.5)
    m.drawmapboundary(fill_color = 'white')
    m.fillcontinents(color = 'lightgrey', lake_color = 'midnightblue', zorder=1) #zorder=1 puts land over the sea ice =0
    parallels = np.arange(0.,81,10.) # labels = [left,right,top,bottom]
    m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(10.,351.,20.)
    m.drawmeridians(meridians,labels=[True,False,False,True])
    levels=([0.,0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1])
    cols=cmocean.cm.ice
    norm = mcolors.BoundaryNorm(levels,ncolors=cols.N, clip=False)
    cs = m.contourf(x,y,seaice_norm, levels=levels, cmap=cols, extend='max', norm=norm)
    #cs.cmap.set_under('w') 
    cbar=plt.colorbar(cs, format="%.2f", orientation="horizontal",fraction=.06, pad=0.08)
    cbar.set_label('Sea Ice Fraction July '+str(day)+', 2014')
    
    outfile = 'SeaIceMap_'+str(day)+'July2014.png'
    plt.savefig(outfile, format="png", dpi=400)
    
ff.close()
    