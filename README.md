# Programa de análisis y publicación de datos de meteoros

Este programa consiste en crear archivos FITS y VOT para eventos de meteoros a partir de los datos proporcionados por el programa Echoes.

El programa realizará la tarea de recopilar toda la información útil a partir de los datos crudos de Echoes, reduciendo el espacio ocupado. Posteriormente, los datos útiles se transformarán en archivos estándares que nos permitirá publicar dichos datos en el repositorio de Observatorio Virtual Español (SVO).

Además, el programa insertará los datos de los meteoros diarios a una base de datos MySQL local, lo cual permite usarlo en el software _SVOCat_ desarrollado por SVO para la publicación de los datos.

El sintaxis para ejecutar el script es el siguiente:

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
| ID       | varchar(30) | NO   | PRI | NULL    |       |
| FECHA    | varchar(30) | YES  |     | NULL    |       |
| ESTACION | varchar(30) | YES  |     | NULL    |       |
| DURACION | int(11)     | YES  |     | NULL    |       |

## Archivo de configuración

