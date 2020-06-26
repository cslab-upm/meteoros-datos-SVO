# Programa de análisis y publicación de datos de meteoros

Este programa consiste en crear archivos FITS y VOT para eventos de meteoros a partir de los datos proporcionados por el programa Echoes.

El programa realizará la tarea de recopilar toda la información útil a partir de los datos en bruto generados por Echoes, permitiendo también reducir el espacio ocupado. Posteriormente, los datos útiles se transformarán en archivos estándares que nos permitirá publicar dichos datos en el repositorio de Observatorio Virtual Español (SVO).

Además, el programa insertará los datos de los meteoros diarios a una base de datos MySQL local, lo cual permite usarlo en el software _SVOCat_ desarrollado por SVO para la publicación de los datos.

La sintaxis para ejecutar el script es el siguiente:

    ./meteoros.sh estacion YYYY-MM-DD

## Instalación

Para la correcta ejecución del software, es necesario instalar **python3** y ciertas librerías de python:

**Python**

    sudo apt-get install python3.7

**BeautifulSoup**

    pip install BeautifulSoup4

**Requests**

    pip install requests

**Numpy**

    pip install numpy

**Pillow**

    pip install Pillow

**Astropy**

    pip install Astropy

**MySQL connector**

    pip3 install mysql-connector-python
    
**Seaborn**
    
    pip install seaborn

## Base de datos MySQL

Además de instalar python, es necesario crear una base de datos MySQL. Para instalar MySQL ejecute:

    sudo apt-get install mysql-server

Una vez instalado MySQL, complete la instalación configurando las opciones de seguridad para la base de datos:

    sudo mysql_secure_instalation

Una vez instalada correctamente MySQL puede importar la base de datos en su máquina:

Conexión a la base de datos:

    mysql -u username -p

Creación de la base de datos:

    mysql> CREATE DATABASE meteorosdb;

Ahora, salga de MySQL (`mysql> exit;`) e importe la estructura de la base de datos (tabla datos_meteoros):

    mysql -u username -p meteorosdb < dump.sql

Para verificar que la base de datos está creada correctamente, visualiza la tabla creada en MySQL:

    mysql> USE meteorosdb

    mysql> DESCRIBE datos_meteoros

Y debería aparecer la siguiente tabla:

| Field    | Type        | Null | Key | Default | Extra |
|----------|-------------|------|-----|---------|-------|
| ID       | varchar(50) | NO   | PRI | NULL    |       |
| DATE     | varchar(50) | NO   |     | NULL    |       |
| STATION  | varchar(50) | NO   |     | NULL    |       |
| DURATION | int(11)     | NO   |     | NULL    |       |
| DAY      | varchar(50) | NO   |     | NULL    |       |
| TYPE     | varchar(50) | NO   |     | NULL    |       |

## Propiedades configurables

El script permite cambiar algunas configuraciones mediante el archivo _configuracion.properties_.

Existen cinco secciones personalizables en el archivo de configuración:
- **[URLs]** Indica la dirección del servidor donde se encuentran los datos abiertos.
- **[Directorios]** Directorios de trabajo. 
    * *dirEchoes* indica el directorio relativo donde están los archivos generados por el programa Echoes
    * *dirDatosAbiertos* indica el directorio relativo donde se almacenarán los archivos FITS y VOT
    * *dirGuardados* indica la ruta absoluta del directorio padre de *dirEchoes* y *dirDatosAbiertos*
- **[Ficheros]**
    * *nombreFicheros* es el nombre de la estación. Es utilizado para generar el nombre de los ficheros generados
    * *permisos* indica los permisos para los archivos generados en forma octal
- **[Umbrales]** Umbrales utilizados en el script para manejar los datos en bruto
- **[MySQL]** Credenciales de la BBDD MySQL
- **[EcoOverdense]** Determina el tiempo máximo (ms) utilizado en el caso de eco sobredenso para determinar si la señal corresponde al mismo eco


## Instalación de la aplicación SVOCat

Para hacer funcionar la aplicación, es necesario un entorno Linux con un servidor web apache, un gestor de base de datos MySQL y el lenguaje de programación PHP.


Una forma sencilla de instalar todos estos paquetes es instalar el paquete LAMP (Linux Apache MySQL PHP). Los comandos para instalar el paquete LAMP serían:


    sudo apt-get install tasksel
    
    sudo tasksel install lamp-server
    
    
Cuando se tenga instalado el paquete, es necesario descomprimir el archivo comprimido meteoros.tar.xz. El archivo debe descomprimirse al directorio donde tenga instalado el servidor web o donde el servidor tenga acceso a ello:


    sudo tar xf meteoros.tar.xz -C $directorio
    
Una vez descomprimida la aplicación, hay que definir los permisos para esta aplicación. Todos los archivos de la aplicación deben ser accesibles por el usuario www-data. Por ejemplo, puede ejecutar:

    cd $directorio
    
    sudo chmod -R ugo+r .
    
    sudo chmod ugo+x `find . -type d`

Además, existen dos directorios especiales /work y /config. El servidor debe tener permiso de lectura y escritura de estos directorios y todos los archivos de estos directorios.

    cd $directorio
    
    sudo chown -R $user:www-data config/ work/
    
    sudo chmod g+rwx config/ work/
    
    sudo chmod -R g+rw config/ work/

