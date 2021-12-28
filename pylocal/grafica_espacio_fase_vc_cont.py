#Loading modules
import BoundaryLayerToolbox as blt #my package
import numpy as np
import pandas as pd
import scipy as spy
import scipy.io as sio
import matplotlib
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import matplotlib.mlab as mlab
import matplotlib.colors as colors

from scipy.stats import stats
import datetime
import sys
import os

#only MER
path2datosVC = "../datos/dataframes_VC/MER/"
path2graficas = "../graficas/espacio_fase/"

contaminantes = {'o3': 'O$_3$ (ppb)', 'pm25': 'PM$_{2.5}$ ($\mu g /m^3$)', 'co': 'CO (ppm)'}

months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct':'10', 'nov':'11', 'dic': '12'}

cont_mar = [[pd.to_datetime('2015-03-03 16:00:00'), pd.to_datetime('2015-03-04 00:00:00')]]
cont_apr = [[pd.to_datetime('2015-04-08 16:00:00'), pd.to_datetime('2015-04-10 18:00:00')]]

cont_may = [[pd.to_datetime('2015-05-05 16:00:00'), pd.to_datetime('2015-05-06 18:00:00')], [pd.to_datetime('2015-05-09 16:00:00'), pd.to_datetime('2015-05-10 18:00:00')]]

cont_jun = [[pd.to_datetime('2015-06-10 16:00:00'), pd.to_datetime('2015-06-13 15:00:00')]]
cont_oct = [[pd.to_datetime('2015-10-04 15:00:00'), pd.to_datetime('2015-10-05 18:00:00')]]
#cont_dic = [[pd.to_datetime('2015-12-25 00:00:00'), pd.to_datetime('2015-12-26 00:00:00')]]

contingencia = {'jan': 'NO', 'feb': 'NO', 'mar': cont_mar, 'apr': cont_apr, 'may': cont_may, 'jun': cont_jun, 'jul': 'NO', 'aug': 'NO', 'sep': 'NO', 'oct': cont_oct, 'nov':'NO', 'dic' : 'NO'}


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 14})

print('***START***')
#sys.argv.pop(0) #Elimina el nombre del script de la lista de argumentos
location = sys.argv.pop(0)

for mm in sys.argv:#La lista de argumentos contiene los nombres de los archivos a convertir. Para todos los archivos has esto:

    print(mm)
    #os.makedirs(path2graficas + mm)

    print('\U0001F914', ' Graficando diagramas espacio fase de ', mm)
    # **Extraer datos**

    month_df = pd.read_csv(path2datosVC +mm+'_vc_contaminantes_cca.csv', index_col=0)
    month_df.index = pd.to_datetime(month_df.index)

    xmin, xmax = month_df['pblh_24'].min(), month_df['pblh_24'].max()
    ymin, ymax = month_df['u_mean_24'].min(), month_df['u_mean_24'].max()

    ny, nx = 512, 512

    xi = np.linspace(xmin, xmax, nx)
    yi = np.linspace(ymin, ymax, ny)
    xi, yi = np.meshgrid(xi, yi)

    VC_grid = xi*yi

    for pollutant in contaminantes.keys():

        x = month_df.dropna(subset=['pblh_24', pollutant])['pblh_24']
        y = month_df.dropna(subset=['pblh_24', pollutant])['u_mean_24']
        z = month_df.dropna(subset=['pblh_24', pollutant])[pollutant]

        #zi = spy.interpolate.griddata([x,y],z,[xi,yi], method='nearest')
        zi = mlab.griddata(x,y,z,xi,yi, interp='linear')

        ################ GRAFICANDO ###################

        fig = plt.figure(figsize = (6.9,6))
        ax = fig.add_subplot(111)
        im = ax.pcolormesh(xi,yi,zi, cmap = 'rainbow') # norm= colors.PowerNorm(gamma=1)
        #ax.contourf(xi,yi,zi)
        vc_levels = [1000, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000]
        vc_levels_colors = ['k','k','k','r','k','k','k','k','k','k']
        vc_levels_linestyle = ['solid','solid','solid','dashed','solid','solid','solid','solid','solid','solid']
        vc_levels_linewidth = [1,1,1,2.3,1,1,1,1,1,1]
        ax.scatter(x, y, s = 15, marker = 'x', color = 'k')

        if contingencia[mm] != 'NO' and pollutant == 'o3':
            for dates in contingencia[mm]:
                ax.scatter(month_df[dates[0]:dates[1]]['pblh_24'], month_df[dates[0]:dates[1]]['u_mean_24'], s = 80, c = month_df[dates[0]:dates[1]]['o3'], marker = 'o')

        if mm == 'dic' and pollutant == 'pm25':
            for dates in [[pd.to_datetime('2015-12-25 00:00:00'), pd.to_datetime('2015-12-26 00:00:00')]]:
                ax.scatter(month_df[dates[0]:dates[1]]['pblh_24'], month_df[dates[0]:dates[1]]['u_mean_24'], s = 80, c = month_df[dates[0]:dates[1]]['pm25'], marker = 'o')

        ax.axhline(4, -100, 3500, c = 'r', linestyle = 'dashed', linewidth = 2.3)
        #ax.plot(x_range, f(x_range), '--k')
        CS = ax.contour(xi,yi,VC_grid, colors=vc_levels_colors, levels=vc_levels, linestyles = vc_levels_linestyle, linewidths = vc_levels_linewidth)
        ax.clabel(CS, fontsize=9, inline=1, fmt = '%1.0f')
        ax.text(xmax-xmax/10, ymax - ymax/21, mm.upper(), fontsize = 14)

        cbar_ax = fig.add_axes([0.85, 0.13, 0.03, 0.76])
        cc = fig.colorbar(im, cax=cbar_ax)
        ax.set_ylabel('<U> ($m/s$)')
        cc.set_label(contaminantes[pollutant])
        ax.set_xlabel('PBLH ($m$)')
        ax.set_ylim(-0.4, ymax + 0.4)
        ax.set_xlim(-100, xmax + 100)
        #plt.tight_layout()
        plt.subplots_adjust(right=0.8)

        fig.savefig(path2graficas + mm + '/' + mm + '_espacio_fase_' + pollutant, facecolor=(1,1,1,0), dpi = 100)



print('***DONE***')
