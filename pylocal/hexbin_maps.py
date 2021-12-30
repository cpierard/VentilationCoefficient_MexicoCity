import numpy as np
import os
import matplotlib.pyplot as plt
import shutil

path2wrf = '/Volumes/BUFFALO_SOLDIER/datos_VC/'

months = {'jan': '01', 'feb': '02', 'mar': '03',
          'apr': '04', 'may': '05', 'jun': '06',
          'jul': '07', 'aug': '08', 'sep': '09',
          'oct': '10', 'nov': '11', 'dic': '12'}

location = ['MER', 'PED', 'SAG', 'TLA', 'UIZ', 'SFE']

xlat = np.loadtxt('../datos/xlat_d02_interpolado.txt')
xlong = np.loadtxt('../datos/xlong_d02_interpolado.txt')

print('***START***')

cdmx = np.loadtxt('../datos/maps/EstadosMX/CDMX.xy')
edomx = np.loadtxt('../datos/maps/EstadosMX/EdoMexico.xy')
mor = np.loadtxt('../datos/maps/EstadosMX/Morelos.xy')

lons = np.reshape(xlong, 102*128)
lats = np.reshape(xlat, 102*128)

for hour in range(11, 15):

    dir2 = "../datos/max_min_anual/{}/{}h_{}_annual.dat"
    print(dir2.format(hour, hour, 'max'))

    annual_max = np.loadtxt(dir2.format(hour, hour, 'max'))
    annual_min = np.loadtxt(dir2.format(hour, hour, 'min'))

    # ############# Ploting ######################
    plt.rcParams.update({'font.size': 13})

    cdmx = np.loadtxt('../datos/maps/EstadosMX/CDMX.xy')
    edomx = np.loadtxt('../datos/maps/EstadosMX/EdoMexico.xy')

    dir3 = "../graficas/max_min_anual/{}".format(hour)
    if os.path.exists(dir3):
        shutil.rmtree(dir3)
    os.makedirs(dir3)
    # ## max ###

    fig = plt.figure(figsize=(8.9, 8))
    ax = plt.subplot()
    im = ax.hexbin(lons, lats, C=np.reshape(annual_max, 102*128),
                   gridsize=80, alpha=1, linewidths=0, cmap='YlOrRd_r')
    ax.plot(cdmx[:, 0], cdmx[:, 1], c='k')
    ax.plot(edomx[:, 0], edomx[:, 1], c='k')
    ax.plot(mor[:, 0], mor[:, 1], c='k')
    ax.set_ylim(19, 19.9)
    ax.set_xlim(-99.5, -98.6)
    fig.colorbar(im)
    ax.set_title('Anual maximum at {}:00 (GMT-6)'.format(hour))

    # my_map.colorbar(location='bottom',
    # label=r'Ventilation Coeficient ($m^2 / s$)')

    plt.savefig(dir3 + '/{}h_max'.format(hour), facecolor=(1, 0, 0, 0))

    # ### min ####

    fig = plt.figure(figsize=(8.9, 8))
    ax = plt.subplot()
    im = ax.hexbin(lons, lats, C=np.reshape(annual_min, 102*128),
                   gridsize=80, alpha=1, linewidths=0)
    ax.plot(cdmx[:, 0], cdmx[:, 1], c='k')
    ax.plot(edomx[:, 0], edomx[:, 1], c='k')
    ax.plot(mor[:, 0], mor[:, 1], c='k')
    ax.set_ylim(19, 19.9)
    ax.set_xlim(-99.5, -98.6)
    fig.colorbar(im)
    ax.set_title('Anual minimum at {}:00 (GMT-6)'.format(hour))

# my_map.colorbar(location='bottom',
# label=r'Ventilation Coeficient($m^2 / s$)')

    plt.savefig(dir3 + '/{}h_min'.format(hour), facecolor=(1, 0, 0, 0))
print('***DONE***')
