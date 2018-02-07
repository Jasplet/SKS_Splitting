#! /usr/bin/env python
### Script containing varous plotting functions for splitting Measurements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as cart
import cartopy
import matplotlib.gridspec as gridspec
import obspy


def load(stat,phase):

    data = pd.read_csv('/Users/ja17375/Python/Shear_Wave_Splitting/Measurements/{}_{}_Splitting.txt'.format(stat,phase),delim_whitespace=True)
    a = data['FAST']
    d = data.index[np.isnan(data['FAST']) == True].tolist() # Find any rows which contain NaNs
    data = data.drop(d)
    data = data[(data.QUAL != 'x')]

    stat_loc = data.STLA[0],data.STLO[0] # sta and stlo are the same for all events (same station). In future maybe read this data in from Station list?)


    #Parse events by whether they are 'null' or 'split'
    null = (data[(data.QUAL == 'n')].BAZ,data[(data.QUAL == 'n')].FAST,data[(data.QUAL == 'n')].DFAST,data[(data.QUAL == 'n')].TLAG,data[(data.QUAL == 'n')].DTLAG,data[(data.QUAL == 'n')].EVLA,data[(data.QUAL == 'n')].EVLO)
    split =(data[(data.QUAL != 'n')].BAZ,data[(data.QUAL != 'n')].FAST,data[(data.QUAL != 'n')].DFAST,data[(data.QUAL != 'n')].TLAG,data[(data.QUAL != 'n')].DTLAG,data[(data.QUAL != 'n')].EVLA,data[(data.QUAL != 'n')].EVLO)
    return data,stat_loc,null,split # also return data so not to break SKS_plot

def SKS_plot(stat,title1,phase='SKS'):
    """
    Function to make diagnostice plots for a given file of splitting measuremtns
    """
    stat_loc, = load(stat,phase)

    fig,axs = plt.subplots(2, 2,sharex='col',figsize=(10,10))


    axs[0,0].errorbar(null[0],null[1],yerr=null[2],fmt='kx',elinewidth=0.5,label='Null')
    axs[0,0].errorbar(split[0].split[1],yerr=split[2],fmt='ko',elinewidth=0.5,label='Split')
    axs[0,0].legend(loc=2)

    axs[0,0].set_ylabel('Fast Direction (deg)')
    axs[0,0].set_ylim([-90,90])
    axs[0,0].set_yticks(np.arange(-90,91,30))
    axs[0,0].set_title('{} - Fast Direction'.format(title1))

    axs[0,1].errorbar(data[(data.QUAL == 'n')].BAZ,data[(data.QUAL == 'n')].WL_FAST,yerr=data[(data.QUAL == 'n')].WL_DFAST,fmt='kx',elinewidth=0.5)
    axs[0,1].errorbar(data[(data.QUAL != 'n')].BAZ,data[(data.QUAL != 'n')].WL_FAST,yerr=data[(data.QUAL != 'n')].WL_DFAST,fmt='ko',elinewidth=0.5)
    axs[0,1].set_ylim([-90,90])
    axs[0,1].set_yticks(np.arange(-90,91,30))
    axs[0,1].set_title('Jacks(Sheba) - Fast Direction')
    axs[0,1].set_xlabel('Back Azimuth')
    axs[0,1].set_ylabel('Fast Direction (deg)')

    plot_lag(axs[1,0],null[0],null[3],null[4],fmt='kx')
    plot_lag(axs[1,0],split[0],split[3],split[4],fmt='ko')
    # axs[1,0].set_ylabel('Tlag (s)')
    # axs[1,0].set_ylim([0,4])
    # axs[1,0].set_title('{} - Lag Time'.format(title1))

    axs[1,1].errorbar(data[(data.QUAL == 'n')].BAZ,data[(data.QUAL == 'n')].WL_TLAG,yerr=data[(data.QUAL == 'n')].WL_DTLAG,fmt='kx',elinewidth=0.5)
    axs[1,1].errorbar(data[(data.QUAL != 'n')].BAZ,data[(data.QUAL != 'n')].WL_TLAG,yerr=data[(data.QUAL != 'n')].WL_DTLAG,fmt='ko',elinewidth=0.5)
    axs[1,1].set_ylim([0,4])
    axs[1,1].set_ylabel('Tlag (s)')
    axs[1,1].set_xlabel('Back Azimuth')
    axs[1,1].set_title('Jacks(Sheba) - Lag Time')

    plt.tight_layout()
    plt.show()



