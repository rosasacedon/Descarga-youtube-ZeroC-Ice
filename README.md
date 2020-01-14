# Laboratorio-sistemas-distribuidos
Laboratorio *sistemas distribuidos*

Escuela Superior de Informática.

https://github.com/rosasacedon/SacedonMartin

##  Miembros
* *Rosa María Sacedón Ortega*
* *Victor Martin Alonso*

## Manual de Usuario
Este manual de usuario pretende explicar la funcionalidad de los componentes de la práctica y su forma de ejecución.


### Pasos para ejecutar

1- En una terminal ejecutar lo siguiente:

    make run

Esto ejecutará todos los nodos de la práctica.

2- En otra terminal ejecutamos:

    icegridgui
    
2.1- Creamos una nueva conexión
 
2.2- Abrimos el archivo el archivo xml que contiene la aplicación.
    File -> Open -> *YoutubeDownloaderApp.xml*
    
2.3- Guardamos al registro con el botón (save to a registry)

2.4- Distribuimos la aplicación en el Live Deployment
    Tools -> Path distribution -> Apply path distribution

2.5- Ejecutamos los servidores con cierto orden.
    1) IceStorm
    2) Transfer / Downloader
    3) Orchestrators
    
3- Ejecutar el cliente

    ./run_client.sh
    
## Descripción de la práctica

El objetivo principal del proyecto es diseñar un sistema cliente-servidor que permita la descarga
de ficheros a partir de URIs. El ejemplo típico será la descarga de clips de audio de YouTube. La
implementación de este proyecto permitirá al alumno trabajar, mediante ZeroC Ice, los siguientes
aspectos:


