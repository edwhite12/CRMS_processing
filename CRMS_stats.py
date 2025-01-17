def months2use(start_year,end_year):
    months2range01 = [1,12]
    range01 = '%02d-%02d' % (months2range01[0],months2range01[1])
    
    months2range02 = [5,10]
    range02 = '%02d-%02d' % (months2range02[0],months2range02[1])
    
    months = [1,2,3,4,5,6,7,8,9,10,11,12,range01,range02]        
    dom = {}
    
    for y in range(start_year, end_year+1):
        # determine number of days in each month
        dom[y] = {}
        dom[y][1] = 31
        if y in range(2000,4001,4):      # not Y4K compliant!!!
            dom[y][2] = 29
        else:
            dom[y][2] = 28
        dom[y][3] = 31
        dom[y][4] = 30
        dom[y][5] = 31
        dom[y][6] = 30
        dom[y][7] = 31
        dom[y][8] = 31
        dom[y][9] = 30
        dom[y][10] = 31
        dom[y][11] = 30
        dom[y][12] = 31
        
        # determine number of days in two ranges
        dom[y][range01] = 0
        dom[y][range02] = 0
        
        for mon in range(1,13):
            # check if month is included in range01 (inclusive)
            if mon >= months2range01[0]:
                if mon <= months2range01[1]:
                    dom[y][range01] += dom[y][mon]
            # check if month is included in range02 (inclusive)
            if mon >= months2range02[0]:
                if mon <= months2range02[1]:
                    dom[y][range02] += dom[y][mon]

    return(months,months2range01,range01,months2range02,range02,dom)
        

def CRMS_hydro_daily_calcs(site, start_year, end_year, obs_type, topdir, write_hdr):
    import numpy as np
    
    months,months2range01,range01,months2range02,range02,dom = months2use(start_year,end_year)
    
    daypath = r'%s\clean_daily\%s_daily_English.csv' % (topdir,site)
    hourpath = r'%s\clean_hourly\%s_hourly_English.csv' % (topdir,site)
    
    # initialize empty dictionaries
    d_sum_wt = {}
    d_ct = {}
    d_min = {}
    d_max = {}  
    d_ave = {}
    d_stdv = {}
    d_hr_resid = {}
    
    d_sum_wt[site] = {}
    d_ct[site] = {}
    d_min[site] = {}
    d_max[site] = {} 
    d_ave[site] = {}
    d_stdv[site] = {}
    d_hr_resid[site] = {}
    
    for y in range(start_year, end_year+1):
        d_sum_wt[site][y] = {}
        d_ct[site][y] = {}
        d_min[site][y] = {}
        d_max[site][y] = {}
        d_ave[site][y] = {}
        d_stdv[site][y] = {}
        d_hr_resid[site][y] = {}
        
        for m in months:
            d_sum_wt[site][y][m] = {}
            d_ct[site][y][m] = {}
            d_min[site][y][m] = {}
            d_max[site][y][m] = {}
            d_ave[site][y][m] = {}
            d_stdv[site][y][m] = {}
            d_hr_resid[site][y][m] = {}
            
            for d in range(1,dom[y][m]+1):
                d_sum_wt[site][y][m][d] = 0.0
                d_ct[site][y][m][d] = 0.0
                d_min[site][y][m][d] = 9999.9
                d_max[site][y][m][d] = 0.0
                d_ave[site][y][m][d] = 0.0
                d_stdv[site][y][m][d] = 0.0
                d_hr_resid[site][y][m][d] = 0.0

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
                        ctflg = '*'
                    else:
                        ctflg = ''
                except:
                    tdr = 'na'
                    ctflg = ''
  
        
def CRMS_hydro_stats(site, start_year, end_year, obs_type, topdir, write_hdr):
    import numpy as np
    
    months,months2range01,range01,months2range02,range02,dom = months2use(start_year,end_year)
    
    daypath = r'%s\clean_daily\%s_daily_English.csv' % (topdir,site)
    hourpath = r'%s\clean_hourly\%s_hourly_English.csv' % (topdir,site)

    # initialize empty dictionaries
    d_sum_wt = {}
    d_ct = {}
    d_min = {}
    d_max = {}  
    d_ave = {}
    d_stdv = {}
    d_mdn = {}
    d_hr_resid = {}
    d_hr_list = {}
    
    d_sum_wt[site] = {}
    d_ct[site] = {}
    d_min[site] = {}
    d_max[site] = {} 
    d_ave[site] = {}
    d_stdv[site] = {}
    d_mdn[site] = {}
    d_hr_resid[site] = {}
    d_hr_list[site] = {}
    
    for y in range(start_year, end_year+1):
        d_sum_wt[site][y] = {}
        d_ct[site][y] = {}
        d_min[site][y] = {}
        d_max[site][y] = {}
        d_ave[site][y] = {}
        d_stdv[site][y] = {}
        d_mdn[site][y] = {}
        d_hr_resid[site][y] = {}
        d_hr_list[site][y] = {}
        
        for m in months:
            d_sum_wt[site][y][m] = 0.0
            d_ct[site][y][m] = 0.0
            d_min[site][y][m] = 9999.9
            d_max[site][y][m] = 0.0
            d_ave[site][y][m] = 0.0
            d_stdv[site][y][m] = 0.0
            d_mdn[site][y][m] = 0.0
            d_hr_resid[site][y][m] = 0.0
            d_hr_list[site][y][m] = []
            
    # read in daily data and save in monthly dictionaries
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
            if av != 'na':
                # add daily data to current year-month dictionary
                d_sum_wt[site][yr][mon] += float(av)*float(ct)
                d_ct[site][yr][mon] += float(ct)
                d_min[site][yr][mon] = min(d_min[site][yr][mon],float(mn))
                d_max[site][yr][mon] = max(d_max[site][yr][mon],float(mx))
                
                # add daily data to current year-month dictionary for first range of months (range01)
                if mon >= months2range01[0]:
                    if mon <= months2range01[1]:
                        d_sum_wt[site][yr][range01] += float(av)*float(ct)
                        d_ct[site][yr][range01] += float(ct)
                        d_min[site][yr][range01] = min(d_min[site][yr][range01],float(mn))
                        d_max[site][yr][range01] = max(d_max[site][yr][range01],float(mx))

                # add daily data to current year-month dictionary for second range of months (range02)
                if mon >= months2range02[0]:
                    if mon <= months2range02[1]:
                        d_sum_wt[site][yr][range02] += float(av)*float(ct)
                        d_ct[site][yr][range02] += float(ct)
                        d_min[site][yr][range02] = min(d_min[site][yr][range02],float(mn))
                        d_max[site][yr][range02] = max(d_max[site][yr][range02],float(mx))


    # calculate average
    for y in range(start_year,end_year+1):
        for m in months:
            if d_ct[site][y][m] != 0.0:
                d_ave[site][y][m] = d_sum_wt[site][y][m]/float(d_ct[site][y][m])
            else:
                d_ave[site][y][m] = 'na'

    # read in hourly data to calculate standard deviation
    hd = np.genfromtxt(hourpath,delimiter=',',dtype='str',skip_header=1)
    for row in hd:
        date = row[1].split('/')
        mon = int(date[0])
        day = int(date[1])
        yr = int(date[2])
        if obs_type.split('_')[0] == 'salinity':
            hval = row[4]
        elif obs_type.split('_')[0] == 'stage':
            hval = row[6]
        if yr in range(start_year,end_year+1):
            if hval != 'na':
                # add hourly data point to two dictionaries (d_hr_resid & d_hr_list) used in calculating standard deviation for month, mon
                if d_ave[site][yr][mon] != 'na':
                    d_hr_resid[site][yr][mon] += (float(hval)-d_ave[site][yr][mon])**2.0
                d_hr_list[site][yr][mon].append(float(hval))
                
                # add hourly data point to two dictionaries (d_hr_resid & d_hr_list) used in calculating standard deviation for first range of months, range01
                if mon >= months2range01[0]:
                    if mon <= months2range01[1]:
                        if d_ave[site][yr][range01] != 'na':
                            d_hr_resid[site][yr][range01] += (float(hval)-d_ave[site][yr][range01])**2.0
                        d_hr_list[site][yr][range01].append(float(hval))                
                
               # add hourly data point to two dictionaries (d_hr_resid & d_hr_list) used in calculating standard deviation for second range of months, range02
                if mon >= months2range02[0]:
                    if mon <= months2range02[1]:
                        if d_ave[site][yr][range02] != 'na':
                            d_hr_resid[site][yr][range02] += (float(hval)-d_ave[site][yr][range02])**2.0
                        d_hr_list[site][yr][range02].append(float(hval))
                
                
    # calculate standard deviation
    for y in range(start_year,end_year+1):
        for m in months:
            try:
                d_stdv[site][y][m] = (d_hr_resid[site][y][m]/(float(d_ct[site][y][m])-1))**0.5
            except:
                d_stdv[site][y][m] = 'na'
    
    # calculate median
    for y in range(start_year,end_year+1):
        for m in months:
            try:
                d_mdn[site][y][m] = np.median(d_hr_list[site][y][m])
            except:
                d_mdn[site][y][m] = 'na'
    
    
    # write output summary tables and save to file
    dicts = [d_ave,d_stdv,d_min,d_max,d_mdn]
    outs = ['%s_ave' % obs_type,'%s_stdev' % obs_type,'%s_min' % obs_type,'%s_max' % obs_type,'%s_median' % obs_type]
    for dn in range(0,len(dicts)):
        d = dicts[dn]
        
        # write gridded output file
        outpath = r'%s\stats\CRMS_%s.csv' % (topdir,outs[dn])
        with open(outpath,mode='a') as osf:
            if write_hdr == 'True':
                header = ('Site,month')
                for y in range(start_year,end_year+1):
                    header = '%s,%s' % (header,y)
                _ = osf.write('%s\n' % header)
            for m in months:
                oline = '%s,%s' % (site,m)
                for y in range(start_year,end_year+1):
                    if d_ct[site][y][m] != 0.0:
                        f_val = d[site][y][m]
                        try:
                            s_val = '%0.4f' % f_val
                        except:
                            s_val = 'na'
                    else:
                        s_val = 'na'
                    oline = '%s,%s' % (oline,s_val)
                _ = osf.write('%s\n' % oline)
        
        # write stacked output file
        outpath2 = r'%s\stats\CRMS_%s_stacked.csv' % (topdir,outs[dn])
        with open(outpath2,mode='a') as osf2:
            if write_hdr == 'True':
                header = ('Site,MM-YYYY,Value')
                _ = osf2.write('%s\n' % header)
            for y in range(start_year,end_year+1):
                for m in months:
                    oline = '%s,%s-%04d' % (site,m,y)
                    if d_ct[site][y][m] != 0.0:
                        f_val = d[site][y][m]
                        if f_val != 'na':
                            try:
                                s_val = '%0.4f' % f_val
                            except:
                                s_val = 'na'
                        else:
                            s_val = 'na'
                    else:
                        s_val = 'na'
                    _ = osf2.write('%s,%s\n' % (oline,s_val))

    del(d_ave,d_stdv,d_hr_resid,d_sum_wt,d_ct,d_min,d_max,d_mdn,d_hr_list)