def SKKS_plot(stat,phase):
    """
    Creates a 3 panel plot showing measured fast direction and lag time vs back azimuth at a given station along with the coverage of the events
    stat - station Code [STRING]
    phase - phase to plot [STRING]
    """
    data = load(stat,phase)

    fig = plt.figure(figsize = [20,20])
    axs = []
    gs = gridspec.GridSpec(2,3)
    proj = cart.AzimuthalEquidistant(central_longitude=data.STLO[0],central_latitude=data.STLA[0])


    ax1 = plt.subplot(gs[0,0])
    ax2 = plt.subplot(gs[1,0])
    ax3 = fig.add_subplot(gs[:,1:],projection = proj)

    ax1.errorbar(data.BAZ,data.TLAG,yerr = data.DTLAG,fmt='kx',elinewidth=0.5)
    ax1.set_ylim([0,4])
    ax1.set_ylabel('Lag (s)')
    ax1.set_xlabel('Back Azimuth (deg)')
    # _lag(ax1,data.BAZ,data.TLAG,data.DTLAG,'kx')
    # _fast(ax2,data.BAZ,data.FAST,data.DFAST,'kx')
    # coverage(ax3,data.EVLA,data.EVLO,data.STLA[0],data.STLO[0],stat)
    # plt.show()
    ax2.errorbar(data.BAZ,data.FAST,yerr=data.DFAST,fmt='kx',elinewidth=0.5)
    ax2.set_ylim([-90,90])
    ax2.set_ylabel('Fast Direction (s)')
    ax2.set_xlabel('Back Azimuth (deg)')
    ### Plot Coverage on third axis object

    ax3.set_global() #This sets the axes extent to its maximum possible setting, so we can find these darn events
    ax3.coastlines(resolution = '110m') # Coastline data is downloaded by Cartopy from Natural Earth (http://www.naturalearthdata.com)
    #Resolution options are 100m,50m and 10m
    ax3.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax3.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
    # Now add observed events
    ax3.plot(data.EVLO,data.EVLA,'ro',markersize = 5,transform = cart.Geodetic(),label='Event Location')
    # ax.set_xticks([-130,-125,-120,-115,-110,-105,-100], crs=proj)
    # ax.set_yticks([30,35,40,45,50,55,60], crs=proj)
    ax3.plot(data.STLO,data.STLA,'kv',transform=cart.Geodetic(),markersize=10,label='Station Loction')
    ax3.set_title('{} coverage for Station {}'.format(phase,stat))
    ax3.legend()
    plt.show()

