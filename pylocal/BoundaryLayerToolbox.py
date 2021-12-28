import scipy.interpolate as interpolate
import numpy as np
import datetime
import pandas as pd

def interpolate_velocity(XLONG, XLAT, XLONG_U, XLAT_U, U, uu = True, Kind = 'linear'):

    '''
    interpolate_velocity(XLONG, XLAT, XLONG_U, XLAT_U, U, uu = True, Kind = 'linear')

        `XLON`, `XLAT`, `XLONG_U`, `XLAT_U, U` van con su dimensión temporal.
        `U` va con su dimensión temporal.
        `uu` define si se trata de velocidad zonal o meridional, es decir si se está interpolando 'u', uu = True.
        `Kind`, tipo de interpolación. Por default es linear.

        ej:
            interpolate_velocity(xlong, xlat, xlong_v, xlat_v, v, uu = False)

    '''

    x_old = XLONG_U[0, 1, :]
    y_old = XLAT_U[0, :, 1]
    x_new = XLONG[0, 1, :]
    y_new = XLAT[0, :, 1]

    if uu == True:
        u_shape = (U.shape[0], U.shape[1], U.shape[2], U.shape[3]-1)

    else:
        u_shape = (U.shape[0], U.shape[1] ,U.shape[2] - 1, U.shape[3])


    U_out = np.zeros(u_shape, dtype='float32')
    #U_out = np.zeros(u_shape, dtype='float32')

    for t in range(0, U.shape[0]):
        for h in range(0, U.shape[1]):

            f = interpolate.interp2d(x_old, y_old, U[t, h, :, :], kind = Kind)
            U_out[t, h, :, :] = f(x_new, y_new)

    return U_out

def compute_height(PH, PHB):

    '''
    compute_height(PH, PHB)

        PH y PHB deben ser prporcionados como una matriz de 4 dimensiones es decir no hay especificar su variable temporal.

    '''

    g = 9.8
    z_shape = (PH.shape[0], PH.shape[1]-1, PH.shape[2], PH.shape[3])
    Z = np.zeros(z_shape, dtype='float32')

    for t in range(0, PH.shape[0]):
        for h in range(0, PH.shape[1]-1):

            Z[t, h, :, :] = ((PH[t, h, :, :] + PHB[t, h, :, :]) + (PH[t, h+1, :, :] + PHB[t, h+1, :, :]))/(g*2)

    return Z

def compute_Richardson(T_s, θ, Z, u, v):

    '''
    compute_Richardson(T_s, θ, Z, u, v):
        OUT: Ri

        T_s = Temperatura superficial
        θ = Temperatura potencial. Tiene que ser un arreglo 1d con una temperatura potencial por cada nivel.
        Z = Arreglo con las alturas para una ubicación.
        u = Arreglo de 1d con los vientos u en cada nivel.
        v = Arreglo de 1d con los vientos v en cada nivel.

        Ri = un arreglo con las mismas dimensiones que Z, con los Richardson calculados para cada altura.

    '''

    g = 9.8
    Ri = np.zeros(Z.shape, dtype='float32')

    for i in range(1,len(θ)-2):

        Vu = np.sqrt(u[i+1]**2 + v[i+1]**2)
        Vd = np.sqrt(u[i-1]**2 + v[i-1]**2)

        Ri[i] = g / T_s * ((θ[i+1] - θ[i-1])*(Z[i+1] - Z[i-1]))/(Vu - Vd)**2

    return Ri


def compute_Richardson_2(θ, Z, u, v):

    '''
        compute_Richardson_2(θ, Z, u, v):
            Especificar tiempo y localización
    '''

    g = 9.8
    Ri = np.zeros(Z.shape, dtype='float32')

    for i in range(0,len(θ)-1):

        Ri[i] = (g*(θ[i] - θ[0])*(Z[i] - Z[0]))/(θ[i] * (u[i]**2 + v[i]**2))

    return Ri

