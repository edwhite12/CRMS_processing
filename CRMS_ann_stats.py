import numpy as np
topdir = r'E:\CRMS'
#f = r'CRMS_salinity_ppt_max'
f = r'CRMS_stage_ft_NAVD88-g12a_max'
fi = '%s\%s.csv' % (topdir,f)
fo = '%s\%s_ann.csv' % (topdir,f)
d = {}

masterCRMSlist = r'%s\CRMS_sites.csv' % topdir
sites = np.genfromtxt(masterCRMSlist,dtype='str')

for s in sites:
    d[s]={}
    for y in range(2006, 2020):
        d[s][y] = -9999.0



with open(fi,mode='r') as ifn:
    nli = 0
    for line in ifn:
        if nli == 0:
            hdr = line
        else:
            spli = line.split(',')
            s = spli[0]
            for n in range(2,16):
                v = spli[n]
                y = range(2006,2020)[n-2]
                if v[0:2] != 'na':
                    d[s][y] = min(d[s][y],float(v))
                    d[s][y] = max(d[s][y],float(v))
        nli += 1

with open(fo,mode='w') as ofn:
    ofn.write(hdr)
    for s in sites:
        lw = '%s,01.12' % s
        for y in range(2006,2020):
            if d[s][y] == -9999.0:
                vt = 'na'
            else:
                vt = d[s][y]
            lw = '%s,%s' % (lw,vt)
        ofn.write('%s\n' % lw)


        
        
