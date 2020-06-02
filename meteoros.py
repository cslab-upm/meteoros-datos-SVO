# coding=utf-8
import datetime
import os
import configparser
from bs4 import BeautifulSoup
import requests
import shutil
import numpy as np
from PIL import Image
from PIL import ImageOps
from astropy.io import fits
from astropy.table import Table as tb
import sys
from astropy.io.votable import parse,writeto,parse_single_table
from astropy.io.votable.tree import Param,Info
from astropy.io.votable.table import from_table
from astropy.io.fits import Header
from astropy import units as u
import gzip
import warnings
import mysql.connector
from mysql.connector import errorcode
warnings.filterwarnings("ignore",module='astropy.io.votable.tree')

#########################################
###      VARIABLES CONFIGURACION      ###
#########################################

estacion = sys.argv[1]
diaExtraido = sys.argv[2]
directorio = "./Extraidos/" + diaExtraido
directorioLogs = "./Logs/" + diaExtraido + ".log"
flogs = open(directorioLogs, "a")

try:
    print("LOG: Leyendo fichero de configuracion")
    config = configparser.ConfigParser()
    config.read('configuracion.properties')
    
    raiz = config.get('URLs', 'raiz')
    
    dirFITS = config.get('Directorios', 'dirFITS')
    dirVOTable = config.get('Directorios', 'dirVOTable')
    directorioTransformadosFits = directorio + dirFITS
    directorioTransformadosVOTable = directorio + dirVOTable
    dirEchoes = config.get('Directorios', 'dirEchoes')
    dirDatosAbiertos = config.get('Directorios', 'dirDatosAbiertos')
    dirGuardados = config.get('Directorios', 'dirGuardados')
    
    nombreFicheros = config.get('Ficheros', 'nombreFicheros')
    permisos = config.get('Ficheros', 'permisos')
    DescripcionVOTable = config.get('Ficheros', 'DescripcionVOTable')
    
    username = config.get('MySQL','username')
    password = config.get('MySQL','password')

    col1T1 = config.get('ColumnasTablas', 'col1T1')
    col2T1 = config.get('ColumnasTablas', 'col2T1')
    col3T1 = config.get('ColumnasTablas', 'col3T1')
    col4T1 = config.get('ColumnasTablas', 'col4T1')
    
    col1T2 = config.get('ColumnasTablas', 'col1T2')
    col2T2 = config.get('ColumnasTablas', 'col2T2')
    col3T2 = config.get('ColumnasTablas', 'col3T2')
    col4T2 = config.get('ColumnasTablas', 'col4T2')
    col5T2 = config.get('ColumnasTablas', 'col5T2')
    
    umbralBajada = config.get('Umbrales', 'umbralBajada')
    umbralSubida = config.get('Umbrales', 'umbralSubida')
    
    durOverdenseEco = config.get('EcoOverdense', 'durOverdenseEco')
    duracionEco = int((int(durOverdenseEco)/1000)*10)
    
    recogerDatosDe = config.get('RecogerDatos', 'recogerDatosDe')
    recogerPrimaryDe = config.get('RecogerDatos', 'recogerPrimaryDe')

    cabeceras = config.get(recogerDatosDe, 'cabeceras')
    cabeceras = cabeceras.split(",")
   
    cabecerasPrimaryHDU = config.get(recogerPrimaryDe, 'cabecerasPrimaryHDU')
    cabecerasPrimaryHDU = cabecerasPrimaryHDU.split(",")
    
    parametros = []
    valores = []
    descripciones = []

    for i in range(len(cabeceras)):
        parametros.append(config.get(recogerDatosDe, cabeceras[i]))
    
    for n in range(len(parametros)):
        dato = parametros[n].split(",")
        valores.append(dato[0])
        descripciones.append(dato[1])
    
    paramsPrimaryHDU = []
    valsPrimaryHDU = []
    desPrimaryHDU = []
    
    for i2 in range(len(cabecerasPrimaryHDU)):
        paramsPrimaryHDU.append(config.get(recogerPrimaryDe, cabecerasPrimaryHDU[i2]))
    
    for n2 in range(len(paramsPrimaryHDU)):
        dato = paramsPrimaryHDU[n2].split(",")
        valsPrimaryHDU.append(dato[0])
        desPrimaryHDU.append(dato[1])
    
    totalCabeceras = cabecerasPrimaryHDU + cabeceras
    totalValores = valsPrimaryHDU + valores
    totalDescripciones = desPrimaryHDU + descripciones
    
    c1 = fits.Card('EXTNAME', 'PrimaryHDU', 'name of the extension')
    c2 = fits.Card('EXTNAME', 'ImageHDU', 'name of the extension')
    c3 = fits.Card('EXTNAME', 'SpectrogramHDU', 'name of the extension')
    c4 = fits.Card('EXTNAME', 'LightCurveHDU', 'name of the extension')
    c5 = fits.Card('DATE', diaExtraido, 'date of its detection (YYYY-MM-DD)')
    
    primaryHeaders = [c1,c5]
    imgHeaders = [c2,c5]
    espHeaders = [c3,c5]
    dataHeaders = [c4,c5]
    
    for p in range(len(cabeceras)):
        if(cabeceras[p][0:7] == "COMMENT" or cabeceras[p][0:7] == "HISTORY"):
            imgHeaders.append(fits.Card(cabeceras[p][0:7],valores[p],descripciones[p]))
            dataHeaders.append(fits.Card(cabeceras[p][0:7],valores[p],descripciones[p]))
            espHeaders.append(fits.Card(cabeceras[p][0:7],valores[p],descripciones[p]))
        else:
            imgHeaders.append(fits.Card(cabeceras[p],valores[p],descripciones[p]))
            dataHeaders.append(fits.Card(cabeceras[p],valores[p],descripciones[p]))
            espHeaders.append(fits.Card(cabeceras[p],valores[p],descripciones[p]))           
    
    for p1 in range(len(cabecerasPrimaryHDU)):
        if(cabecerasPrimaryHDU[p1][0:7] == "COMMENT" or cabecerasPrimaryHDU[p1][0:7] == "HISTORY"):
            primaryHeaders.append(fits.Card(cabecerasPrimaryHDU[p1][0:7],valsPrimaryHDU[p1],desPrimaryHDU[p1]))
        else:
            primaryHeaders.append(fits.Card(cabecerasPrimaryHDU[p1],valsPrimaryHDU[p1],desPrimaryHDU[p1]))            
    
    ih = Header(imgHeaders)
    dh = Header(dataHeaders)
    eh = Header(espHeaders)
    flogs.write("LOG: Fichero de configuracion leido con EXITO\n")
