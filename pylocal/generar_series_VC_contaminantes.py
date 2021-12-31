# The script generates the Dataframes with the VC, PBLH, u_mean.
import BoundaryLayerToolbox as blt
import pandas as pd
import numpy as np
import h5py
import os
import shutil

path2wrf = '/Volumes/BUFFALO_SOLDIER/datos_VC/'
path2DataFrames = "../datos/dataframes_VC/"
path2pollutants = "../datos/contaminantes/2015/"

months = {'jan': '01',
          'feb': '02',
          'mar': '03',
          'apr': '04',
          'may': '05',
          'jun': '06',
          'jul': '07',
          'aug': '08',
          'sep': '09',
          'oct': '10',
          'nov': '11',
          'dic': '12'}


def E1or30(month):
    if month in ['jan', 'mar', 'may', 'jul', 'aug', 'oct', 'dic']:
        return '31'

    elif month in ['apr', 'jun', 'sep', 'jul', 'nov']:
        return '30'

    elif month == 'feb':
        return '28'


location = ['MER', 'PED', 'SAG', 'TLA', 'UIZ', 'SFE']
stations = pd.read_csv('../datos/Stations_Info.csv', index_col=0)

xlat = np.loadtxt('../datos/xlat_d02_interpolado.txt')
xlong = np.loadtxt('../datos/xlong_d02_interpolado.txt')

h_i = "00:00:00"
h_f = "23:50:00"
h_f_wrf = "23:00:00"

print('***START***')

for st in location:

    print('-- ' + st + ' --')

    xlat_st, xlong_st = stations.loc[st][['Latitud', 'Longitud']]

    # contaminantes
    o3_path = path2pollutants + st + "/" + st + "_O3_2015.csv"
    o3_2015 = pd.read_csv(o3_path,
                          names=['date', 'station', 'pollutant', 'O3',
                                 'units'])
    o3_2015.index = pd.date_range('2015-01-01 01:00', '2016-01-01 00:00',
                                  freq='1H')
    o3_2015 = o3_2015.reindex(pd.date_range('2015-01-01 00:00',
                                            '2015-12-31 23:00', freq='1H'))
    o3_2015 = o3_2015.drop(['date', 'station', 'pollutant', 'units'], axis=1)

    pm25_path = path2pollutants + st + "/" + st + "_PM2.5_2015.csv"
    pm25_2015 = pd.read_csv(pm25_path, names=['date', 'station',
                                              'pollutant', 'PM2.5', 'units'])
    pm25_2015.index = pd.date_range('2015-01-01 01:00',
                                    '2016-01-01 00:00', freq='1H')
    pm25_2015 = pm25_2015.reindex(pd.date_range('2015-01-01 00:00',
                                                '2015-12-31 23:00', freq='1H'))
    pm25_2015 = pm25_2015.drop(['date', 'station', 'pollutant', 'units'],
                               axis=1)

    pm10_path = path2pollutants + st + "/" + st + "_PM10_2015.csv"
    pm10_2015 = pd.read_csv(pm10_path, names=['date', 'station', 'pollutant',
                                              'PM10', 'units'])
    pm10_2015.index = pd.date_range('2015-01-01 01:00', '2016-01-01 00:00',
                                    freq='1H')
    pm10_2015 = pm10_2015.reindex(pd.date_range('2015-01-01 00:00',
                                                '2015-12-31 23:00', freq='1H'))
    pm10_2015 = pm10_2015.drop(['date', 'station', 'pollutant', 'units'],
                               axis=1)

    Pollutants = pd.concat([o3_2015, pm25_2015, pm10_2015], axis=1)

    VC_year = pd.DataFrame()

    dir = path2DataFrames + st
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

    for mm in months.keys():

        date_i = '2015-' + months[mm] + '-01' + ' ' + h_i
        date_f = '2015-' + months[mm] + '-' + E1or30(mm) + ' ' + h_f
        date_f_wrf = '2015-' + months[mm] + '-' + E1or30(mm) + ' ' + h_f_wrf

        xx, yy = blt.near_coord_loc(xlong, xlat, xlong_st, xlat_st)

        file_24 = h5py.File(path2wrf + months[mm] + '/' + mm + '_24.h5', 'r')
        vc_24 = np.array(file_24.get('vc_24h'))
        pblh_24 = np.array(file_24.get('pblh_24h'))
        u_mean_24 = np.array(file_24.get('u_mean_24h'))

        if mm == 'nov':
            BEG = pd.date_range('2015-11-01 00:00:00', '2015-11-05 23:00:00',
                                freq='1H')
            ENDD = pd.date_range('2015-11-07 00:00:00', '2015-11-18 23:00:00',
                                 freq='1H')
            BEG = BEG.union(ENDD)
            ENDD = pd.date_range('2015-11-20 00:00:00', '2015-11-20 23:00:00',
                                 freq='1H')
            BEG = BEG.union(ENDD)
            ENDD = pd.date_range('2015-11-22 00:00:00', '2015-11-30 23:00:00',
                                 freq='1H')
            month_t_range = BEG.union(ENDD)

        elif mm == 'jun':
            BEG = pd.date_range('2015-06-01 00:00:00', '2015-06-11 23:00:00',
                                freq='1H')
            ENDD = pd.date_range('2015-06-13 00:00:00', '2015-06-30 23:00:00',
                                 freq='1H')
            month_t_range = BEG.union(ENDD)

        elif mm == 'oct':
            BEG = pd.date_range('2015-10-01 00:00:00', '2015-10-03 23:00:00',
                                freq='1H')
            ENDD = pd.date_range('2015-10-05 00:00:00', '2015-10-31 23:00:00',
                                 freq='1H')
            month_t_range = BEG.union(ENDD)

        elif mm == 'jan':
            month_t_range = pd.date_range('2015-01-15 00:00:00',
                                          '2015-01-31 23:00:00', freq='1H')

        elif mm == 'apr':
            month_t_range = pd.date_range('2015-04-02 00:00:00',
                                          '2015-04-30 23:00:00', freq='1H')

        else:
            month_t_range = pd.date_range(date_i, date_f_wrf, freq='1H')

        wrf_df = blt.wrf2dataframe(vc_24, pblh_24, u_mean_24, month_t_range,
                                   xx, yy)
        wrf_df = wrf_df.asfreq('1H')
        VC_year = pd.concat([VC_year, wrf_df], axis=0)

        print(mm + ' concatenating')

    ALL = pd.concat([VC_year, Pollutants], axis=1)

    final_path = path2DataFrames + st + '/vc_' + st + '.csv'
    ALL.to_csv(final_path, float_format='%.2f')

print('***DONE***')
