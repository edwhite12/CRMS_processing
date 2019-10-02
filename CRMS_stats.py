def CRMS_hydro_stats(site, start_year, end_year, obs_type, topdir, write_hdr):
    import numpy as np
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
        
        for m in range(1,13):
            d_sum_wt[site][y][m] = 0.0
            d_ct[site][y][m] = 0.0
            d_min[site][y][m] = 9999.9
            d_max[site][y][m] = 0.0
            d_ave[site][y][m] = 0.0
            d_stdv[site][y][m] = 0.0
            d_hr_resid[site][y][m] = 0.0
            
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
                d_sum_wt[site][yr][mon] += float(av)*float(ct)
                d_ct[site][yr][mon] += float(ct)
                d_min[site][yr][mon] = min(d_min[site][yr][mon],float(mn))
                d_max[site][yr][mon] = max(d_max[site][yr][mon],float(mx))

    # calculate average
    for y in range(start_year,end_year+1):
        for m in range(1,13):
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
                if d_ave[site][yr][mon] != 'na':
                    d_hr_resid[site][yr][mon] += (float(hval)-d_ave[site][yr][mon])**2.0
    # calculate standard deviation
    for y in range(start_year,end_year+1):
        for m in range(1,13):
            try:
                d_stdv[site][y][m] = (d_hr_resid[site][y][m]/(float(d_ct[site][y][m])-1))**0.5
            except:
                d_stdv[site][y][m] = 'na'
    
    # write output summary tables and save to file
    dicts = [d_ave,d_stdv,d_min,d_max]
    outs = ['%s_ave' % obs_type,'%s_stdev' % obs_type,'%s_min' % obs_type,'%s_max' % obs_type]
    for dn in range(0,len(dicts)):
        d = dicts[dn]
        outpath = r'%s\CRMS_%s.csv' % (topdir,outs[dn])

        with open(outpath,mode='a') as osf:
            if write_hdr == 'True':
                header = ('Site,month')
                for y in range(start_year,end_year+1):
                    header = '%s,%s' % (header,y)
                osf.write('%s\n' % header)
           
            for m in range(1,13):
                oline = '%s,%02d' % (site,m)
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

                osf.write('%s\n' % oline)

    del(d_ave,d_stdv,d_hr_resid,d_sum_wt,d_ct,d_min,d_max,)

def CRMS_moving_window(site, start_year, end_year, obs_type, topdir, write_hdr):
    import numpy as np
    
    daypath = r'%s\clean_daily\%s_daily_English.csv' % (topdir,site)
    
    # build empty dictionaries with a key for every year, month, and day - initialized as na

    av_in = {}
    av_14d = {}
    for y in range(start_year,end_year+1):
        av_in[y] = {}
        av_14d[y] = {}
        
        dim = {}
        dim[1],dim[2],dim[3],dim[4],dim[5],dim[6],dim[7],dim[8],dim[9],dim[10],dim[11],dim[12] = 31,28,31,30,31,30,31,31,30,31,30,31
        if y in range(2000,2100,4):
            dim[2] = 29
        
        for m in range(1,13):
            av_in[y][m] = {}
            av_14d[y][m] = {}

            for d in range(1,dim[m]+1):
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
            av_in[yr][mon][day] = raw_in

    # filter through daily dictionary and fill missing data with last observed value
    all_data = []
    all_data_flag = []
    all_data_filled = []
    for y in range(start_year,end_year+1):
        for m in range(1,13):
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
    

    mov14_ave = []        
    for win_end in range(0,len(all_data)):
        sum14 = 0.0
        if(win_end < 14):
            try:
                sum14 += all_data_filled[0]
            except:
                sum14 = 'na'
        else:
            for i14 in range(0,14):
                fildat = all_data_filled[win_end-i14]
                try:
                    sum14 += float(fildat)
                except:
                    sum14 = 'na'
        if sum14 != 'na':
            mov14_ave.append(sum14/14.0)
        else:
            mov14_ave.append('na')

    # convert array of daily timeseries into dictionary
    cntr = 0
    for y in range(start_year,end_year+1):
        for m in range(1,13):
            for d in av_14d[y][m].keys():
                av_14d[y][m][d] = mov14_ave[cntr]
                cntr += 1
    
    # print moving window output timeseries for QA 
    #with open(r'E:\CRMS\test.csv', mode='w') as outf:
    #    outf.write('orig,filled,flag,14d_ave\n')
    #    for i in range(0,len(all_data)):
    #        outf.write('%s,%s,%s,%s\n' % (all_data[i],all_data_filled[i],all_data_flag[i],mov14_ave[i]))

    outpath = r'%s\CRMS_max_14day_ave_%s.csv' % (topdir,obs_type)
    with open(outpath,mode='a') as osf:
        if write_hdr == 'True':
            header = ('Site,month')
            for y in range(start_year,end_year+1):
                header = '%s,%s' % (header,y)
            osf.write('%s\n' % header)

        for m in range(1,13):
            oline = '%s,%02d' % (site,m)
            for y in range(start_year,end_year+1):
                try:
                    max_av_14d = 0.0
                    for d in av_14d[y][m].keys():
                        max_av_14d = max(av_14d[y][m][d],max_av_14d)
                    f_val = max_av_14d
                    s_val = '%0.1f' % f_val
                except:
                    s_val = 'na'

                oline = '%s,%s' % (oline,s_val)
            osf.write('%s\n' % oline)        



            