except:
    flogs.write("LOG: ERROR en la lectura del fichero de configuracion\n")
    flogs.close()
    sys.exit(1)

# Funcion que lee los datos del dat y los escribe en otro fichero 
def manejodats(archivos,flag,duracion,eliminados,t_deteccion,fecha):
    try:
        for i in range(len(archivos)):
            array_lineas = []
            diferencia = []
            interf = 1 
            f = open(dirGuardados + estacion + dirEchoes + diaExtraido + "/gnuplot/specs/" + flag + "/" + archivos[i] , "r")
            leido = f.readlines()
            f.close()
            for n in range(len(leido)):
                linea = str(leido[n])
                linea = linea.replace('\n','')
                lineas = linea.split(" ")
                final = [p for p in lineas if p ]
                if(final):
                    array_lineas.append(final)
            #para cada instante toma 968 muestras
            resultado2 = -1
            if(flag == "overdense" or flag == "fakes"): 
                t = 967
                #comprueba el umbral de subida para el inicio de la señal
                while t < len(array_lineas):
                    if(float(array_lineas[t][6]) > float(umbralSubida)):
                        tamIn = t
                        break
                    t += 968
            
                d = tamIn+968

                while d < len(array_lineas):
                    c = 0
                    resultado = 0
                    if(float(array_lineas[d][6]) < float(umbralBajada)):
                        k = d+968
                        #comprueba si la señal vuelve a subir durante 1s
                        while c < duracionEco and k < len(array_lineas):
                            if(float(array_lineas[k][6]) > float(umbralSubida)):
                                resultado = -1
                                break
                            c += 1
                            k += 968
                        if(resultado == 0):
                            tamFin = d
                            break
                    d += 968
            #para eventos underdense
            else:
            
                t = 967
                resultado2 = 0
                while t < len(array_lineas):
                    if(float(array_lineas[t][6]) > float(umbralSubida)):
                        tamIn = t
                        if(t < len(array_lineas)-1000):
                            resultado2 = -1
                        break
                    t += 968
                 
                if(resultado2 == 0):
                    tamIn = 967
                    
                d = tamIn+968
                while d < len(array_lineas):
                    if(float(array_lineas[d][6]) < float(umbralBajada)):
                        tamFin = d
                        break
                    d += 968
            sinRuido = array_lineas[tamIn-967:tamFin-967]
            if(resultado2 == 0):
                eliminados.append(i)
                continue

           # deteccion interferencias
           # for length in range(len(sinRuido)):
           #     if(len(sinRuido[length]) == 7):
           #         diferencia.append(sinRuido[length][6])
           # constante = 1
           # comprobar si la diferencia se mantiene constante
           # for cont in range(len(diferencia)):
           #     if(cont != 0):
           #         variacion = abs(float(diferencia[cont]) - float(diferencia[cont - 1]))
           #     if(variacion > float(2) or len(diferencia) == 1):
           #         constante = 0
           #         break
           # if(constante == 0):
           #    print("No es interferencia")
           # else:
           #    eliminados.append(i)
           #     print("Interferencia detectada " + archivos[i])
           #     continue

            fileTabla1 = open(directorio + "/" + archivos[i].replace('.dat','_tabla1.txt'),"w")
            fileTabla2 = open(directorio + "/" + archivos[i].replace('.dat','_tabla2.txt'),"w")
            
            fin = len(sinRuido) - 1
            t_ini = float(sinRuido[0][0])
            t_fin = float(sinRuido[fin][0])
            dur = round((t_fin - t_ini)*1000)
            default = round(100.0)
            date = datetime.datetime.utcfromtimestamp(t_ini).strftime('%Y-%m-%d-%H%M%S%f')
            date = date[:-4]
            if(len(t_deteccion) != 0):
                last = len(t_deteccion) - 1
                if(date == t_deteccion[last]):
                    eliminados.append(i)
                    continue
            if(dur <= 0):
                duracion.append(default)
            else:
                duracion.append(dur)
            
            t_deteccion.append(date)

            date_sql = datetime.datetime.utcfromtimestamp(t_ini).strftime('%Y/%m/%d-%H:%M:%S.%f')
            date_sql = date_sql[:-4]
            fecha.append(date_sql)
	        #introducir muestra de ruido para visualizar mejor la curva de luz
            longitud = len(array_lineas)
            peak = str(array_lineas[longitud-1][5])
            average = str(array_lineas[longitud-1][4])
            for l in range(6):
                if(l != 0):
                    ts = float(t_ini - 0.5 + 0.1*l)
                    t = datetime.datetime.utcfromtimestamp(ts).strftime('%Y/%m/%d-%H:%M:%S.%f')
                    t = t[:-4]
                    fileTabla2.write(str(t) + ' ' + str(ts) + ' ' + str(average) + ' ' + str(peak) + ' ' + '0' + '\n')
            #introducir los datos
            for l in range(len(sinRuido)):
                ts = float(sinRuido[l][0])
                t = datetime.datetime.utcfromtimestamp(ts).strftime('%Y/%m/%d-%H:%M:%S.%f')
                t = t[:-4]
                fileTabla1.write(t + ' ' + sinRuido[l][0] + ' ' + sinRuido[l][1] + ' ' + sinRuido[l][2] + '\n')
                if(len(sinRuido[l]) == 7):
                    fileTabla2.write(t + ' ' + sinRuido[l][0] + ' ' + ' ' + sinRuido[l][4] + ' ' + sinRuido[l][5] + ' ' + sinRuido[l][6] + '\n')
	        #introducir muestra de ruido al final
            for l in range(6):
                if(l != 0):
                    ts = float(t_fin + 0.1*l)
                    t = datetime.datetime.utcfromtimestamp(ts).strftime('%Y/%m/%d-%H:%M:%S.%f')
                    t = t[:-4]
                    fileTabla2.write(str(t) + ' ' + str(ts) + ' ' + str(average) + ' ' + str(peak) + ' ' + '0' + '\n')
            fileTabla1.close()
            fileTabla2.close()  
    except:
        
        flogs.write("LOG: ERROR en la lectura de los .dat o en la eliminacion del ruido en los " + flag + "\n")
        flogs.close()
        shutil.rmtree(directorio)
        sys.exit(1)
        