def near_coord_wrf(xlong, xlat, loclong, loclat):

    '''
        near_coord(xlong, xlat, loclong, loclat)
        OUT: nx, ny

            Busca los índices más cercanos a una coordenada. Para salidas WRF.

    '''

    distlog = np.abs(xlong[0,0,:] - loclong)
    distlat = np.abs(xlat[0,:,0] - loclat)
    nx = 0
    ny = 0

    for i in range(0, len(xlong[0,0,:])):

        if distlog[i] < distlog[ny]:
            ny = i

    for j in range(0, len(xlat[0,:,0])):

        if distlat[j] < distlat[nx]:
            nx = j

    return nx, ny

def near_coord_loc(xlong, xlat, loclong, loclat):

    '''
        near_coord(xlong, xlat, loclong, loclat)
        OUT: nx, ny

            Busca los índices más cercanos a una coordenada. Para matrices normales (verificar indices de todas formas).

    '''

    distlog = np.abs(xlong[:,0] - loclong)
    distlat = np.abs(xlat[0,:] - loclat)
    nx = 0
    ny = 0

    for i in range(0, len(xlong[:,0])):

        if distlog[i] < distlog[ny]:
            ny = i

    for j in range(0, len(xlat[0,:])):

        if distlat[j] < distlat[nx]:
            nx = j

    return ny, nx


def detecta_PBL_Ri(Ri, Z, Ric):

    '''
        detecta_PBL(Ri, Z, Ric):
            OUT: n, z

            Decta el índice de la primera capa donde el gradiente es igual al valor crítico. n es el índice y z es la altura donde está la capa límite.
            Ri = perfil vertical de Richardon.
            Z = alturas para una coordenada
            Ric = valor crítico de Richardson. Usualmente es 0.21.
    '''

    n = 0

    for i in range(0,len(Ri)-1):

        if Ri[i] < Ric and Ri[i+1] > Ric:
            n = i
            break
        elif Ri[i] > Ric and Ri[i+1] < Ric:
            n = i
            break

    print('Capa límite: ', Z[i], '. Ínidce: ', n)
    return n, Z[n]

def detecta_PBL_indices(Ri, Z, Ric):

    '''
        detecta_PBL_indices(Ri, Z, Ric):
            OUT: n

            Decta el conjunto de índices donde el gradiente es igual al valor crítico. n es un arreglo que contiene todos los índices.
            Ri = perfil vertical de Richardon.
            Z = alturas para una coordenada
            Ric = valor crítico de Richardson. Usualmente es 0.21.
    '''

    n = []

    for i in range(0,len(Ri)-1):

        if Ri[i] < Ric and Ri[i+1] > Ric:
            n.append(i)

        elif Ri[i] > Ric and Ri[i+1] < Ric:
            n.append(i)

        elif Ri[i] == 0.21:
            n.append(i)
            print('índice ', i, ' == ', Ric)

    #print('Capa límite: ', Z[i], '. Ínidce: ', n)
    return n #, Z[n]

nombres_delegaciones = ["alvaro_obregon", "azcapotzalco", "benito_juarez", "coyoacan", "cuajimalpa", "cuauhtemoc", "gustavo_a_madero", "iztacalco", "iztapalapa",
"magdalena_contreras", "miguel_hidalgo", "milpa_alta", "tlahuac", "tlalpan", "venustiano_carranza", "xochimilco"]

nombres_estados = ["CDMX", "Michoacan", "Tlaxcala", "EdoMexico", "Morelos", "Guerrero", "Puebla", "Hidalgo", "Queretaro"]


class region:
    """
    Declares a new class specific for geografical polygons. The main purpose is to locate which points in a grid are inside of the polygon.
    ATRIBUTES:
        self.lon: Is an array with all the longitudinal coordinates of the polygon.
        self.lat: Is an array with all the latitude coordinates of the polygon.
        self.max_lon: gives the max longitud of the polygon.
        self.max_lat: gives the max longitud of the polygon.
        self.min_lon: gives the min longitud of the polygon.
        self.min_lat: gives the min longitud of the polygon.
        self.name: Is the name of the region, in a string.
        self.nx: All the x indices
        self.ny:
    """
    def __init__(self):
        self.lon = None
        self.lat = None
        self.max_lon = None
        self.max_lat = None
        self.min_lon = None
        self.min_lat = None
        self.name = None
        self.nx = None
        self.ny = None

