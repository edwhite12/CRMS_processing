# -*- coding: cp1252 -*-
print ('\n\nsetting things up...')

import os
import numpy as np
import os
import sys
import datetime as dt
import CRMS_stats
from builtins import Exception

################################################################
####                    SET THE SETTINGS                    ####
################################################################

yr_start = 2006
yr_end = 2024

topdir = 'E:/CRMS_%04d-%04d' % (yr_start,yr_end)
masterCRMS = '%s/Full_Continuous_Hydrographic_20250117.csv' % topdir
masterCRMSlist = '%s/CRMS_sites.csv' % topdir
geoidfile = '%s/Hydro Shift from 99-12B.csv' % topdir  # '%s/CRMS_GEOID99_TO_GEOID12A.csv' % topdir
survey_subsidence_file = '%s/CRMS_survey_dates_subsidence_rates.csv' % topdir
sub_conv = 0.001/0.3048 # subsidence rates are provided in mm/yr - hourly output files with corrected subsidence need to be in feet

split_files = 'no'          # split_files is a flag to separate the master CRMS bulk download file into individual files for each site; if set to 'no' the split files must already exist; 
build_files = 'yes'          # build_files is a flag to build new daily and hourly data from the raw split files; if set to 'no' the split daily and hourly clean files must already exist and the stats will be generated from those files

sites = np.genfromtxt(masterCRMSlist,dtype='str')


################################################################################################
####                    SETUP FOLDER DIRECTORIES FOR PROCESSED CRMS DATA                    ####
################################################################################################
if split_files == 'yes':
    folds = ['raw','clean_hourly','clean_daily','stats']

    for fol in folds:
        if os.path.exists(r'%s\%s' % (topdir,fol)) == True:
            print('\n\n\n\noutput directory \%s already exists in %s !!!!' % (fol,topdir))
            print(' \n\ndo you want to....\n(a) continue with that folder and re-write old files \n(b) rename folder here \n(c) quit program and handle yourself? ')
            warn = input('pick one: <  a    b    c  >')
            if warn == 'a':
                print('\nyou chose to continue.  \n(a) you sure? \n(b) or would you prefer to rename the folder \n(c) or just quit, already?')
                warn = str(input('pick one: <  a    b    c  >'))
    
            if warn == 'c':
                print('\nsee ya later.')
                sys.exit()
            elif warn == 'b':
                apptext = str(input('what word would you like to append to the folder name? please reply within quotes (e.g. "old").'))
                old = r'%s\%s' % (topdir,fol)
                new = r'%s\%s_%s' % (topdir,fol,apptext)
                print('\n renaming %s to %s' % (old, new))
                os.rename(old,new)
                os.mkdir(r'%s\%s' % (topdir,fol))
            elif warn == 'a':
                print('\nOK this will overwrite any old data...continuing on.')
        else:
            os.mkdir(r'%s\%s' % (topdir,fol))
    

################################################################################################
####                    SPLIT BULK DOWNLOAD TABLE INTO INDIVIDUAL FILES                     ####
################################################################################################

# The below script parses the bulk data download into individual files - it requires that the file is structured such that the data for each CRMS site is lumped (vertically together)
if split_files == 'yes':
    print('splitting master CRMS file by site ID')

#    data_by_site = {}
#    for s in sites:
#        data_by_site[s] = []

    with open(masterCRMS,mode='rt') as inf:
        nline = 0
        old_site = 'old'
        current_site = 'current'
        data_by_site = []
        for line in inf:
            if nline == 0:
                hdr = line
            else:
                current_site = line.split(',')[0]

                if current_site != old_site:
                    # if on to a new site, must first print out old site data to new file
                    print(' - writing individual CRMS file for %s' % old_site)
                    rawpath = r'%s\raw\%s_raw.csv' % (topdir,old_site)
                    with open(rawpath, mode='w') as splitfile:
                        splitfile.write(hdr)
                        for val in data_by_site:
                            splitfile.write(val)

                    # once old data is written, re-initialize data for new site
                    print('processing new site: %s' % current_site)
                    data_by_site = []

                else:   # still on current site 
                    try:
                        data_by_site.append(line)
                    except Exception as e:
                        print(e)
                    
            old_site = current_site
            nline += 1

#    print('writing individual CRMS files')
#
#    for site in sites:
#        print('   - site %s' % site)
#        rawpath = r'%s\raw\%s_raw.csv' % (topdir,site)
#        with open(rawpath, mode='w') as splitfile:
#            splitfile.write(hdr)
#            for val in data_by_site[site]:
#                splitfile.write(val)

    print('done splitting CRMS data by site\n')
else:
    print('using pre-split CRMS files saved in \raw folder')

    

