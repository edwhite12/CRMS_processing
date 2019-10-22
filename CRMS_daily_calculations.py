##########################################################################################################################
###  python script that loops through CRMS sites and calculates daily values from summary files e.g. tidal range       ###
###  functions for specific calculations are at the top and the looping over CRMS sites is at the bottom of this file  ###
##########################################################################################################################

def CRMS_hydro_daily_tidal_range(site, start_year, end_year, obs_type, topdir, write_hdr):
    import numpy as np
    daypath = r'%s\clean_daily\%s_daily_English.csv' % (topdir,site)
    hourpath = r'%s\clean_hourly\%s_hourly_English.csv' % (topdir,site)

    dom = {}
    dom[1] = 31
    dom[2] = 28
    dom[3] = 31
    dom[4] = 30
    dom[5] = 31
    dom[6] = 30
    dom[7] = 31
    dom[8] = 31
    dom[9] = 30
    dom[10] = 31
    dom[11] = 30
    dom[12] = 31


    # initialize empty dictionaries
    d_tdr = {}
    d_ctflg = {}
    
    d_tdr[site] = {}
    d_ctflg[site] = {}
    
    for y in range(start_year, end_year+1):
        if y in range(2000,4001,4):      # not Y4K compliant!!!
            dom[2] = 29
        d_tdr[site][y] = {}
        d_ctflg[site][y] = {}
        
        for m in range(1,13):
            d_tdr[site][y][m] = {}
            d_ctflg[site][y][m] = {}
           
            for d in range(1,dom[m]+1):
                d_tdr[site][y][m][d] = 'na'
                d_ctflg[site][y][m][d] = ''


    # read in daily data and save in daily dictionaries
    dd = np.genfromtxt(daypath,delimiter=',',dtype='str',skip_header=1)
    for row in dd:
        date = row[1].split('/')
        mon = int(date[0])
        day = int(date[1])
        yr = int(date[2])
        if obs_type.split('_')[0] == 'salinity':
            av = row[2]
            mn = row[4]
            mx = row[5]
            ct = row[7]
        elif obs_type.split('_')[0] == 'stage':
            av = row[8]
            mn = row[10]
            mx = row[11]
            ct = row[13]

        if yr in range(start_year,end_year+1):
            if int(ct == 0):
                tdr = 'na'
                ctflg = ''
            else:
                try:
                    tdr = float(mx) - float(mn)
                    if int(ct) != 24:
                        #ctflg = '*'
                        tdr = 'na'
                        ctflg = ''
                    else:
                        ctflg = ''
                except:
                    tdr = 'na'
                    ctflg = ''
##        print(site,yr,mon,day,tdr)
##        input()
        d_tdr[site][yr][mon][day] = tdr
        d_ctflg[site][yr][mon][day] = ctflg
    return(d_tdr,d_ctflg)     

##################################################################################################
### looping over sites to build daily timeseries for calculations performed in functions above ###
##################################################################################################
print ('\n\nsetting things up...')
import numpy as np

topdir = r'E:\CRMS'
masterCRMS = r'%s\CRMS_Continuous_Hydrographic_20190428.csv' % topdir
masterCRMSlist = r'%s\CRMS_sites.csv' % topdir
sites = np.genfromtxt(masterCRMSlist,dtype='str')

sy = 2006
ey = 2018

dom = {}
dom[1] = 31
dom[2] = 28
dom[3] = 31
dom[4] = 30
dom[5] = 31
dom[6] = 30
dom[7] = 31
dom[8] = 31
dom[9] = 30
dom[10] = 31
dom[11] = 30
dom[12] = 31

all_data = {}
for site in sites:
    all_data[site] = {}
    
for y in range(sy,ey+1):
    for m in range(1,13):
        if y in (2000,4001,4):
            dom[2] = 29
        for d in range(1,dom[m]+1):
            ymd = '%04d%02d%02d' % (y,m,d)
            all_data[site][ymd] = '-'

            
ns = 0    
for site in sites:
    ns += 1
    print(' %03d/%03d  - %s' %(ns,len(sites),site) )
    
    rawpath = r'%s\raw\%s_raw.csv' % (topdir,site)
    hrpath = r'%s\clean_hourly\%s_hourly_English.csv' % (topdir,site)
    daypath = r'%s\clean_daily\%s_daily_English.csv' % (topdir,site)
    geoidfile = r'%s\CRMS_GEOID99_TO_GEOID12A.csv' % topdir

    if ns == 1:
        write_hdr = 'True'
    else:
        write_hdr = 'False'

    daily_returns = CRMS_hydro_daily_tidal_range(site,sy,ey+1,'stage_ft_NAVD88-g12a',topdir,write_hdr)
    tr = daily_returns[0]
    cf = daily_returns[1]

    for y in tr[site].keys():
        for m in tr[site][y].keys():
            for d in tr[site][y][m].keys():
                ymd = '%04d%02d%02d' % (y,m,d)
                try:
                    val = '%0.2f%s' % (tr[site][y][m][d],cf[site][y][m][d])
                except:
                    val = '%s%s' % (tr[site][y][m][d],cf[site][y][m][d])
                all_data[site][ymd] = val

print('writing output file')
with open(r'%s\daily_tidal_range.csv' % topdir,mode='w') as outf:
    hdr = 'YYYYMMDD,MM-DD-YYYY'
    for site in sites:
        hdr = '%s,%s' % (hdr,site)
    outf.write('%s\n' % hdr)

    
    for ymd in all_data[sites[0]].keys():
        linestring = '%s,%s-%s-%s' % (ymd,ymd[4:6],ymd[6:8],ymd[0:4])
        for site in sites:
            linestring = '%s,%s' % (linestring,all_data[site][ymd])
        outf.write('%s\n' % linestring)
        
