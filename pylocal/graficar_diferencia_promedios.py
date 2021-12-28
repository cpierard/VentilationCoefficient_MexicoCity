## Para correr hay que especifiar la estación 'cca' o 'jqro', seguido de los meses para genera los promedios.

import importlib.util
spec=importlib.util.spec_from_file_location("BoundaryLayerToolbox","/Users/claudiopierard/VC/BoundaryLayerToolbox.py")
blt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blt)
import numpy as np
import scipy as spy
import scipy.io as sio
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import datetime
import sys
import os

ceilo_color = '#F0F8FF'
h48_color = '#FBC0C0'
h24_color = '#defec8'

path2promedios = "/Users/claudiopierard/VC/datos/promedios/"
path2graficas = "/Users/claudiopierard/VC/graficas/"
#path2wrf = "/Users/claudiopierard/WRF/Datos/WRF/"
months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct':'10', 'nov':'11', 'dic': '12'}

print('***START***')
sys.argv.pop(0) #Elimina el nombre del script de la lista de argumentos
location = sys.argv.pop(0)

for mm in sys.argv: #La lista de argumentos contiene los nombres de los archivos a convertir. Para todos los archivos has esto:

    print('Graficando', mm)
    # **Extraer datos**
    month_avg = np.loadtxt(path2promedios + location +'/'+ mm + "_promedios_" + location + ".dat")
    path_month_graficas = path2graficas + location + '/' + mm + '/'
    #os.makedirs(path_month_graficas)

    plt.rcParams.update({'font.size': 13}) #Tamaño letra
    plt.rcParams["font.family"] = "Times New Roman"

    ##################### 24h #######################
    #################################################

    #os.makedirs(path_month_graficas + '24h')

    ## Gráfica de ceilo en cada hora  y PBLH_24

    h_range= range(0,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #plt.fill_between(h_range, month_avg[:,0] - month_avg[:,1], month_avg[:,0] + month_avg[:,1], facecolor='#F0F8FF', alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,0] - month_avg[:,4], label = 'Diferencia')
    #plt.fill_between(h_range, month_avg[:,4] - month_avg[:,5], month_avg[:,4] + month_avg[:,5], facecolor= h24_color, alpha=1.0, edgecolor='none')
    #plt.plot(h_range, month_avg[:,4], c = 'g', label='PBLH 24h')
    plt.ylabel('Diferencia entre LIDAR y PBLH (m)')
    plt.xlabel('Hora (UTC-6)')
    plt.grid()
    plt.xlim((0,24))
    plt.ylim((0,2000))
    plt.xticks(range(0,25,4))
    plt.legend(loc=(0.05,0.83), fancybox = True, shadow = True, fontsize = 13)

    plt.savefig(path_month_graficas + 'DIF_' + mm + '_Raw_PBLH_24_' + location, facecolor=(1,1,1,0))

    ## Gráfica de ceilo en pormediado en el intervalo  y PBLH_24

    h_range= range(0,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #plt.fill_between(h_range, month_avg[:,2] - month_avg[:,3], month_avg[:,2] + month_avg[:,3], facecolor='#F0F8FF', alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,2] - month_avg[:,4], label = 'Diferencia')
    #plt.fill_between(h_range, month_avg[:,4] - month_avg[:,5], month_avg[:,4] + month_avg[:,5], facecolor= h24_color, alpha=1.0, edgecolor='none')
    #plt.plot(h_range, month_avg[:,4], c = 'g', label='PBLH 24h')
    plt.ylabel('Diferencia entre LIDAR y PBLH (m)')
    plt.xlabel('Hora (UTC-6)')
    plt.legend(loc=(0.05,0.83), fancybox = True, shadow = True, fontsize = 13)
    plt.grid()
    plt.xlim((0,24))
    plt.ylim((0,2000))
    plt.xticks(range(0,25,4))
    plt.savefig(path_month_graficas + 'DIF_' + mm + '_Raw_mean_PBLH_24_'+location, edgecolor='w', facecolor=(1,1,1,0))

    ###################### 48 h #########################
    #####################################################

    #os.makedirs(path_month_graficas + '48h')
    ## ceilo promedio en hora y pblh en 1 coord.

    h_range= range(0,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #ceilo
    #plt.fill_between(h_range, month_avg[:,0] - month_avg[:,1], month_avg[:,0] + month_avg[:,1], facecolor=ceilo_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,0] - month_avg[:,6], label = 'Diferencia')
    #48h
    #plt.fill_between(h_range, month_avg[:,6] - month_avg[:,7], month_avg[:,6] + month_avg[:,7], facecolor=h48_color, alpha=1.0, edgecolor='none')
    #plt.plot(h_range, month_avg[:,6], c = 'r', label='PBLH 48h')
    plt.ylabel('Diferencia entre LIDAR y PBLH (m)')
    plt.xlabel('Hora (UTC-6)')
    plt.legend(loc=(0.05,0.83), fancybox = True, shadow = True, fontsize = 13)
    plt.grid()
    plt.xlim((0,24))
    plt.ylim((0,2000))
    plt.xticks(range(0,25,4))
    plt.savefig(path_month_graficas + 'DIF_' + mm + '_Raw_PBLH_48_' + location, facecolor=(1,1,1,0))

    ## ceilo promedio en intervalo de tiempo y pblh en 1 coord.

    h_range= range(0,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #ceilo
    #plt.fill_between(h_range, month_avg[:,2] - month_avg[:,3], month_avg[:,2] + month_avg[:,3], facecolor=ceilo_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,2] - month_avg[:,6], label = 'Diferencia')
    #48h
    #plt.fill_between(h_range, month_avg[:,6] - month_avg[:,7], month_avg[:,6] + month_avg[:,7], facecolor=h48_color, alpha=1.0, edgecolor='none')
    #plt.plot(h_range, month_avg[:,6], c = 'r', label='PBLH 48h')
    plt.ylabel('Diferencia entre LIDAR y PBLH (m)')
    plt.xlabel('Hora (UTC-6)')
    plt.legend(loc=(0.05,0.83), fancybox = True, shadow = True, fontsize = 13)
    plt.grid()
    plt.xlim((0,24))
    plt.ylim((0,2000))
    plt.xticks(range(0,25,4))
    plt.savefig(path_month_graficas + 'DIF_' + mm + '_Raw_mean_PBLH_48_' + location, facecolor=(1,1,1,0))

print('***DONE***')
