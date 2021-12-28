#import importlib.util
#spec = importlib.util.spec_from_file_location("BoundaryLayerToolbox", "/Users/claudiopierard/VC/BoundaryLayerToolbox.py")
#blt = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(blt)
import matplotlib
import numpy as np
#import h5py
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

import scipy as spy
import scipy.io as sio
import scipy.optimize as optimization
import scipy.interpolate as interpolate
#from netCDF4 import Dataset
import os
import pandas as pd
#pd.set_option('html', False)
#from IPython import display

#matplotlib
#from matplotlib import animation
import matplotlib.colors as colors
#from mpl_toolkits.axes_grid1 import make_axes_locatable
#%matplotlib inline
#from mpl_toolkits.axes_grid1 import host_subplot
#import mpl_toolkits.axisartist as AA
#import datetime
import matplotlib.mlab as mlab
#from scipy.stats import stats

xlat = np.loadtxt("/Users/claudiopierard/VC/datos/xlat_d02_interpolado.txt")
xlong = np.loadtxt("/Users/claudiopierard/VC/datos/xlong_d02_interpolado.txt")
hgt = np.loadtxt("/Users/claudiopierard/VC/datos/hgt_d02_interpolado.txt")
#months = {1:'jun', 2:'feb', 3:'mar',4: 'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dic'}
path2datosVC = "../datos/dataframes_VC_contaminantes/cca/"
path2pollutants = "../datos/contaminantes/2015/CCA/"

path2estaciones = "../datos/loc_estaciones/air_quality_stn.xy"
estaciones = pd.read_table(path2estaciones, index_col=0, names=['long','lat', 'height'])
estaciones = estaciones.transpose().to_dict()
estaciones['CCA']

months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct':'10', 'nov':'11', 'dic': '12'}

apr = pd.read_csv(path2datosVC + 'apr_vc_contaminantes_cca.csv', index_col=0)

xmin, xmax = apr['pblh_24'].min(), apr['pblh_24'].max()
ymin, ymax = apr['u_mean_24'].min(), apr['u_mean_24'].max()

ny, nx = 512, 512
xi = np.linspace(xmin, xmax, nx)
yi = np.linspace(ymin, ymax, ny)
xi, yi = np.meshgrid(xi, yi)

x = apr.dropna(subset=['pblh_24', 'o3'])['pblh_24']
y = apr.dropna(subset=['pblh_24', 'o3'])['u_mean_24']
z = apr.dropna(subset=['pblh_24', 'o3'])['o3']

zi = mlab.griddata(x,y,z,xi,yi)

fig = plt.figure(figsize = (6,6))

ax = fig.add_subplot(111)

im = ax.pcolormesh(xi,yi,zi)
im = ax.scatter(apr['pblh_24'], apr['u_mean_24'], c = apr['o3'], s = 10)
#ax.plot(x_range, f(x_range), '--k')

cbar_ax = fig.add_axes([0.95, 0.13, 0.03, 0.76])
cc = fig.colorbar(im, cax=cbar_ax)
ax.set_ylabel('<U> ($m/s$)')
cc.set_label('Ozono (ppb)')
ax.set_xlabel('PBLH ($m$)')
ax.set_ylim(-0.4, 10)
ax.set_xlim(-100, 3500)
plt.savefig('prueba', facecolor=(1,1,1,0), dpi = 100)