def read_region(region, f):
    """
    read_region(region, f):
        The function reads an .txt file and fills up its attributes, except region.nx and region.ny.
        'region' is an object class region, previously declared as region(). f is the file location, it must be a string.

    """
    n = f.find('.')
    region.name = f[0:n]
    R=open(f,'r')
    lon=[]
    lat=[]
    for line in R:
        if '>' in line:
            pass
        else:
            lon.append(float(line.split()[0]))
            lat.append(float(line.split()[1]))
    region.lon=np.array(lon)
    region.lat=np.array(lat)
    region.max_lon = max(region.lon)
    region.max_lat = max(region.lat)
    region.min_lon = min(region.lon)
    region.min_lat = min(region.lat)

def in_or_out(region, x, y):
    """
    in_or_out(region, x, y):
        Checks if the point x and y, is inside of the polygon region. The polygon must be an object class region.
        OUT: boolean.
    """
    crossings = 0
    for i in range(0,len(region.lon)-1):
        if x < region.lon[i] and x < region.lon[i+1] or x > region.lon[i] and x > region.lon[i+1]:
            pass

        elif y > region.lat[i] and y > region.lat[i+1]:
            pass

        elif y < region.lat[i] and y < region.lat[i+1]:
            if x < region.lon[i] and x > region.lon[i+1] or x > region.lon[i] and x < region.lon[i+1]:
                crossings += 1

        elif y > region.lat[i] and y < region.lat[i+1]:
            if x > region.lon[i] and x < region.lon[i+1]:
                y_c = region.lat[i] + (region.lat[i+1] - region.lat[i])*(x - region.lon[i])/(region.lon[i+1] - region.lon[i])
                if y_c > y:
                    crossings += 1

        elif y < region.lat[i] and y > region.lat[i+1]:
            if x < region.lon[i] or x > region.lon[i+1]:
                y_c = region.lat[i+1] + (region.lat[i] - region.lat[i+1])*(x - region.lon[i+1])/(region.lon[i] - region.lon[i+1])
                if y_c > y:
                    crossings += 1

    if crossings % 2 == 0:
        return False

    elif crossings % 2 != 0:
        return True

def points_in_region(region, x_long, x_lat):
    """
    points_in_region(region, x_long, x_lat):
        Looks for the points inside a polygon. 'region' is the polygon it must be an object region.
        x_long is an array containing all the longitud coordinates of the grid.
        x_lat is an array containing all the latitud coordinates of the grid.
            OUT: nothing. It appends the nx and ny indices of the points inside of the polygon to the atribitute region.nx and region.ny .
    """
    nx = []
    ny = []
    for i in range(0, x_long.shape[0]):
        for j in range(0, x_long.shape[1]):
            if in_or_out(region, x_long[i,j], x_lat[i,j]) == True:
                nx.append(i)
                ny.append(j)
    #return nx, ny
    region.nx = nx
    region.ny = ny

def import_var_mat(file, station):
    """
    import_var_mat(file, station):
        Imports the variables in a .mat file previously read using scipy.io.loadmat() function.
        The argument station is the name or acronym of the station, it must be a string.
        It returns a directory containing all the arrays.
    """


    variables = ["PBLH","T","T2","U","V","PH","PHB","HGT","XLAT","XLONG"]#,"XLAT_U","XLONG_U","XLAT_V","XLONG_V"]
    d = {}
    for i in variables:
        d[i] = file["s"][station][0][0][0][0][i]

    return