################################################################################################
####              READ IN SUBSIDENCE RATES AND SURVEY DATES FOR EACH CRMS SITE              ####
################################################################################################
if build_files == 'yes':
    print('reading in subsidence rates and survey dates')
    survey_sub_rates = np.genfromtxt(survey_subsidence_file,dtype='str',delimiter=',',skip_header=1)
    survey_dates = {}
    subsidence_rates = {}
    for r in survey_sub_rates:
        site = r[0]
        dstr = r[1].split('-')
        subrate = r[2]
        survdate = dt.date(int(dstr[0]),int(dstr[1]),int(dstr[2]))
        survey_dates[site] = survdate
        subsidence_rates[site] = float(subrate)

################################################################################################
####                   READ IN GEOID CONVERSION FACTORS FOR EACH CRMS SITE                 ####
################################################################################################
if build_files == 'yes':
    print('reading in geoid conversions')
    gc = {}
    with open(geoidfile,mode='rt') as gf:
        for line in gf:
            if line[0:4] == 'CRMS':
                gc[line.split(',')[0]] = float(line.split(',')[1])

########################################################################################################
####    STEP THROUGH CRMS SITES AND PROCESS RAW DATA THEN SAVE INTO CLEAN HOURLY AND DAILY FILES    ####
########################################################################################################
ns = 0    
for site in sites:
    ns += 1
    print('Processing site %03d/%03d  - %s' %(ns,len(sites),site) )
    
    crmssite = site.split('-')[0]
    
    rawpath = r'%s\raw\%s_raw.csv' % (topdir,site)
    hrpath = r'%s\clean_hourly\%s_hourly_English.csv' % (topdir,site)
    daypath = r'%s\clean_daily\%s_daily_English.csv' % (topdir,site)

    ########################################################################
    ####    PROCESS HOURLY DATA AND SAVE 'CLEAN' HOURLY OUTPUT FILE     ####
    ########################################################################

    if build_files == 'yes':
        print('  - building new clean hourly output file')

        try:
            sub = subsidence_rates[crmssite]
            survey_date = survey_dates[crmssite]
            note = '     - %s site was surveyed on %04d-%02d-%02d\n     - using subsidence rate of %0.2f mm/yr.' % (site,survey_date.year,survey_date.month,survey_date.day,sub)
            sbf = 'c'
        except:
            sub = 0.0
            survey_date = dt.date(yr_start,1,1)
            note = '     - %s site does not have survey data\n     - no subsidence correction applied.' % site
            sbf = ''
            
        print(note)

        with open(rawpath,mode='rt') as rawdata:
            with open(hrpath,mode='wt') as cleanhour:

                clean_hourly_header = r'stationID,Date_mm/dd/yyyy,time_hh:mm:ss,timezone,salinity_ppt,salinity_flag(r=raw a=adjusted na=nodata),stage_ft_NAVD88_12B,stage_flag(r=raw data used/no adjustments made; a=adjusted; s=datum shifted to geoid12b from 99; c= subsidence corrected based; nd=used Geoid99 but no datum conversion found for site; na=nodata)'
                
                cleanhour.write('%s\n' % clean_hourly_header)
                nr = 0
                for allrow in rawdata:
                    if nr > 0:
                        row = allrow.split(',')
                        sid,d,t,tz,dat = row[0],row[1],row[2],row[3],row[19]
                        
                        ##########################################################################################
                        ####    DETERMINE SUBSIDENCE OFFSET BASED ON SUBSIDENCE RATE AND TIME SINCE SURVEY    ####
                        ##########################################################################################
                        # subsidence offset sign convention: 
                        #       this sub_offset value should be subtracted from raw data to reduce water surface 
                        #       elevation if data is from after survey (e.g., gage has subsided and reading is
                        #       higher than reality due to sunken gage) and to increase water surface elevation 
                        #       if data is from before survey. The survey_date will be the time where the raw water
                        #       surface elevation is assumed to be accurately tied into the survey/geoid conversion
                        #       and sub_offset=0 when dtdate=survey_date
                        
                        dtdate = dt.date(int(d.split('/')[2]),int(d.split('/')[0]),int(d.split('/')[1]))        # this format requires the DATE column in CRMS raw data files to be of the format M/D/YYYY
                        sub_offset = sub_conv*sub*(dtdate - survey_date).days/365.25            
                        
                        
                        ##############################################################
                        ####    DETERMINE GEOID DATUM CONVERSION FACTOR TO USE    ####
                        ##############################################################
                        if dat == 'GEOID99':
                                try:
                                    datc = gc[sid]
                                    dcf = 's'
                                except:
                                    try:
                                        datc = gc[sid.split('-')[0]]
                                        dcf = 's'
                                    except:
                                        datc = 0.0
                                        dcf = 'nd'
                        else:
                                datc = 0.0
                                dcf = ''
                        
                        #########################################################
                        ####    PROCESS HOURLY DATA AND APPLY CONVERSIONS    ####
                        #########################################################
                        if row[10] != '': # try for adjusted salinity
                            sal = row[10]
                            sal_f = 'a'
                        #elif row[9] != '': # if no adjusted salinity - use raw - COMMENTED OUT - DO NOT WANT TO USE RAW DATA AT ALL, ALWAYS USE ADJUSTED (per LAS)
                        #    sal = row[9]
                        #    sal_f = 'r'
                        else:
                            sal = 'na'
                            sal_f = 'na'
                        try:
                            if float(sal) < 0.0:    # check for negative salinity values and set to na
                                sal = 'na'
                        except:
                            sal = 'na'
                        if row[16] != '':
                            stg_c = float(row[16]) + datc - sub_offset # try for adjusted stage and add datum and subsidence conversion factors
                            stg_f = 'a %s %s' % (dcf,sbf)
                        elif row[15] != '':
                            stg_c = float(row[15]) + datc - sub_offset # if no adjusted stage - use raw stage and add datum and subsidence conversion factors
                            stg_f = 'r %s %s' % (dcf,sbf)
                        else:
                            stg_c = 'na'
                            stg_f ='na'

                        writerow = '%s,%s,%s,%s,%s,%s,%s,%s\n' % (sid,d,t,tz,sal,sal_f,stg_c,stg_f)
                        cleanhour.write(writerow)
                    nr += 1

        ##########################################################################
        ####    PREPARE DAILY OUTPUT FILE FROM 'CLEAN' HOURLY OUTPUT FILE     ####
        ##########################################################################
    
        print('  - building new daily summary output file')
        with open(hrpath,mode='rt') as cleanhour:
            sal = {}
            salorder = {}
            stg = {}
            stgorder = {}
            nr = 0
            for allrow in cleanhour:
                if nr > 0:
                    row = allrow.split(',')
                    sid,d,t,tz,salh,stgh = row[0],row[1],row[2],row[3],row[4],row[6]

                # add date as a key to stage and salinity dictionaries
                    if d not in sal.keys():
                        ndaysal = len(sal.keys())
                        sal[d] = []
                        salorder[ndaysal+1] = d
                    if d not in stg.keys():
                        ndaystg = len(stg.keys())
                        stg[d] = []
                        stgorder[ndaystg+1] = d

                # append salinity and stage to daily value arrays
                    if salh != 'na':
                        sal[d].append(float(salh))
                    if stgh != 'na':
                        stg[d].append(float(stgh))
                        
                nr += 1

        with open(daypath,mode='wt') as sumdaily:
            daily_header = r'stationID,Date_mm/dd/yyyy,mean_salinity_ppt,median_salinity_ppt,min_salinity_ppt,max_salinity_ppt,stdev_salinity_ppt,ncount_salinity,mean_stage_ftNAVD88,median_stage_ftNAVD88,min_stage_ftNAVD88,max_stage_ftNAVD88,stdev_stage_ftNAVD88,ncount_stage_ftNAVD88'
            sumdaily.write('%s\n' % daily_header)
                
            for nday in stgorder.keys():
                d = stgorder[nday]
                if len(sal[d]) > 0:
                    salstring = '%0.1f,%0.1f,%0.1f,%0.1f,%0.1f,%d' % (np.mean(sal[d]),np.median(sal[d]),np.min(sal[d]),np.max(sal[d]),np.std(sal[d]),len(sal[d]))
                else:
                    salstring = 'na,na,na,na,na,0'

                if len(stg[d]) > 0:
                    stgstring = '%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%d' % (np.mean(stg[d]),np.median(stg[d]),np.min(stg[d]),np.max(stg[d]),np.std(stg[d]),len(stg[d]))
                else:
                    stgstring = 'na,na,na,na,na,0'

                sumdaily.write('%s,%s,%s,%s\n' % (site,d,salstring,stgstring))
    else:
        print('using existing clean hourly and daily files to perform stats calculations')


    ##################################################
    ####    CALCULATE STATISTICS FOR CRMS SITE    ####
    ##################################################

    if ns == 1:
        write_hdr = 'True'
    else:
        write_hdr = 'False'
    print('  - calculating stage summary statistics')
    CRMS_stats.CRMS_hydro_stats(site,yr_start,yr_end,'stage_ft_NAVD88-g12b',topdir,write_hdr)
    print('  - calculating salinity summary statistics')
    CRMS_stats.CRMS_hydro_stats(site,yr_start,yr_end,'salinity_ppt',topdir,write_hdr)
    print('  - calculating moving window salinity summary statistics')
    CRMS_stats.CRMS_moving_window(site,yr_start,yr_end,'salinity_ppt',topdir,write_hdr)   

