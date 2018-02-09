#! /usr/bin/env python
##############################
#   Program: interact_sheba.py
#
##############################
#   Author: J. Asplet
##############################
#   A python program to act as a wrapper to sheba.
#   It read, filters, and trims SAC files from a
#   provided list of events and passes each event
#   to sheba for shear wave splitting analysis.
#   When the analysis is complete the program will
#   collect the output files for each event and it
#   will concatenate them together into a summary
#   output file!
#
##############################
#   Import Statements
##############################
#   Standard Packages - all freely available
import obspy as ob
import numpy as np
import pandas as pd
import matplotlib.pyplot as ply #Just incase
import subprocess as sub
import os.path
##############################
#   Import other scripts in Programs/
import Split_Read as sr
import Split_Measure as sm #Just in incase
import plot as sp
##############################
def main():
    """
    Main - call this function to run the interface to sheba
    """
   #First Indentify the possible station that we could have data for
   #This way we know what directory paths to look in for the sac files
    path = '/Users/ja17375/Shear_Wave_Splitting'
    statlist ='{}/Data/StationList.txt'.format(path)
    stations = pd.read_csv(statlist,delim_whitespace=True).STAT
   #Loop over all stations in the list.
    for station in stations:
        #Each station SHOULD have its own directory within Data/SAC_files
        #If the data has been downloaded. So lets look for directorys that exist
        dir_path = '{}/Data/SAC_files/{}'.format(path,station)
        if os.path.isdir(dir_path):
            #Happy Days! The data directory exists!
            with open('{}/{}_downloaded_streams.txt'.format(dir_path,station),'r') as reader: # NEW_read_stream.txt is a textfile containing filenames of streams which have been read and saved by Split_Read for this station. s
                for line in reader.readlines():
                    line.strip('\n')
                    st_id = '{}'.format(str(line[0:-1]))

                    Event = Interface(ob.read(st_id))

        else:
            print('The directory {}/Data/SAC_files/{} does not exists'.format(path,station))



class Interface:
    """
    Class which will act as the interface to sheba.
    The "subprocess" sheba will be a bound method
    """
    def __init__(self,st):
        # self.date = date
        # self.time = time
        self.BHE = st.select(channel='BHE')
        self.BHN = st.select(channel='BHN')
        self.BHZ = st.select(channel='BHZ')

    def sheba(self):
        """
        The big one! This function uses the subprocess module to host sac and then runs sheba as a SAC macro
        """

## Psuedo code plan for script
# Read Station list

# for stat in list:
    #request sac file list from data/SAC_files/stat/

    #for event in eventlist:
        #st = ob.read(event*

        #filter stream

        #trim stream to reasonable range (1400- 1600)

        #byte-swap stream
        #set headers for inclination/azimuth (call sac subprocess to do this)

        # sac m sheba
    #end loop over eventlist
#end loop over stationlist

#concatenate sheba result files together - possibly add some more metadata as well

#subroutine for stacking error surfaces
