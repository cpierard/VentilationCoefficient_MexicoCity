# Loading modules
import numpy as np
import pandas as pd
import matplotlib
# matplotlib.use("macOSX")
# matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
import scipy.stats as stats
from matplotlib.gridspec import GridSpec
import sys
import os
import shutil

path2datosVC = "../datos/dataframes_VC/"

# plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 13})

for pol in ['O3', 'PM25', 'PM10']:

    dir = "../graficas/" + pol
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

print('***START***')
sys.argv.pop(0)  # Elimina el nombre del script de la lista de argumentos
locations = ['SFE', 'MER', 'PED', 'SAG', 'TLA', 'UIZ']

for loc in locations:

    # print('Processing ', loc)
    print('\U0001F914', ' Graficando diagramas espacio fase de ', loc)
    # **Extraer datos**


    loc_df = pd.read_csv('../datos/dataframes_VC/' + loc + '/vc_' + loc + '.csv', index_col=0)
    loc_df.index = pd.to_datetime(loc_df.index)

    day_loc_df = loc_df.between_time('08:00', '18:00')

    ########### OZONE ##############

    color_1 = 'orangered'
    color_2 = 'royalblue'
    nom_o3 = 95

    h = sorted(day_loc_df.loc[day_loc_df.O3 > 95]['pblh'].dropna())
    j = sorted(day_loc_df.loc[day_loc_df.O3 < 95]['pblh'].dropna())

    fit_h = stats.norm.pdf(h, np.mean(h), np.std(h))
    fit_j = stats.norm.pdf(j, np.mean(j), np.std(j))

    k = sorted(day_loc_df.loc[day_loc_df.O3 > 95]['u_mean'].dropna())
    l = sorted(day_loc_df.loc[day_loc_df.O3 < 95]['u_mean'].dropna())

    fit_k = stats.norm.pdf(k, np.mean(k), np.std(k))
    fit_l = stats.norm.pdf(l, np.mean(l), np.std(l))

    fig = plt.figure(figsize=(8,8))
    gs = GridSpec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4], wspace=0.01, hspace=0.01)

    ax1 = fig.add_subplot(gs[0])
    ax1.hist(day_loc_df.loc[day_loc_df.O3 < 95]['pblh'],density = True, alpha = 0.4, color = color_2, bins = 15)
    ax1.hist(day_loc_df.loc[day_loc_df.O3 > 95]['pblh'],density = True, alpha = 0.4, color = color_1, bins = 15)
    ax1.plot(h,fit_h, c = color_1, linewidth=2)
    ax1.plot(j,fit_j, c = color_2, linewidth=2)
    ax1.set_axis_off()

    ax2 = fig.add_subplot(gs[1])
    ax2.set_axis_off()

    ax3 = fig.add_subplot(gs[2])
    ax3.scatter(day_loc_df.loc[day_loc_df.O3 < nom_o3]['pblh'], day_loc_df.loc[day_loc_df.O3 < nom_o3]['u_mean'],
                c = color_2, alpha = 0.7, label = "Ozone < 95 ppm", s = 10)
    ax3.scatter(day_loc_df.loc[day_loc_df.O3 > nom_o3]['pblh'], day_loc_df.loc[day_loc_df.O3 > nom_o3]['u_mean'],
                c = color_1, alpha = 0.7, label = "Ozone > 95 ppm", s = 10)
    ax3.set_xlabel(r'PBLH ($m$)', fontsize = 13)
    ax3.set_ylabel(r'Mean wind velocity ($m \ s^{-1}$)', fontsize = 13)
    ax3.set_xlim(-100,3900)
    ax3.set_ylim(-0.5,14.5)
    ax3.legend()
    ax3.text(0.91, 0.02, loc, transform=ax3.transAxes)
    ax3.grid(linestyle='--')

    ax4 = fig.add_subplot(gs[3])
    ax4.hist(day_loc_df.loc[day_loc_df.O3 < 95]['u_mean'],density = True, alpha = 0.4, color = color_2, bins = 20,
             orientation = "horizontal")
    ax4.hist(day_loc_df.loc[day_loc_df.O3 > 95]['u_mean'],density = True, alpha = 0.4, color = color_1, bins = 20,
            orientation = "horizontal")
    ax4.plot(fit_k, k, c = color_1, linewidth=2)
    ax4.plot(fit_l, l, c = color_2, linewidth=2)
    ax4.set_axis_off()
        #fig.savefig(path2graficas + mm + '/' + mm + '_espacio_fase_' + pollutant, facecolor=(1,1,1,0), dpi = 100)
    plt.savefig('../graficas/O3/' + loc + '_O3_distribuciones', facecolor = (1,0,0,0))
    plt.close()

    ############# PM2.5 ##################

    color_1 = 'goldenrod'
    color_2 = 'steelblue'
    nom_pm25 = 45

    h = sorted(day_loc_df.loc[day_loc_df['PM2.5'] > nom_pm25]['pblh'].dropna())
    j = sorted(day_loc_df.loc[day_loc_df['PM2.5'] < nom_pm25]['pblh'].dropna())

    fit_h = stats.norm.pdf(h, np.mean(h), np.std(h))
    fit_j = stats.norm.pdf(j, np.mean(j), np.std(j))

    k = sorted(day_loc_df.loc[day_loc_df['PM2.5'] > nom_pm25]['u_mean'].dropna())
    l = sorted(day_loc_df.loc[day_loc_df['PM2.5'] < nom_pm25]['u_mean'].dropna())

    fit_k = stats.norm.pdf(k, np.mean(k), np.std(k))
    fit_l = stats.norm.pdf(l, np.mean(l), np.std(l))

    fig = plt.figure(figsize=(8,8))
    gs = GridSpec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4], wspace=0.01, hspace=0.01)

    ax1 = fig.add_subplot(gs[0])
    ax1.hist(day_loc_df.loc[day_loc_df['PM2.5'] < nom_pm25]['pblh'],density = True, alpha = 0.4, color = color_2, bins = 15)
    ax1.hist(day_loc_df.loc[day_loc_df['PM2.5'] > nom_pm25]['pblh'],density = True, alpha = 0.4, color = color_1, bins = 15)
    ax1.plot(h,fit_h, c = color_1, linewidth=2)
    ax1.plot(j,fit_j, c = color_2, linewidth=2)
    ax1.set_axis_off()

    ax2 = fig.add_subplot(gs[1])
    ax2.set_axis_off()

    ax3 = fig.add_subplot(gs[2])
    #CS = ax3.contour(xi,yi,VC_grid, colors='k', levels=[3000, 6000, 9000, 12000, 15000, 18000, 21000, 24000],alpha = 0.7)
    #ax3.clabel(CS, fontsize=9, inline=1, fmt = '%1.0f')
    ax3.scatter(day_loc_df.loc[day_loc_df['PM2.5'] < nom_pm25]['pblh'], day_loc_df.loc[day_loc_df['PM2.5'] < nom_pm25]['u_mean'],
                c = color_2, alpha = 0.7, label = r"PM2.5 < 45 $\mu g \ m^{-3}$", s = 10)
    ax3.scatter(day_loc_df.loc[day_loc_df['PM2.5'] > nom_pm25]['pblh'], day_loc_df.loc[day_loc_df['PM2.5'] > nom_pm25]['u_mean'],
                c = color_1, alpha = 0.7, label = r"PM2.5 > 45 $\mu g \ m^{-3}$", s = 10)
    ax3.set_xlabel(r'PBLH ($m$)', fontsize = 13)
    ax3.set_ylabel(r'Mean wind velocity ($m \ s^{-1}$)', fontsize = 13)
    ax3.set_xlim(-100,3900)
    ax3.set_ylim(-0.5,14.5)
    ax3.legend()
    ax3.text(0.91, 0.02, loc, transform=ax3.transAxes)
    ax3.grid(linestyle='--')

    ax4 = fig.add_subplot(gs[3])
    ax4.hist(day_loc_df.loc[day_loc_df['PM2.5'] < nom_pm25]['u_mean'],density = True, alpha = 0.4, color = color_2, bins = 20,
             orientation = "horizontal")
    ax4.hist(day_loc_df.loc[day_loc_df['PM2.5'] > nom_pm25]['u_mean'],density = True, alpha = 0.4, color = color_1, bins = 20,
            orientation = "horizontal")
    ax4.plot(fit_k, k, c = color_1, linewidth=2)
    ax4.plot(fit_l, l, c = color_2, linewidth=2)
    ax4.set_axis_off()
    plt.savefig('../graficas/PM25/' + loc + '_PM25_distribuciones', facecolor = (1,0,0,0))
    plt.close()

    ############## PM10 ###############

    color_1 = 'darkorange'
    color_2 = 'royalblue'
    nom_pm10 = 75

    h = sorted(day_loc_df.loc[day_loc_df['PM10'] > nom_pm10]['pblh'].dropna())
    j = sorted(day_loc_df.loc[day_loc_df['PM10'] < nom_pm10]['pblh'].dropna())

    fit_h = stats.norm.pdf(h, np.mean(h), np.std(h))
    fit_j = stats.norm.pdf(j, np.mean(j), np.std(j))

    k = sorted(day_loc_df.loc[day_loc_df['PM10'] > nom_pm10]['u_mean'].dropna())
    l = sorted(day_loc_df.loc[day_loc_df['PM10'] < nom_pm10]['u_mean'].dropna())

    fit_k = stats.norm.pdf(k, np.mean(k), np.std(k))
    fit_l = stats.norm.pdf(l, np.mean(l), np.std(l))

    fig = plt.figure(figsize=(8,8))
    gs = GridSpec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4], wspace=0.01, hspace=0.01)

    ax1 = fig.add_subplot(gs[0])
    ax1.hist(day_loc_df.loc[day_loc_df['PM10'] < nom_pm10]['pblh'],density = True, alpha = 0.4, color = color_2, bins = 15)
    ax1.hist(day_loc_df.loc[day_loc_df['PM10'] > nom_pm10]['pblh'],density = True, alpha = 0.4, color = color_1, bins = 15)
    ax1.plot(h,fit_h, c = color_1, linewidth=2)
    ax1.plot(j,fit_j, c = color_2, linewidth=2)
    ax1.set_axis_off()

    ax2 = fig.add_subplot(gs[1])
    ax2.set_axis_off()

    ax3 = fig.add_subplot(gs[2])
    #CS = ax3.contour(xi,yi,VC_grid, colors='k', levels=[3000, 6000, 9000, 12000, 15000, 18000, 21000, 24000],alpha = 0.7)
    #ax3.clabel(CS, fontsize=9, inline=1, fmt = '%1.0f')
    ax3.scatter(day_loc_df.loc[day_loc_df['PM10'] < nom_pm10]['pblh'], day_loc_df.loc[day_loc_df['PM10'] < nom_pm10]['u_mean'],
                c = color_2, alpha = 0.7, label = "PM10 < 75 $\mu g \ m^{-3}$", s = 10)
    ax3.scatter(day_loc_df.loc[day_loc_df['PM10'] > nom_pm10]['pblh'], day_loc_df.loc[day_loc_df['PM10'] > nom_pm10]['u_mean'],
                c = color_1, alpha = 0.7, label = "PM10 > 75 $\mu g \ m^{-3}$", s = 10)
    ax3.set_xlabel(r'PBLH ($m$)', fontsize = 13)
    ax3.set_ylabel(r'Mean wind velocity ($m \ s^{-1}$)', fontsize = 13)
    ax3.set_xlim(-100,3900)
    ax3.set_ylim(-0.5,14.5)
    ax3.legend()
    ax3.text(0.91, 0.02, loc, transform=ax3.transAxes)
    ax3.grid(linestyle='--')

    ax4 = fig.add_subplot(gs[3])
    ax4.hist(day_loc_df.loc[day_loc_df['PM10'] < nom_pm10]['u_mean'],density = True, alpha = 0.4, color = color_2, bins = 20,
             orientation = "horizontal")
    ax4.hist(day_loc_df.loc[day_loc_df['PM10'] > nom_pm10]['u_mean'],density = True, alpha = 0.4, color = color_1, bins = 20,
            orientation = "horizontal")
    ax4.plot(fit_k, k, c = color_1, linewidth=2)
    ax4.plot(fit_l, l, c = color_2, linewidth=2)
    ax4.set_axis_off()
    plt.savefig('../graficas/PM10/' + loc + '_PM10_distribuciones', facecolor = (1,0,0,0))
    plt.close()

print('***DONE***')
