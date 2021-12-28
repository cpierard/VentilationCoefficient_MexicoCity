import numpy as np
import h5py
import sys
import os
import shutil
import matplotlib.pyplot as plt
from osgeo import gdal
from mpl_toolkits.basemap import Basemap
from pylab import rcParams
import pandas as pd

path2wrf = '/Volumes/BUFFALO_SOLDIER/datos_VC/'

months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'}

location = ['MER', 'PED', 'SAG', 'TLA', 'UIZ', 'SFE']

xlat = np.loadtxt('../datos/xlat_d02_interpolado.txt')
xlong = np.loadtxt('../datos/xlong_d02_interpolado.txt')


print('***START***')

dir = "../datos/max_min_anual"
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)


for hour in range(11, 15):

    monthly_max = np.zeros((12,102,128))
    monthly_min = np.zeros((12,102,128))

    annual_max = np.zeros((102,128))
    annual_min = np.zeros((102,128))

    dir2 = "../datos/max_min_anual/" + str(hour)
    if os.path.exists(dir2):
        shutil.rmtree(dir2)
    os.makedirs(dir2)

    for mm in months.keys():
        t = int(months[mm]) - 1
        print(path2wrf + str(months[mm]) + '/'+ mm + '_24.h5')
        file_24 = h5py.File(path2wrf + str(months[mm]) + '/'+ mm + '_24.h5', 'r')
        vc_24 = np.array(file_24.get('vc_24h'))
        #pblh_24 = np.array(file_24.get('pblh_24h'))
        #u_mean_24 = np.array(file_24.get('u_mean_24h'))

        for i in range(0, 102):
            for j in range(0,128):

                monthly_max[t, i, j] = vc_24[:, hour, i, j].max()
                monthly_min[t, i, j] = vc_24[:, hour, i, j].min()

    for i in range(0, 102):
        for j in range(0,128):

            annual_max[i, j] = monthly_max[:, i, j].max()
            annual_min[i, j] = monthly_min[:, i, j].min()

    #for i in range(0,12):

    #    np.savetxt(dir2 + "/" + str(i+1) + "_max_month.dat", monthly_max[i, :, :], fmt='%.2f')
    #    np.savetxt(dir2 + "/" + str(i+1) + "_min_month.dat", monthly_min[i, :, :], fmt='%.2f')


    np.savetxt(dir2 + "/" + str(hour) + "h_max_annual.dat", annual_max, fmt='%.2f')
    np.savetxt(dir2 + "/" + str(hour) + "h_min_annual.dat", annual_min, fmt='%.2f')

    """
    ############## Ploting ######################
    plt.rcParams.update({'font.size': 13})

    znvm_df = pd.read_csv('../datos/municipios_edomex.csv')

    dir3 = "../graficas/max_min_anual/" + str(hour)
    if os.path.exists(dir3):
        shutil.rmtree(dir3)
    os.makedirs(dir3)
    ### max ###

    plt.figure(figsize = (8.6,8))
    my_map = Basemap(llcrnrlon=-99.5, llcrnrlat=19,urcrnrlon=-98.6, urcrnrlat=19.9)
    my_map.readshapefile('../datos/maps/entidades/INEGI_Municipio_', 'INEGI_Municipio_', drawbounds=False)


    for info, shape in zip(my_map.INEGI_Municipio__info, my_map.INEGI_Municipio_):
        idx_1 = info['NOMBRE'].find(', ') + 2

        if info['NOMBRE'][:6] == 'Ciudad':
            x, y = zip(*shape)
            my_map.plot(x, y, marker=None, c = 'k', linewidth = 1)

        if info['NOMBRE'][idx_1:] in znvm_df.municipios.values:
            x, y = zip(*shape)
            my_map.plot(x, y, marker=None, c = 'k', linewidth =1)


    lons = np.reshape(xlong, 102*128)
    lats = np.reshape(xlat, 102*128)
    x,y = my_map(lons, lats)

    my_map.hexbin(x,y, C = np.reshape(annual_max, 102*128), gridsize=90, alpha = 1, mincnt=1, linewidths=0, cmap='YlOrRd_r')
    plt.title('Anual maximum at ' + str(hour) + ' (GMT-6)')

    my_map.colorbar(location='bottom', label=r'Ventilation Coeficient ($m^2 / s$)')

    plt.savefig(dir3 + '/' + str(hour) + 'h_max', facecolor = (1,0,0,0))

    #### min ####

    plt.figure(figsize = (8.6,8))
    my_map = Basemap(llcrnrlon=-99.5, llcrnrlat=19,urcrnrlon=-98.6, urcrnrlat=19.9)
    my_map.readshapefile('../datos/maps/entidades/INEGI_Municipio_', 'INEGI_Municipio_', drawbounds=False)


    for info, shape in zip(my_map.INEGI_Municipio__info, my_map.INEGI_Municipio_):
        idx_1 = info['NOMBRE'].find(', ') + 2

        if info['NOMBRE'][:6] == 'Ciudad':
            x, y = zip(*shape)
            my_map.plot(x, y, marker=None, c = 'k', linewidth = 1)

        if info['NOMBRE'][idx_1:] in znvm_df.municipios.values:
            x, y = zip(*shape)
            my_map.plot(x, y, marker=None, c = 'k', linewidth =1)


    lons = np.reshape(xlong, 102*128)
    lats = np.reshape(xlat, 102*128)
    x,y = my_map(lons, lats)

    my_map.hexbin(x,y, C = np.reshape(annual_min, 102*128), gridsize=90, alpha = 1, mincnt=1, linewidths=0)
    plt.title('Anual minimum at ' + str(hour) + ' (GMT-6)')

    my_map.colorbar(location='bottom', label=r'Ventilation Coeficient ($m^2 / s$)')
    plt.savefig(dir3 + '/' + str(hour) + 'h_min', facecolor = (1,0,0,0))
"""
print('***DONE***')