def read_ceilometro_month(file_path):
    """
    read_celiomentro_month(file_path)
         OUT: datetime format array, pblh_raw, pblh_filtered
    Is a function that imports data of the ceilometer data per month. You can find the data in the
    folder Datos/ceilometro/215_utc.
    """
    datetimes = []
    raws = []
    filtereds = []
    file = open(file_path, 'r')
    for line in file:
        date, raw, filtered = line.split()
        date = datetime.datetime.strptime(date, '%Y-%m-%d-%H:%M:%S')
        datetimes.append(date)
        raws.append(raw)
        filtereds.append(filtered)

    filtereds = np.array(filtereds)
    filtereds = filtereds.astype(np.float)
    raws = np.array(raws)
    raws = raws.astype(np.float)
    return datetimes, raws, filtereds

def search_hours(hh, DT):
    indexes = []
    for i in range(0, len(DT)):
        if DT[i].hour == hh and DT[i].minute == 0:
            indexes.append(i)
    return indexes

def promedios_mesuales_hora(hh, DT, RAW):

    index_array = search_hours(hh, DT)

    mensuales = []
    mensuales_std = []
    mensuales_hora = []
    mensuales_hora_std = []

    for i in index_array:
        mensuales.append(RAW[i])
        intervalo_hora = []

        for j in range(-3, 4):
            intervalo_hora.append(RAW[i + j])

        mean_hora = np.mean(intervalo_hora)
        std_hora = np.std(intervalo_hora)
        mensuales_hora.append(mean_hora)
        mensuales_hora_std.append(std_hora)


    mean_mesuales = np.mean(mensuales)
    std_mensuales = np.std(mensuales)
    mean_mensuales_hora = np.mean(mensuales_hora)
    std_mensuales_hora = np.mean(mensuales_hora_std)

    return mean_mesuales, std_mensuales, mean_mensuales_hora, std_mensuales_hora

def promedios_mensuales(DT, RAW):
    mes = []
    mes_std = []
    mes_inteval = []
    mes_inteval_std = []
    for h in range(0, 24):
        mean_mm, std_mm, mean_mm_intv, std_mm_intv = promedios_mesuales_hora(h, DT, RAW)
        mes.append(mean_mm)
        mes_std.append(std_mm)
        mes_inteval.append(mean_mm_intv)
        mes_inteval_std.append(std_mm_intv)

    mes = np.array(mes)
    mes_std = np.array(mes_std)
    mes_inteval = np.array(mes_inteval)
    mes_inteval_std = np.array(mes_inteval_std)

    return  [mes, mes_std, mes_inteval, mes_inteval_std]

def promedios_mensuales_wrf(PBLH, ix, iy):
    month = []
    month_std = []

    for h in range(0, 24):

        h_mean = np.mean(PBLH[:,h, ix, iy])
        h_std = np.std(PBLH[:,h, ix, iy])
        month.append(h_mean)
        month_std.append(h_std)

    month = np.array(month)
    month_std = np.array(month_std)

    return  [month, month_std]

def exportfile(filename, ceilo, wrf_24, wrf_48, encabezado = ''):
    Arr = np.zeros((8, 24))
    Arr[0,:] = ceilo[0]
    Arr[1,:] = ceilo[1]
    Arr[2,:] = ceilo[2]
    Arr[3,:] = ceilo[3]
    Arr[4,:] = wrf_24[0]
    Arr[5,:] = wrf_24[1]
    Arr[6,:] = wrf_48[0]
    Arr[7,:] = wrf_48[1]

    np.savetxt(filename, Arr.T, fmt="%10.3f", header=encabezado)
    return Arr.T

def wrf2dataframe(vc_24, pblh_24, u_24, month_t_range, ix, iy):
    """
        wrf2dataframe(var_24, var_48, month_t_range, ix, iy):
        - var_24 : salida de variable 24 para el dominio.
        - month_t_range : rango temoral de los datos var_24 y var_48.
        - ix y iy son los índices que corresponden al punto más cercano a una estación en el dominio.
    """

    i_shape= vc_24.shape

    month_vc_24 = np.reshape(vc_24[:,:, ix, iy], i_shape[0]*i_shape[1])
    month_pblh_24 = np.reshape(pblh_24[:,:, ix, iy], i_shape[0]*i_shape[1])
    month_u_24 = np.reshape(u_24[:,:, ix, iy], i_shape[0]*i_shape[1])


    month_wrf_df = pd.DataFrame({'VC' : pd.Series(month_vc_24, index=month_t_range),
                               'pblh' : pd.Series(month_pblh_24, index=month_t_range),
                               'u_mean' : pd.Series(month_u_24, index=month_t_range)})
    return month_wrf_df

