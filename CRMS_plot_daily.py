print('setting up...')
import os
import numpy as np
import datetime as dt
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.dates as mpd


fol = r'E:\CRMS\clean_daily'
outf = r'E:\CRMS\clean_daily\salinity_plots'

sitefiles = os.listdir(fol)

for sitefile in sitefiles:
    if (sitefile[0:4] == 'CRMS'):
            
        site = sitefile.split('_')[0]
        
        print('plotting %s...' % site)

        plot_title = site

        dates = []
        vals = []


        fn = r'%s_daily_English.csv' % site

        csvf = r'%s\%s' % (fol,fn)
        date_col = 1    # column with date in CRMS csv file
        val_col = 2     # column with value in CRMS csv file (2 = daily mean salinity, 8 = daily mean stage)

        y_txt = r'Daily Mean Salinity (ppt)'
        y_range = [0, 36]
        x_txt = r'Elapsed Year'
        x_range = [dt.date(2006,1,1),dt.date(2019,12,31)]
        serieslabel = site


        pngfile = r'%s\%s_salinity.png' % (outf,site)

        f=np.genfromtxt(csvf,dtype=(str,str),skip_header=1,usecols=[date_col,val_col],delimiter=',')

        for row in f:
                if row[1] != 'na':
                        dates.append(dt.date(int(row[0].split('/')[2]),int(row[0].split('/')[0]),int(row[0].split('/')[1])))
                        vals.append(float(row[1]))


        dates_plt = mpd.date2num(dates)
        fig = plt.figure()
        fig.suptitle(plot_title)
        ax = fig.add_subplot(111,facecolor='whitesmoke')
        ax.set_ylabel(y_txt)
        #ax.set_xlabel(x_txt)
        ax.plot_date(dates_plt,vals,marker='o',markersize=2,linestyle='solid',linewidth=0,color='red',label=serieslabel)
        ax.legend(loc='upper right',edgecolor='none',facecolor='none')
        #ax.set_ylim(y_range)
        ax.set_xlim(x_range)
        ax.grid(True,which='both',axis='both',color='silver',linewidth=0.5)

        plt.savefig(pngfile)
        plt.close()

print('done.')



