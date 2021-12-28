import importlib.util
spec = importlib.util.spec_from_file_location("BoundaryLayerToolbox", "/Users/claudiopierard/VC/BoundaryLayerToolbox.py")
blt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blt)
import matplotlib
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy as spy

import os
import sys
import pandas as pd
import datetime

import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

xlat = np.loadtxt("/Users/claudiopierard/VC/datos/xlat_d02_interpolado.txt")
xlong = np.loadtxt("/Users/claudiopierard/VC/datos/xlong_d02_interpolado.txt")
hgt = np.loadtxt("/Users/claudiopierard/VC/datos/hgt_d02_interpolado.txt")
months = {1:'jan', 2:'feb', 3:'mar',4: 'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dic'}
path2datosVC = "../datos/dataframes_VC/cca/"
path2pollutants = "../datos/contaminantes/2015/CCA/"
path2graphs = "../graficas/cca/"
months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct':'10', 'nov':'11', 'dic': '12'}


#Importo ubicación de estaciones a un diccionario
path2estaciones = "../datos/loc_estaciones/air_quality_stn.xy"
estaciones = pd.read_table(path2estaciones, index_col=0, names=['long','lat', 'height'])
estaciones = estaciones.transpose().to_dict()

print("*** START ***")

#Importo datos de contaminantes de 2015 en el CCA
o3_2015 = pd.read_csv(path2pollutants + "CCA_o3_2015.csv", index_col=0)
o3_2015.index = pd.to_datetime(o3_2015.index)

pm25_2015 = pd.read_csv(path2pollutants + "CCA_pm25_2015.csv", index_col=0)
pm25_2015.index = pd.to_datetime(pm25_2015.index)

co_2015 = pd.read_csv(path2pollutants + "CCA_co_2015.csv", index_col=0)
co_2015.index = pd.to_datetime(co_2015.index)

#Importo datos de VC de 2015 en el CCA para un mes
sys.argv.pop(0)