def find_pblh_index(PBLH, HGT, Z):
    """
        find_pblh_index(PBLH, HGT, Z):
            'PBLH' es la altura de capa de mezcla en un dominio espacial con su dimensión temporal.
            'HGT' es el relieve en el mismo dominio.
            'Z' son todas las alturas para el dominio.
    """
    indexes = np.zeros_like(PBLH, dtype=int) #creates the array that will store the indexes.
    for t in range(0, Z.shape[0]):
        for i in range(0, Z.shape[2]):
            for j in range(0, Z.shape[3]):
                for h in range(0, Z.shape[1]):

                    if Z[t,h,i,j] > PBLH[t,i,j]+ HGT[0,i,j]: #if the heigth
                        indexes[t,i,j] = h
                        break
    return indexes

def U_mean_PBL(U, V, PBLH, HGT, Z):
    """
    U_mean_PBL(U, V, PBLH, HGT, Z)
        Computes the mean velocity magnitud under de PBL for a 2D domain with temporal dimension.
    """

    U_mean_PBL = np.zeros_like(PBLH) #Creates the new array to store the VC for each point and time.
    U_mean = np.sqrt(U**2 + V**2) #Computes the magnitud of the velocity
    ix_pblh = find_pblh_index(PBLH, HGT, Z) #Computes de height indexes that correspond to the PBLH.

    for t in range(0, Z.shape[0]):
        for i in range(0, Z.shape[2]):
            for j in range(0, Z.shape[3]):

                if ix_pblh[t, i, j] == 0: #to avoid nan in the data.
                    vertical_U_mean = np.mean(U_mean[t, 0, i, j])
                else:
                    vertical_U_mean = np.mean(U_mean[t, :ix_pblh[t,i,j], i, j]) #the average of the velocity magnitude in the mixed layer.

                U_mean_PBL[t,i,j] = vertical_U_mean #computing the VC.

    return U_mean_PBL

def U_PBL(U, PBLH, HGT, Z):
    """
    ventilation_coefficient(U, V, PBLH, HGT, Z)
        Computes the ventilation coefficient for a 2D domain with temporal dimension.
    """

    U_PBL = np.zeros_like(PBLH) #Creates the new array to store the VC for each point and time.
    ix_pblh = find_pblh_index(PBLH, HGT, Z) #Computes de height indexes that correspond to the PBLH.

    for t in range(0, Z.shape[0]):
        for i in range(0, Z.shape[2]):
            for j in range(0, Z.shape[3]):

                if ix_pblh[t, i, j] == 0: #to avoid nan in the data.
                    vertical_U_mean = np.mean(U[t, 0, i, j])
                else:
                    vertical_U_mean = np.mean(U[t, :ix_pblh[t,i,j], i, j]) #the average of the velocity magnitude in the mixed layer.

                U_PBL[t,i,j] = vertical_U_mean #computing the VC.

    return U_PBL

def ventilation_coefficient(U, V, PBLH, HGT, Z):
    """
    ventilation_coefficient(U, V, PBLH, HGT, Z)
        Computes the ventilation coefficient for a 2D domain with temporal dimension.
    """

    vc = np.zeros_like(PBLH) #Creates the new array to store the VC for each point and time.
    U_mean = np.sqrt(U**2 + V**2) #Computes the magnitud of the velocity
    ix_pblh = find_pblh_index(PBLH, HGT, Z) #Computes de height indexes that correspond to the PBLH.

    for t in range(0, Z.shape[0]):
        for i in range(0, Z.shape[2]):
            for j in range(0, Z.shape[3]):

                if ix_pblh[t, i, j] == 0: #to avoid nan in the data.
                    vertical_U_mean = np.mean(U_mean[t, 0, i, j])
                else:
                    vertical_U_mean = np.mean(U_mean[t, :ix_pblh[t,i,j], i, j]) #the average of the velocity magnitude in the mixed layer.

                vc[t,i,j] = PBLH[t,i,j] * vertical_U_mean #computing the VC.

    return vc