def CRMS_moving_window(site, start_year, end_year, obs_type, topdir, write_hdr):
    import numpy as np
    
    months,months2range01,range01,months2range02,range02,dom = months2use(start_year,end_year)

    daypath = r'%s\clean_daily\%s_daily_English.csv' % (topdir,site)
    
    # build empty dictionaries with a key for every year, month, and day - initialized as na

    av_in = {}
    av_14d = {}
    for y in range(start_year,end_year+1):
        av_in[y] = {}
        av_14d[y] = {}
        
        for m in months:
            av_in[y][m] = {}
            av_14d[y][m] = {}
            for d in range(1,dom[y][m]+1):
                av_in[y][m][d] = 'na'
                av_14d[y][m][d] = 'na'

    # read in daily data and save in daily dictionaries
    dd = np.genfromtxt(daypath,delimiter=',',dtype='str',skip_header=1)
    for row in dd:
        date = row[1].split('/')
        mon = int(date[0])
        day = int(date[1])
        yr = int(date[2])

        if obs_type.split('_')[0] == 'salinity':
            raw_in = row[2]
        elif obs_type.split('_')[0] == 'stage':
            raw_in = row[8]

        if raw_in != 'na':
            # save input data value to dictionary for specific months/years used in moving window
            av_in[yr][mon][day] = raw_in

            # save input data point to dictionary used in moving window for first range of months, range01
            if mon >= months2range01[0]:
                if mon <= months2range01[1]:
                    av_in[yr][range01][day] = raw_in
            
            # save input data point to dictionary used in moving window for second range of months, range02
            if mon >= months2range02[0]:
                if mon <= months2range02[1]:
                    av_in[yr][range02][day] = raw_in

    # filter through daily dictionary and fill missing data with last observed value
    all_data = []
    all_data_flag = []
    all_data_filled = []
    for y in range(start_year,end_year+1):
        for m in months:
            for d in av_in[y][m].keys():
                all_data.append(av_in[y][m][d])
                all_data_flag.append('')
                all_data_filled.append('na')

    # fill missing data with last good data point                
    for i in range(0,len(all_data)):
        orig = all_data[i]
        if orig == 'na':
            for ip in range(i,min(i+500,len(all_data))):
                brfl = 0
                nxt = all_data[ip]
                if nxt != 'na':
                    all_data_filled[i] = float(nxt)
                    all_data_flag[i] = 'f'
                    break
        else:
            all_data_filled[i] = float(all_data[i])
            all_data_flag[i] = ''
    
