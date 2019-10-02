import numpy as np
topdir = r'E:\CRMS'
fi = '%s\Full_Marsh_Vegetation_20190502.csv' % topdir
start_year,end_year = 2012,2019

WLout = '%s\CMRS_Veg_comments_WaterLevel.csv' % topdir
WLUout = '%s\CMRS_Veg_comments_WaterLevelUnits.csv' % topdir
OWout = '%s\CMRS_Veg_comments_OpenWater.csv' % topdir
BGout = '%s\CMRS_Veg_comments_BareGround.csv' % topdir
DVout = '%s\CMRS_Veg_comments_DeadVeg.csv' % topdir
FUout = '%s\CMRS_Veg_comments_FloodedUndetermined.csv' % topdir



WL = {}     # dictionary to hold water level comment
WLu = {}    # dictionary to hold water level units
OW = {}     # dictionary to hold open water comment
BG = {}     # dictionary to hold bare ground comment
DV = {}     # dictionary to hold dead vegetation comment
FU = {}     # dictionary to hold flooded-undetermined comment
sites = []  # array to hold the CRMS sites in the order in which they are encountered in the input file

with open(fi,mode='r') as ifn:
    nli = 0
    for line in ifn:
        nli += 1
        if nli == 1:
            hdr = line
        else:
            spli = line.split(',')
            s = spli[0]
            mdy = spli[3]   # date is 4th column in veg file
            com = spli[29]  # comment is the 30th column in veg file

            day = mdy.split('/')[0]
            mon = mdy.split('/')[1]
            yr = int(mdy.split('/')[2])

            if s not in sites:
                print('found site: %s' % s)
                sites.append(s)
                WL[s] = {}
                WLu[s] = {}
                OW[s] = {}
                BG[s] = {}
                DV[s] = {}
                FU[s] = {}
                for y in range(start_year, end_year+1):
                    WL[s][y] = 'na'                    
                    WLu[s][y] = 'na'                    
                    OW[s][y] = 'na'                    
                    BG[s][y] = 'na'                    
                    DV[s][y] = 'na'                     
                    FU[s][y] = 'na'                    
            
            if yr >= start_year:
                for comment in com.split('. '):
                    try:
                        cs_ds = comment.split('  ')
                        if len(cs_ds) > 1:
                            cs_ss = cs_ds[0]
                            for a in range(1,len(cs_ds)):
                                cs_ss = '%s %s' % (cs_ss,cs_ds[a])                       
                        else:
                            cs_ss = comment
                    except:
                        cs_ss = comment

                    if WL[s][yr] == 'na':
                        if 'Water Level is ' in comment:
                            cs = cs_ss.split('Water Level is ')
                            try:
                                WL[s][yr] = cs[1].split(' ')[0]
                            except:
                                 WL[s][yr] = 'na'
                            try:
                                if WL[s][yr] != 'below':
                                    if WL[s][yr] != 'Below':
                                        WLu[s][yr] = '%s %s %s' % (cs[1].split(' ')[1],cs[1].split(' ')[2],cs[1].split(' ')[3])
                            except:
                                WLu[s][yr] = 'na'
                                
                    if 'Open water is ' in comment:
                        csow = comment.split('Open water is ')
                        if OW[s][yr] == 'na':
                            OW[s][yr] = csow[1].split('.')[0]

                    if 'Bare ground is ' in comment:
                        csbg = comment.split('Bare ground is ')
                        if BG[s][yr] == 'na':
                            BG[s][yr] = csbg[1].split('.')[0]

                    if 'Dead vegetation is ' in comment:
                        csdv = comment.split('Dead vegetation is ')
                        if DV[s][yr] == 'na':
                            DV[s][yr] = csdv[1].split('.')[0]

                    if 'Flooded-Undetermined is ' in comment:
                        csfu = comment.split('Flooded-Undetermined is ')
                        if FU[s][yr] == 'na':
                            FU[s][yr] = csfu[1].split('.')[0]

hdr = 'site'
for y in range(start_year, end_year+1):
    hdr = '%s,%s' % (hdr,y)

with open(WLout,mode='w') as wlof:
    wlof.write('%s\n' % hdr)
    for s in sites:
        wrline = '%s' % s
        for y in range(start_year, end_year+1):
            wrline = '%s,%s' % (wrline,WL[s][y])
        wlof.write('%s\n' % wrline )   

with open(WLUout,mode='w') as wluof:
    wluof.write('%s\n' % hdr)
    for s in sites:
        wrline = '%s' % s
        for y in range(start_year, end_year+1):
            wrline = '%s,%s' % (wrline,WLu[s][y])
        wluof.write('%s\n' % wrline )   

with open(OWout,mode='w') as owof:
    owof.write('%s\n' % hdr)
    for s in sites:
        wrline = '%s' % s
        for y in range(start_year, end_year+1):
            wrline = '%s,%s' % (wrline,OW[s][y])
        owof.write('%s\n' % wrline )

with open(BGout,mode='w') as bgof:
    bgof.write('%s\n' % hdr)
    for s in sites:
        wrline = '%s' % s
        for y in range(start_year, end_year+1):
            wrline = '%s,%s' % (wrline,BG[s][y])
        bgof.write('%s\n' % wrline )   

with open(DVout,mode='w') as dvof:
    dvof.write('%s\n' % hdr)
    for s in sites:
        wrline = '%s' % s
        for y in range(start_year, end_year+1):
            wrline = '%s,%s' % (wrline,DV[s][y])
        dvof.write('%s\n' % wrline )

with open(FUout,mode='w') as fuof:
    fuof.write('%s\n' % hdr)
    for s in sites:
        wrline = '%s' % s
        for y in range(start_year, end_year+1):
            wrline = '%s,%s' % (wrline,FU[s][y])
        fuof.write('%s\n' % wrline )   