# Funcion que convierte los archivos a fits
def conversionfits(archivosscreenshots,archivosdat,flag,duracion,eliminados,t_deteccion):
    try:
        os.makedirs(directorioTransformadosFits + flag)    
        #eliminar datos anómalos
        c = 0
        for j in range(len(eliminados)):
            d = eliminados[j] - c
            del archivosscreenshots[d]
            del archivosdat[d]
            c = c + 1
        for i in range(len(archivosscreenshots)):
            test_input = directorio + "/" + archivosdat[i].replace('.dat','_tabla1.txt')
            table = tb.read(test_input, format='ascii')
            os.remove(test_input)
            
            test_input2 = directorio + "/" + archivosdat[i].replace('.dat','_tabla2.txt')
            table2 = tb.read(test_input2, format='ascii')
            os.remove(test_input2)
            
            nombre = archivosdat[i][32:]
            nombreFits = nombre.replace('.dat','')

            screenshot_input = dirGuardados + estacion + dirEchoes + diaExtraido + "/screenshots/" + flag + "/" + archivosscreenshots[i]
            #screenshot_output_1 = directorioTransformadosFits + flag + "/" +  nombreFicheros + nombreFits + '.fits'
            screenshot_output = directorioTransformadosFits + flag + "/" + estacion + '_' + t_deteccion[i] + '.fits'
            
            #fichero = nombreFicheros + nombreFits + '.fits'
            fichero = estacion + '_' + t_deteccion[i] + '.fits'
            c5 = fits.Card('DURATION', duracion[i],'Duration of the event(ms)')
            primaryHeaders.append(c5)
            c6 = fits.Card('TITLE', fichero, 'Name of the file')
            primaryHeaders.append(c6)
            ph = Header(primaryHeaders)
            
            primaryHeaders.remove(c5)
            
            im = Image.open(screenshot_input)
            im = ImageOps.flip(im)
            im.save("temporal.png")
    
            image = Image.open('temporal.png')
            xsize, ysize = image.size
            r, g, b = image.split()
            r_data = np.array(r.getdata())
            r_data = r_data.reshape(ysize, xsize)
            g_data = np.array(g.getdata())
            g_data = g_data.reshape(ysize, xsize)
            b_data = np.array(b.getdata())
            b_data = b_data.reshape(ysize, xsize)
            datos = [r_data,g_data,b_data]
            os.remove('temporal.png')
            
            hdu1 = fits.PrimaryHDU(header=ph)
            hdu2 = fits.ImageHDU(data=datos,header=ih)
            hdu3 = fits.BinTableHDU(data=np.array(table),header=eh)
            hdu4 = fits.BinTableHDU(data=np.array(table2),header=dh)
            hdul = fits.HDUList([hdu1,hdu2,hdu3,hdu4])
            hdul.writeto(screenshot_output)
            
            hdulist = fits.open(screenshot_output, mode='update')
            header2 = hdulist[2].header
            header3 = hdulist[3].header
           
            header2.set('TTYPE1',col1T1.split(",")[0],col1T1.split(",")[1])
            header2.set('TUNIT2','s')
            header2.set('TTYPE2',col2T1.split(",")[0],col2T1.split(",")[1])
            header2.set('TUNIT3','Hz')
            header2.set('TTYPE3',col3T1.split(",")[0],col3T1.split(",")[1])
            header2.set('TUNIT4', 'dB')
            header2.set('TTYPE4',col4T1.split(",")[0],col4T1.split(",")[1])
            header2.set('DURATION',duracion[i],'Duration of the event(ms)')
            
            header3.set('TTYPE1',col1T2.split(",")[0],col1T2.split(",")[1])
            header3.set('TTYPE2',col2T2.split(",")[0],col2T2.split(",")[1])
            header3.set('TUNIT2','s')
            header3.set('TTYPE3',col3T2.split(",")[0],col3T2.split(",")[1])
            header3.set('TUNIT3', 'dB')
            header3.set('TTYPE4',col4T2.split(",")[0],col4T2.split(",")[1])
            header3.set('TUNIT4', 'dB')
            header3.set('TTYPE5',col5T2.split(",")[0],col5T2.split(",")[1])
            header3.set('TUNIT5', 'dB')
            header3.set('DURATION',duracion[i],'Duration of the event(ms)')
                
            hdulist.flush()
            hdulist.close()
            primaryHeaders.pop()
            with open(screenshot_output, 'rb') as f_in:
                with gzip.open(screenshot_output + ".gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    ficherosFITS.append(fichero + ".gz")
    except:
        flogs.write("LOG: ERROR en la conversion  de los " + flag + " a FITS\n")
        flogs.close()
        shutil.rmtree(directorio)
        sys.exit(1)

# Funcion que sube los ficheros FITS comprimidos via FTP
def moverArchivosFITS(ficherosFITS,flag):
    try:
        actual = os.getcwd()
        os.chdir(dirGuardados + estacion + dirDatosAbiertos)
        if(flag == "overdense"):
            os.mkdir(diaExtraido)
            os.chmod(diaExtraido,int(permisos,8))
        os.chdir(diaExtraido)
        os.mkdir(flag)
        os.chmod(flag,int(permisos,8))
        os.chdir(actual + directorioTransformadosFits.replace(".","") + flag)
        for n in range(len(ficherosFITS)):
            os.chmod(ficherosFITS[n],int(permisos,8))
            shutil.move(ficherosFITS[n], dirGuardados + estacion + dirDatosAbiertos + diaExtraido + "/" + flag +"/" + ficherosFITS[n])
        os.chdir(actual)
    except:
        flogs.write("LOG: ERROR al mover los FITS de los " + flag + "\n")
        flogs.close()
        shutil.rmtree(directorio)
        sys.exit(1)        

# Funcion que obtiene los enlaaces para los VOTable
def enlacesVOTable(flag):
    try:
        r  = requests.get(raiz + estacion + dirDatosAbiertos + diaExtraido + "/" + flag)
        data = r.text
        soup = BeautifulSoup(data,'html.parser')
        for link in soup.find_all('a'):
            if(link.get('href').find("gz") != -1):
                url = raiz + estacion + dirDatosAbiertos + diaExtraido + "/" + flag + "/" + link.get('href')
                enlaces.append(url)   
    except:
        flogs.write("LOG: ERROR en la obtencion de los enlaces para los VOTable de los " + flag + "\n")
        flogs.close()
        shutil.rmtree(directorio)
        sys.exit(1)      


# Funcion que convierte los fits a VOTable
def conversionVOTable(archivosdat,flag,t_deteccioni,duracion):
    try:
        os.makedirs(directorioTransformadosVOTable + flag)
        for i in range(len(archivosdat)):
            nombre = archivosdat[i][32:]
            nombreFits = nombre.replace('.dat','')
            nombreVOTable = nombre.replace('.dat','')
            
            #fichero_fits = directorioTransformadosFits + flag + "/" + nombreFicheros + nombreFits + '.fits'
            fichero_fits = directorioTransformadosFits + flag + "/" + estacion + '_' + t_deteccion[i] + '.fits'
            #votable_output =  directorioTransformadosVOTable + flag + "/" + nombreFicheros + nombreVOTable + '.vot'
            votable_output =  directorioTransformadosVOTable + flag + "/" + estacion + '_'+ t_deteccion[i] + '.vot'
            #votable_output2 =  directorioTransformadosVOTable + flag + "/" + nombreFicheros + nombreVOTable + '_2.vot'
            votable_output2 =  directorioTransformadosVOTable + flag + "/" + estacion + '_' + t_deteccion[i] + '_2.vot'
          
            #fichero = nombreFicheros + nombreFits + '.fits'
            fichero = estacion + '_' + t_deteccion[i]
            
            t = tb.read(fichero_fits,2)
            t2 = tb.read(fichero_fits,3)
            
            os.remove(fichero_fits)
            votable = from_table(t[0:1])
            votable2 = from_table(t2[0:1])

            writeto(votable,  votable_output)
            writeto(votable2,  votable_output2)
            
            tabla2 = parse_single_table(votable_output2)
            os.remove(votable_output2)
            
            votable = parse(votable_output)

            resource = votable.resources[0]
            resource.description = "Fichero " + fichero + " " + DescripcionVOTable
            resource.tables.append(tabla2)
            
            param = Param(votable,name="TITLE", datatype="char", arraysize=str(len(fichero)), value=fichero)
            param.description = "Name of the file"
            resource.params.append(param)
            
            param = Param(votable,name="DATE", datatype="char", arraysize=str(len(diaExtraido)), value=diaExtraido)
            param.description = "Date of its detection (YYYY-MM-DD)"
            resource.params.append(param)

            param = Param(votable, name="DURATION", datatype="int",value=duracion[i],unit="ms")
            param.description = "Duration of the event"
            resource.params.append(param)

            for n in range(len(totalValores)):
                flag_u = 0
                index = totalDescripciones[n].find('(')
                if(index != -1):
                    if(n == 41 or n == 44 or n== 45):
                        flag_u = 0
                    else:
                        unidad = totalDescripciones[n].split('(',1)[1].split(')')[0]
                        flag_u = 1
                if(totalValores[n].isdigit() or (totalValores[n].startswith('-') and totalValores[n][1:].isdigit())):
                    if(flag_u == 1):
                        param = Param(votable,name=totalCabeceras[n],datatype='int',value=totalValores[n],unit=unidad)
                    else:
                        param = Param(votable,name=totalCabeceras[n], datatype="int",value=totalValores[n])
                    param.description = totalDescripciones[n]
                    resource.params.append(param)
                elif(totalValores[n] == "True" or totalValores[n] == "False"):
                    param = Param(votable,name=totalCabeceras[n], datatype="boolean",value=totalValores[n])
                    param.description = totalDescripciones[n]
                    resource.params.append(param)
                else:
                    try:
                        if(float(totalValores[n])):
                            if(flag_u == 1):
                                param = Param(votable,name=totalCabeceras[n],datatype='float',value=totalValores[n],unit=unidad)
                            else:
                                param = Param(votable,name=totalCabeceras[n], datatype="float",value=totalValores[n])
                            param.description = totalDescripciones[n]
                            resource.params.append(param)
                    except:
                        if(totalCabeceras[n][0:7] == "COMMENT" or totalCabeceras[n][0:7] == "HISTORY"):
                            info = Info(name=totalCabeceras[n][0:7], value=totalValores[n])
                            resource.infos.append(info)
                        else:
                            param = Param(votable,name=totalCabeceras[n], datatype="char", arraysize=str(len(totalValores[n])), value=totalValores[n])
                            param.description = totalDescripciones[n]
                            resource.params.append(param)
            votable.to_xml(votable_output)
            stri = '    <FITS extnum="2">\n     <STREAM encoding="gzip" href="'+enlaces[i]+'"/>\n    </FITS>\n'
            stri2 = '    <FITS extnum="3">\n     <STREAM encoding="gzip" href="'+enlaces[i]+'"/>\n    </FITS>\n'
            

            f = open(votable_output, "r")
            leido = f.readlines()
            f.close()
            os.remove(votable_output)

            hayIni = 0
            hayFin = 0
            for n in range(len(leido)):
                if(leido[n][4:8] == "DATA"):
                    if(hayIni == 0):
                        Ini = n+1
                        hayIni = 1
                    else:
                        Ini2 = n+1            
                if(leido[n][5:9] == "DATA"):
                    if(hayFin == 0):
                        Fin = n
                        hayFin = 1
                    else:
                        Fin2 = n
    
            parte1 = leido[:Ini]
            parte2 = leido[Fin:Ini2]
            parte3 = leido[Fin2:]
    
            file2 = open(votable_output,"w")
            
            for p1 in range(len(parte1)):
                if(parte1[p1][3:10] == "TABLE n"):
                    file2.write("  <TABLE nrows=\"" + str(len(t)) + "\">" + "\n") 
                else:
                    file2.write(parte1[p1])            
            
            file2.write(stri)

            for p2 in range(len(parte2)):
                if(parte2[p2][3:10] == "TABLE n"):
                    file2.write("  <TABLE nrows=\"" + str(len(t2)) + "\">" + "\n")
                else:
                    file2.write(parte2[p2])
            
            file2.write(stri2)

            for p3 in range(len(parte3)):
                file2.write(parte3[p3])    
                
            file2.close()  
    except:
        flogs.write("LOG: ERROR en la conversion a  VOTable de los " + flag + "\n")
        flogs.close()
        shutil.rmtree(directorio)
        sys.exit(1)   

# Funcion que sube los ficheros VOTable via FTP
def moverArchivosVOTable(ficherosFITS,flag):
    try:
        actual = os.getcwd()
        os.chdir(directorioTransformadosVOTable + flag)
        for n in range(len(ficherosFITS)):
            filename = ficherosFITS[n].replace(".fits.gz",".vot")
            os.chmod(filename,int(permisos,8))
            shutil.move(filename, dirGuardados + estacion + dirDatosAbiertos + diaExtraido + "/" + flag + "/" + filename)
        os.chdir(actual)
    except:
        flogs.write("LOG: ERROR al mover los VOTable de los " + flag + "\n")
        flogs.close()
        shutil.rmtree(directorio)
        sys.exit(1)      

# Funcion que inserta los datos de los meteoros a la DDBB
def insertarDatos(meteoro_id,fecha,duracion,flag):
    try:
        #conexion con la DDBB
        cnx = mysql.connector.connect(user=username,password=password,host='localhost',database='meteorosdb')
        cursor = cnx.cursor()
        if(len(meteoro_id)!=0):
            day = meteoro_id[0][0:10]
        for l in range(len(fecha)):
            m_id = 'fuenlabrada_' + meteoro_id[l]
            add_meteoro = ("INSERT INTO datos_meteoros " "(ID,DATE,STATION,DURATION,DAY,TYPE) " "VALUES (%s, %s, %s, %s, %s, %s)")
            data_meteoro = (m_id,fecha[l],estacion,duracion[l],day,flag)
            cursor.execute(add_meteoro,data_meteoro)
            cnx.commit()
        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            flogs.write("LOG: ERROR al insertar los datos de " + flag + " a la BBDD"+"\n")
            flogs.close()
            shutil.rmtree(directorio)
            sys.exit(1)

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            flogs.write("LOG: ERROR al insertar los datos de " + flag + " a la BBDD" + "\n")
            flogs.close()
            shutil.rmtree(directorio)
            sys.exit(1)
        else:
            print(err)
    else:
        cnx.close()
        

#########################################
###         INICIO DEL SCRIPT         ###
#########################################

r  = requests.get(raiz + estacion + dirEchoes + diaExtraido + "/screenshots/overdense")
if r.status_code != 200:
    print("LOG: No hay datos para extraer en la fecha introducida")
    flogs.write("LOG: ERROR, No hay datos para extraer en la fecha introducida\n")
    flogs.close()
    sys.exit(1)
    
if(os.path.isdir(dirGuardados + estacion + dirDatosAbiertos + diaExtraido)):
    actual = os.getcwd()
    os.chdir(dirGuardados + estacion + dirDatosAbiertos)
    shutil.rmtree(diaExtraido)
    os.chdir(actual)
    
os.makedirs(directorio)

for i in ["overdense","fakes","underdense"]:
    ficherosFITS = []
    enlaces = []
    array_screenshots = []
    array_dats = []
    duration = []
    eliminados = []
    t_deteccion = []
    fecha = []
    try:
        dirs = os.listdir(dirGuardados + estacion + dirEchoes + diaExtraido + "/screenshots/" + i)
        for file in dirs:
            array_screenshots.append(file)
        dirs = os.listdir(dirGuardados + estacion + dirEchoes + diaExtraido + "/gnuplot/specs/" + i)
        for file in dirs:
            array_dats.append(file)
    except:
        flogs.write("LOG: ERROR al listar los directorios con los gnuplots y las screenshots " + i + "\n")
        flogs.close()
        shutil.rmtree(directorio)
        sys.exit(1) 
        
    array_screenshots.sort()
    array_dats.sort()

    print("LOG: Va a comenzar la conversion de los archivos " + i)
    flogs.write("LOG: Conversion de los archivos " + i +  ":\n")
    manejodats(array_dats,i,duration,eliminados,t_deteccion,fecha)
    flogs.write("LOG: Datos leidos de los .dat y ruido eliminado de los " + i + " con exito\n")
    conversionfits(array_screenshots,array_dats,i,duration,eliminados,t_deteccion)
    flogs.write("LOG: Conversion de los archivos " + i + " a FITS realizada con exito\n")
    moverArchivosFITS(ficherosFITS,i)
    flogs.write("LOG: Ficheros FITS " + i + " comprimidos y movidos con exito\n")
    enlacesVOTable(i)
    conversionVOTable(array_dats,i,t_deteccion,duration)
    flogs.write("LOG: Conversion de fits a VOTable de los " + i + " realizada con exito\n")
    moverArchivosVOTable(ficherosFITS,i)
    flogs.write("LOG: Ficheros VOTable de los " + i + " comprimidos y movidos con exito\n")
    insertarDatos(t_deteccion,fecha,duration,i)
    flogs.write("LOG: Datos " + i + " insertados a la BBDD con exito\n")

shutil.rmtree(directorio)
flogs.close()
sys.exit(0) 
