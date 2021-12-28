import importlib.util
spec=importlib.util.spec_from_file_location("BoundaryLayerToolbox","/Users/claudiopierard/VC/BoundaryLayerToolbox.py")
blt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blt)
import numpy as np
import pandas as pd
import scipy as spy
import scipy.io as sio
import matplotlib
import matplotlib.pyplot as plt
import scipy.optimize as optimization
from scipy.stats import stats
import datetime
import sys
import os

ceilo_color = '#F0F8FF'
h48_color = '#FBC0C0'
h24_color = '#defec8'

path2promedios = "/Users/claudiopierard/VC/datos/promedios/"
path2graficas = "/Users/claudiopierard/VC/graficas/"
path2DataFrames = "/Users/claudiopierard/VC/datos/dataframes/"
path2VC = "/Users/claudiopierard/VC/datos/VC/"
months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct':'10', 'nov':'11', 'dic': '12'}

keys_24 = ['PBLH_24']
keys_48 = ['PBLH_48']
keys_ceilo = ['Raw', 'Raw_mean']

print('***START***')
sys.argv.pop(0) #Elimina el nombre del script de la lista de argumentos
location = sys.argv.pop(0)

for mm in sys.argv: #La lista de argumentos contiene los nombres de los archivos a convertir. Para todos los archivos has esto:
    print('\U0001F914', ' Graficando gunshot plots', mm)
    # **Extraer datos**

    month_df = pd.read_csv(path2DataFrames + location + '/' + mm + "_dataframe_"+ location + ".csv", index_col=0)
    month_df.index = pd.to_datetime(month_df.index)

    path2gunshot = path2graficas + location + '/' + mm + '/'

    #RAW vs keys()

    ajuste_params = {'slope': [], 'intercept': [], 'r_value': [],  'plot_name': [], 'month_numb': []}

    for key in keys_24:
        for ceilo in keys_ceilo:
            df_temp = pd.DataFrame(month_df, columns=[ceilo, key])
            #fig, ax = plt.subplots(1,1)
            #fig.set_size_inches(7,6)

            # datos
            x = df_temp[ceilo]  #dic_df.asfreq('1H').between_time('06:00:00', '23:00:00').Raw
            y = df_temp[key]  #dic_VC_df.between_time('06:00:00', '23:00:00')[key]
            tag = (df_temp.index.hour)#dic_VC_df.between_time('06:00:00', '23:00:00').index.hour

            ##Ajuste lineal
            #popt, pcov = optimization.curve_fit(blt.ajuste_lineal, df_temp.dropna()[ceilo], df_temp.dropna()[key])
            slope, intercept, r_value, p_value, std_err = stats.linregress(df_temp.dropna()[ceilo], df_temp.dropna()[key])

            # define the colormap
            cmap = plt.cm.rainbow #matplotlib.colors.ListedColormap(['black','yellow', 'red', 'blue', 'white', 'green'])
            # extract all colors from the .rainbow map
            cmaplist = [cmap(i) for i in range(cmap.N)]
            # create the new map
            cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
            # define the bins and normalize
            bounds = np.linspace(0,24, 9)
            norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

            # make the scatter
            plt.rcParams["font.family"] = "Times New Roman"
            plt.rcParams.update({'font.size': 14})
            """
            plt.figure(figsize = (7,6))
            scat = plt.scatter(x,y, cmap=cmap, norm=norm, c=tag, edgecolors='none', s = 35)

            #Format
            plt.ylim(-100, 3500)
            plt.xlim(-100, 3500)
            plt.xlabel('LIDAR (m)')
            plt.ylabel('PBLH 24h (m)')
            xx = np.linspace(-100, 3500, 10)

            #plt.plot(xx, blt.ajuste_lineal(xx, *popt), c = 'k') #plot linear fit
            plt.plot(xx, blt.ajuste_lineal(xx, intercept, slope), c = 'k') #plot linear fit

            plt.text(.1, 1.8, '$R^2$ = $u$', fontsize=12)

            plt.plot(xx, blt.ajuste_lineal(xx, 0, 1), '--') #Plot identity
            plt.rcParams.update({'font.size': 14})
            #plt.title('UTC-6')
            plt.grid()
            plt.colorbar()
            #plt.tight_layout()
            plt.savefig(path2gunshot + 'GSP_' + mm + '_' + ceilo + '_' + key, facecolor=(1,1,1,0))
            """

            fig = plt.figure(figsize = (6.9,6))
            ax = fig.add_subplot(111)
            im = scat = plt.scatter(x,y, cmap=cmap, norm=norm, c=tag, edgecolors='none', s = 35)

            #Format
            xx = np.linspace(-100, 3500, 10)

            #plt.plot(xx, blt.ajuste_lineal(xx, *popt), c = 'k') #plot linear fit
            ax.plot(xx, blt.ajuste_lineal(xx, intercept, slope), c = 'k') #plot linear fit

            ax.plot(xx, blt.ajuste_lineal(xx, 0, 1), '--') #Plot identity

            #plt.title('UTC-6')
            ax.grid()
            fig.subplots_adjust(right=0.83)
            cbar_ax = fig.add_axes([0.85, 0.13, 0.03, 0.76])
            fig.colorbar(im, cax=cbar_ax)

            #'$R^2$ = $' + str(rr)+ '$'
            ax.text(x = 30, y = 3200, s = '$R$ = $' + str(r_value)[:7]+ '$', fontsize=12)

            ax.set_ylim(-100, 3500)
            ax.set_xlim(-100, 3500)
            ax.set_xlabel('LIDAR (m)')
            ax.set_ylabel('PBLH 24h (m)')

            #plt.tight_layout()
            plt.savefig(path2gunshot + 'GSP_' + mm + '_' + ceilo + '_' + key, facecolor=(1,1,1,0), dpi = 100)

            #Guardar parametros de ajuste
            ajuste_params['plot_name'].append('GSP_' + mm + '_' + ceilo + '_' + key)
            print('- plot_name: ', 'GSP_' + mm + '_' + ceilo + '_' + key)
            ajuste_params['slope'].append(slope)
            print('-- slope: ', slope)
            ajuste_params['intercept'].append(intercept)
            print('-- intercept: ', intercept)
            ajuste_params['r_value'].append(r_value)
            print('-- r_value: ', r_value)
            ajuste_params['month_numb'].append(int(months[mm]))
            print('-- month_numb: ', int(months[mm]))
            print()
            #ajuste_params['std_err'].append(std_err)

    for key in keys_48:
        for ceilo in keys_ceilo:
            df_temp = pd.DataFrame(month_df, columns=[ceilo, key])
            #fig, ax = plt.subplots(1,1)
            #fig.set_size_inches(7,6)

            # datos
            x = df_temp[ceilo]  #dic_df.asfreq('1H').between_time('06:00:00', '23:00:00').Raw
            y = df_temp[key]  #dic_VC_df.between_time('06:00:00', '23:00:00')[key]
            tag = (df_temp.index.hour)#dic_VC_df.between_time('06:00:00', '23:00:00').index.hour

            ##Ajuste lineal
            #popt, pcov = optimization.curve_fit(blt.ajuste_lineal, df_temp.dropna()[ceilo], df_temp.dropna()[key])
            slope, intercept, r_value, p_value, std_err = stats.linregress(df_temp.dropna()[ceilo], df_temp.dropna()[key])

            # define the colormap
            cmap = plt.cm.rainbow #matplotlib.colors.ListedColormap(['black','yellow', 'red', 'blue', 'white', 'green'])
            # extract all colors from the .rainbow map
            cmaplist = [cmap(i) for i in range(cmap.N)]
            # create the new map
            cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
            # define the bins and normalize
            bounds = np.linspace(0,24, 9)
            norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

            """
            # make the scatter
            plt.figure(figsize = (7,6))
            scat = plt.scatter(x,y, cmap=cmap, norm=norm, c=tag, edgecolors='none', s = 35)

            # create a second axes for the colorbar
            #ax2 = plt.add_axes([0.95, 0.1, 0.03, 0.8])
            #cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')

            #Format
            plt.ylim(-100, 3500)
            plt.xlim(-100, 3500)
            plt.xlabel('LIDAR (m)')
            plt.ylabel('PBLH 48h (m)')
            xx = np.linspace(-100, 3500, 10)

            #plt.plot(xx, blt.ajuste_lineal(xx, *popt), c = 'k') #plot linear fit
            plt.plot(xx, blt.ajuste_lineal(xx, intercept, slope), c = 'k') #plot linear fit

            plt.plot(xx, blt.ajuste_lineal(xx, 0, 1), '--') #Plot identity
            plt.rcParams.update({'font.size': 14})
            #plt.title('UTC-6')
            plt.grid()
            plt.colorbar()
            #plt.tight_layout()
            plt.savefig(path2gunshot +  'GSP_' + mm + '_' + ceilo + '_' + key , facecolor=(1,1,1,0))
            """

            fig = plt.figure(figsize = (6.9,6))
            ax = fig.add_subplot(111)
            im = scat = plt.scatter(x,y, cmap=cmap, norm=norm, c=tag, edgecolors='none', s = 35)

            #Format
            xx = np.linspace(-100, 3500, 10)

            #plt.plot(xx, blt.ajuste_lineal(xx, *popt), c = 'k') #plot linear fit
            ax.plot(xx, blt.ajuste_lineal(xx, intercept, slope), c = 'k') #plot linear fit

            ax.plot(xx, blt.ajuste_lineal(xx, 0, 1), '--') #Plot identity

            #plt.title('UTC-6')
            ax.grid()
            fig.subplots_adjust(right=0.83)
            cbar_ax = fig.add_axes([0.85, 0.13, 0.03, 0.76])
            fig.colorbar(im, cax=cbar_ax)

            #'$R^2$ = $' + str(rr)+ '$'
            ax.text(x = 30, y = 3200, s = '$R$ = $' + str(r_value)[:7]+ '$', fontsize=12)

            ax.set_ylim(-100, 3500)
            ax.set_xlim(-100, 3500)
            ax.set_xlabel('LIDAR (m)')
            ax.set_ylabel('PBLH 24h (m)')

            #plt.tight_layout()
            plt.savefig(path2gunshot + 'GSP_' + mm + '_' + ceilo + '_' + key, facecolor=(1,1,1,0), dpi = 100)

            ajuste_params['plot_name'].append('GSP_' + mm + '_' + ceilo + '_' + key)
            print('- plot_name: ','GSP_' + mm + '_' + ceilo + '_' + key)
            ajuste_params['slope'].append(slope)
            print('-- slope: ', slope)
            ajuste_params['intercept'].append(intercept)
            print('-- intercept: ', intercept)
            ajuste_params['r_value'].append(r_value)
            print('-- r_value: ', r_value)
            ajuste_params['month_numb'].append(int(months[mm]))
            print('-- month_numb: ', int(months[mm]))
            print()

    aju_param_df = pd.DataFrame(ajuste_params)
    aju_param_df.to_csv(path2gunshot + 'parametros_ajustes_gunshotplots_' + mm + '_' + location + '.csv', float_format='%.4f')

print('***DONE***')