#    # calculate 14-day moving window average using filled data
#    mov14_ave = []        
#    for win_end in range(0,len(all_data)):
#        sum14 = 0.0
#        if(win_end < 14):
#            try:
#                sum14 += all_data_filled[0]
#            except:
#                sum14 = 'na'
#        else:
#            for i14 in range(0,14):
#                fildat = all_data_filled[win_end-i14]
#                try:
#                    sum14 += float(fildat)
#                except:
#                    sum14 = 'na'
#        if sum14 != 'na':
#            mov14_ave.append(sum14/14.0)
#        else:
#            mov14_ave.append('na')

    # calculate 14-day moving window average using skipping missing data data
    mov14_ave = []

    for win_end in range(0,len(all_data)):
        sum14 = 0.0
        cntr = 0
        if(win_end < 14):
            try:        # if try fails, that means value of data is 'na' - skip
                sum14 += float(all_data[0])
                cntr += 1
            except:
                sum14 = sum14
                #sum14 = 'na'
        else:
            for i14 in range(0,14):
                fildat = all_data[win_end-i14]
                try:    # if try fails, that means value of data is 'na' - skip
                    sum14 += float(fildat)
                    cntr += 1
                except:
                    sum14 = sum14
                    #sum14 = 'na'
        if cntr != 0:
            mov14_ave.append(sum14/cntr)
        else:
            mov14_ave.append('na')



    # convert array of daily timeseries into dictionary
    cntr = 0
    for y in range(start_year,end_year+1):
        for m in months:
            for d in av_14d[y][m].keys():
                av_14d[y][m][d] = mov14_ave[cntr]
                cntr += 1

    # print moving window output timeseries for QA 
    #with open(r'E:\CRMS\test.csv', mode='w') as outf:
    #    outf.write('orig,filled,flag,14d_ave\n')
    #    for i in range(0,len(all_data)):
    #        outf.write('%s,%s,%s,%s\n' % (all_data[i],all_data_filled[i],all_data_flag[i],mov14_ave[i]))

    #write gridded output file
    outpath = r'%s\stats\CRMS_max_14day_ave_%s.csv' % (topdir,obs_type)
    with open(outpath,mode='a') as osf:
        if write_hdr == 'True':
            header = ('Site,month')
            for y in range(start_year,end_year+1):
                header = '%s,%s' % (header,y)
            osf.write('%s\n' % header)
        
        for m in months:
            oline = '%s,%s' % (site,m)
            for y in range(start_year,end_year+1):
                s_val = 'na'
                
                max_av_14d = 0.0
                for d in av_14d[y][m].keys():
                    if av_14d[y][m][d] != 'na':
                        max_av_14d = max(av_14d[y][m][d],max_av_14d)
                        f_val = max_av_14d
                        s_val = '%0.1f' % f_val

                oline = '%s,%s' % (oline,s_val)
            osf.write('%s\n' % oline)        

    #write stacked output file
    outpath2 = r'%s\stats\CRMS_max_14day_ave_%s_stacked.csv' % (topdir,obs_type)
    with open(outpath2,mode='a') as osf2:
        if write_hdr == 'True':
            header = ('Site,MM-YYYY,Value')
            _ = osf2.write('%s\n' % header)
        for y in range(start_year,end_year+1):
            for m in months:
                oline = '%s,%s-%04d' % (site,m,y)
                try:
                    max_av_14d = 0.0
                    for d in av_14d[y][m].keys():
                        max_av_14d = max(av_14d[y][m][d],max_av_14d)
                    f_val = max_av_14d
                    s_val = '%0.1f' % f_val
                except:
                    s_val = 'na'

                _ = osf2.write('%s,%s\n' % (oline,s_val))
                