for mm in sys.argv:

    print('\U0001F4C8', "Plotting", mm)

    local_path = path2graphs + mm + '/' + 'vc_contaminantes_series/'
    os.makedirs(local_path)

    month_vc = pd.read_csv(path2datosVC + mm + "_dataframe_cca.csv", index_col=0)
    month_vc.index = pd.to_datetime(month_vc.index)

    date_beg = "2015-" + months[mm] + '-01'
    date_end = "2015-" + months[mm] + '-' + blt.E1or30(mm)

    #date_beg:date_end
    ############### THE WEEKEND BANDS #################
    def dayOfWeek_array(datetime_arr):
        y = datetime_arr.year
        m = datetime_arr.month
        d = datetime_arr.day
        t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
        new_m = []
        for i in m:
            new_m.append(t[i-1])
        new_m = np.array(new_m)
        y -= m < 3
        return np.trunc((y + y/4 - y/100 + y/400 + new_m + d) % 7).astype(np.int)

    A = o3_2015[date_beg:date_end].index.date
    B = o3_2015[date_beg:date_end].index.time
    C = dayOfWeek_array(o3_2015[date_beg:date_end].index)

    DF = pd.DataFrame({'date': A, 'time': B, 'week_index': C})
    DF.index = DF.week_index
    DF = DF.drop('week_index', 1)

    sat = DF.loc[6].drop_duplicates(subset = 'date', keep = 'first')
    sun = DF.loc[0].drop_duplicates(subset = 'date', keep = 'last')

    new_sun = []
    new_sat = []

    for i in range(0, len(sun.date.values)):
        dt = datetime.datetime.combine(sun['date'].values[i], sun['time'].values[i])
        new_sun.append(dt)

    for i in range(0, len(sat.date.values)):
        dt = datetime.datetime.combine(sat['date'].values[i], sat['time'].values[i])
        new_sat.append(dt)

    sat = new_sat
    sun = new_sun

    weekend = []

    for j in range(0, len(sun)):
         if sun[j].day == 1:
                weekend.append([sun[j] - datetime.timedelta(hours = 23), sun[j]])

    for i in range(0, len(sat)):
        for j in range(0, len(sun)):

            if sat[i].day == sun[j].day - 1:
                weekend.append([sat[i], sun[j]])

        if sat[i].day == 31:
            weekend.append([sat[i] , sat[i] + datetime.timedelta(hours = 23)])
    #### Contingencias
    # Marzo
    cont_mar = [[pd.to_datetime('2015-03-03 16:00:00'), pd.to_datetime('2015-03-04 00:00:00')]]
    cont_apr = [[pd.to_datetime('2015-04-08 16:00:00'), pd.to_datetime('2015-04-10 18:00:00')]]

    cont_may = [[pd.to_datetime('2015-05-05 16:00:00'), pd.to_datetime('2015-05-06 18:00:00')], [pd.to_datetime('2015-05-09 16:00:00'), pd.to_datetime('2015-05-10 18:00:00')]]

    cont_jun = [[pd.to_datetime('2015-06-10 16:00:00'), pd.to_datetime('2015-06-13 15:00:00')]]
    cont_oct = [[pd.to_datetime('2015-10-04 15:00:00'), pd.to_datetime('2015-10-05 18:00:00')]]
    cont_dic = [[pd.to_datetime('2015-12-25 00:00:00'), pd.to_datetime('2015-12-26 00:00:00')]]

    ############### PLOT O3 ###############
    plt.rcParams["font.family"] = "Times New Roman"

    plt.figure(figsize=[20,5])
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust()
    par1 = host.twinx()

    host.set_ylabel("VC ($m^2/s$)")
    par1.set_ylabel("Ozono (ppb)")

    host.plot(month_vc['VC_24'],  c = 'k', label = 'VC')
    par1.plot(o3_2015[date_beg:date_end]['o3'], c = 'b', label = 'Ozono')

    for wk in weekend:
        host.axvspan(wk[1], wk[0], color='grey', alpha=0.4)

    if mm == 'mar':
        for contin in cont_mar:
            host.axvspan(contin[1], contin[0], color='yellow', alpha=0.4)
    elif mm == 'apr':
        for contin in cont_apr:
            host.axvspan(contin[1], contin[0], color='yellow', alpha=0.4)

    if mm == 'may':
        for contin in cont_may:
            host.axvspan(contin[1], contin[0], color='yellow', alpha=0.4)

    if mm == 'jun':
        for contin in cont_jun:
            host.axvspan(contin[1], contin[0], color='yellow', alpha=0.4)

    if mm == 'oct':
        for contin in cont_oct:
            host.axvspan(contin[1], contin[0], color='yellow', alpha=0.4)

    host.legend(fancybox = True, shadow = True, ncol=2, loc = 'best', fontsize = 13)
    plt.rcParams.update({'font.size': 13})

    minor_axis = pd.date_range(date_beg, date_end, freq='1D')
    host.set_xticks(minor_axis, minor=True)
    host.grid(which='both')

    plt.savefig(local_path + mm + "_vc_vs_o3.png" , facecolor=(1,1,1,0))

    ############### PLOT PM2.5 ###############

    plt.figure(figsize=[20,5])
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust()
    par1 = host.twinx()

    host.set_ylabel("VC ($m^2/s$)")
    par1.set_ylabel("PM 2.5 $(\mu g/m^3)$")

    host.plot(month_vc['VC_24'],  c = 'k', label = 'VC')
    par1.plot(pm25_2015[date_beg:date_end]['pm25'], c = 'r', label = 'PM 2.5')

    for wk in weekend:
        host.axvspan(wk[1], wk[0], color='grey', alpha=0.4)

    if mm == 'dic':
        for contin in cont_dic:
            host.axvspan(contin[1], contin[0], color='yellow', alpha=0.4)

    host.legend(fancybox = True, shadow = True, ncol=2, loc = 'best', fontsize = 13)
    plt.rcParams.update({'font.size': 13})
    plt.rcParams["font.family"] = "Times New Roman"

    minor_axis = pd.date_range(date_beg, date_end, freq='1D')
    host.set_xticks(minor_axis, minor=True)
    host.grid(which='both')

    plt.savefig(local_path + mm + "_vc_vs_pm25.png" , facecolor=(1,1,1,0))

    ############### PLOT CO ###############

    plt.figure(figsize=[20,5])
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust()
    par1 = host.twinx()

    host.set_ylabel("VC ($m^2/s$)")
    par1.set_ylabel("CO (ppm)")

    host.plot(month_vc['VC_24'],  c = 'k', label = 'VC')

    par1.plot(co_2015[date_beg:date_end]['co'], c = 'g', label = 'CO')

    for wk in weekend:
        host.axvspan(wk[1], wk[0], color='grey', alpha=0.4)

    host.legend(fancybox = True, shadow = True, ncol=2, loc = 'best', fontsize = 13)
    plt.rcParams.update({'font.size': 13})
    plt.rcParams["font.family"] = "Times New Roman"

    minor_axis = pd.date_range(date_beg, date_end, freq='1D')
    host.set_xticks(minor_axis, minor=True)
    host.grid(which='both')

    plt.savefig(local_path + mm + "_vc_vs_co.png" , facecolor=(1,1,1,0))

print("*** DONE ***")