def VCS(dir_month):
    """
    VCS(dir_month):
        Calcula el producto punto de la velocidad con el gradiente del relieve, para un directorio con las siguientes variables:
        'U', 'V', 'HGT',

        'U', 'V'  ya deben estar interpoladas.

        Modifica el directorio ya existente y agrega la variable 'I_VCS'

    """

    U = dir_month['U']
    V = dir_month['V']
    b = dir_month['HGT'][:,:]
    grad_b = np.gradient(b)

    u_shape = (U.shape[0], U.shape[2], U.shape[3])
    I_VCS = np.zeros(u_shape, dtype='float32')

    for t in range(0, U.shape[0]):
        for y in range(0, U.shape[3]):
            for x in range(0, U.shape[2]):

                grad_b_vect = [grad_b[0][x,y], grad_b[1][x,y]]

                U_vect = [U[t,0, x,y], V[t,0,x,y]]
                #print(U_vect)
                I_VCS[t,x,y] = np.dot(U_vect, grad_b_vect)/1000


    dir_month['I_VCS'] = I_VCS

def interpolate_field(x_range, y_range, XLONG_field, XLAT_field, field, Kind = 'linear'):

    '''
    interpolate_field(x_range, y_range, XLONG_field, XLAT_field, field, Kind = 'linear')

        Hola. Aquí debe haber una descripción de la función, pero no la hay... Lo siento mucho.

    '''
    #L = []
    nx = len(x_range)
    ny = len(y_range)
    x_old = XLONG_field[0,0,:]
    y_old = XLAT_field[0,:,0]

    if len(field.shape) == 4:
        field_shape = (field.shape[0], field.shape[1], nx, ny)
        field_out = np.zeros(field_shape, dtype='float32')
        #print(field_out.shape)

        for t in range(0, field.shape[0]):
            for h in range(0, field.shape[1]):

                f = interpolate.interp2d(x_old, y_old, field[t, h, :, :], kind = Kind)
                field_out[t, h, :, :] = f(x_range, y_range).T
                #L.append(f(x,y))

    elif len(field.shape) == 3:
        field_shape = (field.shape[0], nx, ny)
        field_out = np.zeros(field_shape, dtype='float32')
        #print(field.shape)
        #print(field_out.shape)

        for t in range(0, field.shape[0]):

            f = interpolate.interp2d(x_old, y_old, field[t, :, :], kind = Kind)
            field_out[t, :, :] = f(x_range, y_range).T
            #L.append(f(x,y))

    return field_out

def ajuste_lineal(x, a, b):
    return a + b*x
def brunt_vaisala_freq_square(Z, T_pot):
    g = 9.8 #m/s^2
    t_len = Z.shape[0]
    h_len = Z.shape[1]
    x_len = Z.shape[2]
    y_len = Z.shape[3]

    NN = np.zeros((Z.shape[0], Z.shape[1]-1, Z.shape[2], Z.shape[3]))
    for t in range(0, t_len):
        for x in range(0, x_len):
            for y in range(0, y_len):

                NN[t, :, x, y] = g/T_pot[t,:h_len-1, x, y] * np.diff(T_pot[t,:, x, y])/np.diff(Z[t, :, x, y])
    return NN

def E1or30(month):
    if month in ['jan', 'mar', 'may', 'jul', 'aug', 'oct', 'dic']:
        return '31'
    elif  month in ['apr', 'jun', 'sep', 'jul', 'nov']:
        return '30'
    elif month == 'feb':
        return '28'