def SKS_SKKS_plot(stat):
    """
    Creates a 3 panel plot showing measured fast direction and lag time vs back azimuth at a given station along with the coverage of the events
    for BOTH SKS  and SKKS
    stat - station Code [STRING]
    phase - phase to plot [STRING]
    """
    SKS_data = load(stat,phase='SKS')
    SKKS_data = load(stat,phase='SKKS')

    fig = plt.figure(figsize = [20,20])
    axs = []
    gs = gridspec.GridSpec(2,3) # Creates a 2x3 grid in the figure space for plotting in
    proj = cart.AzimuthalEquidistant(central_longitude=SKKS_data.STLO[0],central_latitude=SKKS_data.STLA[0])


    ax1 = plt.subplot(gs[0,0])
    ax2 = plt.subplot(gs[1,0])
    ax3 = fig.add_subplot(gs[:,1:],projection = proj) # have to use add_subplots in order to add a different projection

    ax1.errorbar(SKS_data.BAZ,SKS_data.TLAG,yerr = SKS_data.DTLAG,fmt='rx',elinewidth=0.5,label='SKS')
    ax1.errorbar(SKKS_data.BAZ,SKKS_data.TLAG,yerr=SKKS_data.DTLAG,fmt = 'bo',elinewidth=0.5,label='SKKS')
    ax1.set_ylim([0,4])
    ax1.set_ylabel('Lag (s)')
    ax1.set_xlabel('Back Azimuth (deg)')
    ax1.legend()
    # _lag(ax1,data.BAZ,data.TLAG,data.DTLAG,'kx')
    # _fast(ax2,data.BAZ,data.FAST,data.DFAST,'kx')
    # coverage(ax3,data.EVLA,data.EVLO,data.STLA[0],data.STLO[0],stat)
    # plt.show()
    ax2.errorbar(SKS_data.BAZ,SKS_data.FAST,yerr = SKS_data.DFAST,fmt='rx',elinewidth=0.5,label='SKS')
    ax2.errorbar(SKKS_data.BAZ,SKKS_data.FAST,yerr=SKKS_data.DFAST,fmt = 'bo',elinewidth=0.5,label='SKKS')
    ax2.set_ylim([-90,90])
    ax2.set_ylabel('Fast Direction (s)')
    ax2.set_xlabel('Back Azimuth (deg)')
    ### Plot Coverage on third axis object
    #ax3.set_extent([-180,180,-60,90])
    ax3.set_global() #This sets the axes extent to its maximum possible setting, so we can find these darn events
    ax3.coastlines(resolution = '110m') # Coastline data is downloaded by Cartopy from Natural Earth (http://www.naturalearthdata.com)
    #Resolution options are 100m,50m and 10m
    ax3.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax3.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
    # Now add observed events
    ax3.plot(SKS_data.EVLO,SKS_data.EVLA,'ro',markersize = 5,transform = cart.Geodetic(),label='Event Locations (SKS)')
    ax3.plot(SKKS_data.EVLO,SKKS_data.EVLA,'bx',markersize = 5,transform = cart.Geodetic(),label='Event Locations (SKKS)')
    # ax.set_xticks([-130,-125,-120,-115,-110,-105,-100], crs=proj)
    # ax.set_yticks([30,35,40,45,50,55,60], crs=proj)
    ax3.plot(SKS_data.STLO,SKS_data.STLA,'kv',transform=cart.Geodetic(),markersize=10,label='Station {}'.format(stat))
    ax3.set_title('SKS/SKKS coverage for Station {}'.format(stat))
    ax3.legend()
    plt.show()

def plot_lag(ax,baz,lag1,dlag1,fmt):

    ax.errorbar(baz,lag1,yerr=dlag1,fmt=fmt,elinewidth=0.5)

    ax.set_ylim([0,4])
    ax.set_ylabel('Lag (s)')
    ax.set_xlabel('Back Azimuth (deg)')

def plot_fast(ax,baz,fast1,dfast1,fmt):

    ax.errorbar(baz,fast1,yerr=dfast1,fmt = fmt,elinewidth=0.5)
    ax.set_ylim([-90,90])
    ax.set_ylabel('Fast Direction (s)')
    ax.set_xlabel('Back Azimuth (deg)')

def coverage(evla,evlo,stla,stlo,stat):
    """
    Creates a map showing the locations of a seismic station and the associated events using a AzimuthalEquidistant projection centered on the Station
    evla - event longitude(s) [deg] can be 1 or more
    evlo - event latitude(s) [deg] can be 1 or more
    stla - station latitude [deg]
    stlo - station longitude [deg]
    stat - Station Code (string)
    """
    # We can either do and AzimuthalEquidistant projection centered on the staiton or a nice, Pacific-centered one
    # proj = cart.PlateCarree(central_longitude=180)
    proj = cart.AzimuthalEquidistant(central_longitude=stlo,central_latitude=stla)
    ax = plt.axes(projection=proj)
    ax.set_global() #This sets the axes extent to its maximum possible setting, so we can find these darn events

    ax.coastlines(resolution = '110m') # Coastline data is downloaded by Cartopy from Natural Earth (http://www.naturalearthdata.com)
    #Resolution options are 100m,50m and 10m

    ax.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')

    # Now add observed events
    ax.plot(evlo,evla,'ro',markersize = 5,transform = cart.Geodetic(),label='Event Location')

    # ax.set_xticks([-130,-125,-120,-115,-110,-105,-100], crs=proj)
    # ax.set_yticks([30,35,40,45,50,55,60], crs=proj)
    stat = 'NEW'
    ax.plot(stlo,stla,'kv',transform=cart.Geodetic(),markersize=10,label='Station Loction')
    ax.set_title('Coverage for Station {}'.format(stat))
    ax.legend()
    plt.show()
