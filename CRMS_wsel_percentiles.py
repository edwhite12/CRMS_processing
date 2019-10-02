import numpy as np
import os

topdir = r'E:\CRMS\clean_hourly'
sitefiles = os.listdir(topdir)
allsites = []
sumdi = {}
for y in range(2006,2020):
    sumdi[y] = {}
    sumdi[y]['n'] = {}
    for p in [0,1,10,20,30,40,50,60,70,80,90,99,100]:
        sumdi[y]['P%02d'%p] = {}
nsite = 0
for sitefile in sitefiles:
    nsite += 1
    hourpath = r'%s\%s' % (topdir,sitefile)
    site = sitefile.split('_')[0]
    allsites.append(site)
    print('analyzing %03d/%03d:  %s' % (nsite,len(sitefiles),site))
    din = np.genfromtxt(hourpath,delimiter=',',dtype='str',skip_header=1,usecols=[1,6])
    dd = {}
    for y in range(2006,2020):
        dd[y] = []

    for r in din:
        y = int(r[0].split('/')[2])
        if r[1] != 'na':
            dd[y].append(float(r[1]))

    for y in range(2006,2020):
        sumdi[y]['n'][site]=len(dd[y])
        if len(dd[y])> 10:
            for p in [0,1,10,20,30,40,50,60,70,80,90,99,100]:
                sumdi[y]['P%02d'%p][site] = np.percentile(dd[y],p)
        else:
            for p in [0,1,10,20,30,40,50,60,70,80,90,99,100]:
                sumdi[y]['P%02d'%p][site] = 'na'
    
for p in [0,1,10,20,30,40,50,60,70,80,90,99,100]:
    outfile = r'E:\CRMS\WSEL_hourly_data_counts.csv'
    with open(outfile,mode='w') as of:
        hdr = 'site'
        for y in range(2006,2020):
            hdr = '%s,%s' % (hdr, y)
        of.write('%s\n' % hdr)
        for site in allsites:
            wrstr = '%s' % site
            for y in range(2006,2020):
                val = sumdi[y]['n'][site]
                wrstr = '%s,%s' %(wrstr,val)
            of.write('%s\n' % wrstr)

    
for p in [0,1,10,20,30,40,50,60,70,80,90,99,100]:
    outfile = r'E:\CRMS\WSEL_percentile_p%02d_English.csv' % p
    with open(outfile,mode='w') as of:
        hdr = 'site'
        for y in range(2006,2020):
            hdr = '%s,%s' % (hdr, y)
        of.write('%s\n' % hdr)
        for site in allsites:
            wrstr = '%s' % site
            for y in range(2006,2020):
                val = sumdi[y]['P%02d' % p][site]
                wrstr = '%s,%s' %(wrstr,val)
            of.write('%s\n' % wrstr)

            
    
