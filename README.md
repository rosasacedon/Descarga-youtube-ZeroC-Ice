# Laboratorio-sistemas-distribuidos
Laboratorio *sistemas distribuidos*

Escuela Superior de Informática.

https://github.com/rosasacedon/SacedonMartin

##  Miembros
* *Rosa María Sacedón Ortega*
* *Victor Martin Alonso*

## Manual de Usuario

Este manual de usuario pretende explicar la funcionalidad de los componentes de la práctica y su forma de ejecución.

client.config: Archivo con la configuracion del cliente para poderlo ejecutar.

client.py: Contiene el cliente y las llamadas para descargas los archivos mp3 o tranferir los existentes, que estas opciones se controlan mediante 
los flags --downloader y --transfer, la ejecucion de este cliente para descargar por ejemplo un video sería: 
./client.py --Ice.Config=client.config "orchestrator" "--download" "<url>" y el tranfer sería: ./client.py --Ice.Config=client.config "orchestrator" "--transfer" "<nombre_archivo>"

downloader_factory.py: Fabrica downloaders en funcion de las peticiones de descarga que haga el cliente.

downloads-node.config: Archivo de configuracion del nodo downloads, que es el que gestiona las peticiones de descarga.

Makefile: Este archivo contiene las instrucciones para desplegar los nodos del sistema mediante una llamada make run.

orchestrator.py: Gestiona las peticiones del cliente.

orchestrator-node.config: Archivo de configuracion del nodo orchestrator.

registry-node.config: Archivo de configuracion del nodo registry.

run_client.sh: Ejecutable para arrancar el cliente.

run_server.sh: Ejecutable para arrancar los servidores.

templates.xml: Plantilla del orchestrator.

trawlnet.ice: Archivo ice con las estructuras basicas del sistema distribuido.

utils.py: Archivo con funcionalidades sobre los canales de eventos.

YoutubeDownloaderApp.xml: Archivo xml con la configuracion del icegrid, listo para cargarlo en el icegrid y desplegarlo.



### Pasos para ejecutar

* *CON MAKEFILE

1- En una terminal ejecutamos 

    make run
  
  Esto ejecutará todos los nodos de la práctica
  
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
    
3- Ejecutar el cliente con los tres makes que se muestran a continuación: 

3.1- Para la descarga 
	
	make run-client-download url="<url>"
	
3.1- Para la lista

	make run-client-list
	
3.3- Para transferir

	make run-client-transfer nombre="<name.mp3>"

* *CON LOS ARCHIVOS .SH

1- En una terminal ejecutar lo siguiente:

    run_server.sh

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

    ./run_client.sh <url> <nombre_fichero>
    
## Descripción de la práctica

El objetivo principal del proyecto es diseñar un sistema cliente-servidor que permita la descarga
de ficheros a partir de URIs. El ejemplo típico será la descarga de clips de audio de YouTube. La
implementación de este proyecto permitirá al alumno trabajar, mediante ZeroC Ice, los siguientes
aspectos:
	
	-  Comunicación asíncrona
	-  Manejo de canales de eventos
	-  Despliegue de servidores de forma dinámica
	-  Gestión de un grid

## Arquitectura del proyecto

El sistema está formado por cinco tipos de componentes: downloaders, encargados de la descargade ficheros;  orchestrators, para la gestión de los  downloaders;  transfers, empleados para latransferencia de archivos; clientes, que solicitarán ficheros; y canales de eventos para mantener unestado coherente entre componentes. Con el objetivo de facilitar el desarrollo de la práctica, laarquitectura descrita se irá desarrollando a lo largo de distintas fases:

	-  FASE 1: Introducción de los Actores
	-  FASE 2: Descarga y sincronización de componentes
	-  FASE 3: El sistema final

### FASE 3: El sistema final

#### PARTE 1: Implementación

En la tercera fase el sistema se compondrá de un  cliente, tres  orchestrators,  una factoría de downloaders y una factoría de transfers. El cliente tendrá que mandar un URL en forma de string a uno de los orchestrators que, a su vez, redirigirá la petición a un downloader creado a tal efecto siempre que el fichero de audio no haya sido descargado previamente en el sistema. El downloader descargará el archivo y notificará que se ha descargado correctamente en un canal de eventos para que todos los orchestrators sepan que el fichero existe, mandando la información de ese fichero. Al terminar se destruirá.

El cliente podrá solicitar la lista de ficheros descargados a uno de los orchestrators.

Además, el cliente también tendrá la opción de pedir la transferencia de un archivo de audio. Harála petición a uno de los *orchestrators* que, a su vez, redirigirá la petición a un transfer creado a tal efecto siempre que el fichero de audio haya sido descargado previamente en el sistema. El transferle mandará directamente al cliente el archivo. Al terminar se destruirá.

Los orchestrators se anunciarán al resto de orchestrators en su creación, que se anunciarán a su vez al nuevo orchestrator para actualizar las listas de orchestrators existentes de cada objeto. Además, un nuevo orchestrator ha de ser consciente de los ficheros de audio que ya han sido descargados en el sistema.

##### Downloader

El downloader es el componente encargado de la descarga de ficheros, y son creados bajo
demanda mediante una factoría de objetos. En esta fase su funcionamiento consiste en:

	- Es creado por una factoría de objetos para poder recibir nuevas peticiones de descarga.
		-> Downloader* create()
		devolverá un objeto downloader ya añadido al adaptador de objetos.
	- Recibe peticiones de descarga.
		-> string addDownloadTask(string url)
		creará la tarea para que el downloader descargue el audio del vídeo por medio de la
		librería youtube-dl.
		-> void newFile(FileInfo fileInfo)
		informará a los orchestrators de que hay un nuevo archivo en el sistema. Nombre del
		topic: UpdateEvents
	- Es destruido al finalizar la descarga.
		-> void destroy()
		eliminará al downloader del adaptador y terminará su ejecución.

##### Transfer

El *transfer* es el componente encargado de la transferencia de ficheros, y son creados bajo
demanda mediante una factoría de objetos. En esta fase su funcionamiento consiste en:

	- Es creado por una factoría de objetos para poder recibir nuevas peticiones de transferencia.
		-> Transfer* create(string fileName)
		devolverá un objeto transfer ya añadido al adaptador de objetos y con el archivo a
		mandar abierto.
	- Recibe peticiones de transferencia.
		-> string recv(int size)
		creará la tarea para que el transfer transfiera el audio deforma similar a como se realiza
		el envío de información por medio de sockets en python.
	- Es destruido al finalizar la descarga.
		-> void close()
		cerrará el archivo que se haya transferido, propio del objeto transfer concreto.
		-> void destroy()
		eliminará al transfer del adaptador y terminará su ejecución.

##### Orchestrator

El *orchestrator* es el componente del sistema que se encarga de la gestión de los downloaders
haciendo de intermediario entre éstos y el cliente. Pueden existir uno o varios y su
funcionamiento en esta fase consiste en:

	- Está siempre a la espera de recibir nuevas peticiones por parte del cliente.
	- Recibe peticiones de descarga que son asignadas a downloaders, después de haber solicitado
	su creación, mediante la función pertinente.
		-> string downloadTask(string url)
		creará una nueva tarea de descarga que enviará a un downloader si el fichero no existe
		ya en el sistema.
	- Recibe peticiones de transferencia que son asignadas a transfers, después de haber solicitado
	su creación, mediante la función pertinente.
		-> Transfer* getFile(string name)
		creará una nueva tarea de transferencia que enviará a un transfer si el fichero existe en el
		sistema.
	- Mantiene listas actualizadas de los ficheros ya descargados en el sistema controlando los
	eventos del canal de actualizaciones UpdateEvents.
		-> FileList getFileList();
		proporcionará la lista de ficheros disponibles (ya descargados e indexados) de todos los
 		downloaders del sistema.
	- Cuando se arranca un nuevo orchestrator saluda al resto de orchestrators, que se anuncian
	al nuevo objeto.
		-> void hello(Orchestrator* me);
		informará a los orchestrators que ya existen en el sistema de que es un nuevo
		orchestrator. Nombre del topic: OrchestratorSync
		-> void announce(Orchestrator* other);
		anunciará cada orchestrator al nuevo orchestrator en el sistema.

##### Cliente

El cliente es el componente del sistema que se conecta a cualquiera de los orchestrators para
solicitar información o la descarga de ficheros. En esta fase solicitará descargas, transferencias o
la lista de ficheros a cualquiera de los orchestrators: recibe una URL como argumento para
descargar, el nombre de un fichero para una transferencia y si no recibe nada lista los ficheros que
hay en el sistema.

##### Ejecución

Deberán lanzarse el registro, la factoría de downloaders, la factoría de transfers y tres orchestrators.
Se comprobará que un cliente puede solicitar descargas, recibir archivos y listar los ficheros del
sistema. Deberán reflejarse los cambios en el lado del servidor: actualización de listas de ficheros,
notificación de nuevos ficheros, notificación de nuevos orchestrators, etc.

#### PARTE 2: Despliegue con IcegridGUI

La imaplementación será modificada para poder desplegarse con IcegridGUI como una aplicación
llamada YoutubeDownloadsApp. El estado final de la configuración de la aplicación se muestra en
la Figura 2. Consiste en:

	- Nodo 1: aloja al registro, a un servidor de IcePatch2 y un servidor de IceStorm.
	- Nodo 2: tres servidores orchestrator definidos por medio de una plantilla.
		▸ Estos servidores deberán pertenecer a un grupo de réplica alcanzable por medio del
		identificador orchestrator.
	- Nodo 3: dos factorías, una de downloaders y otra de transfers, obtenidas de plantillas.
		▸ Los proxies indirectos de estas factorías serán conocidos por los orchestrators.


##### Cliente

Solicitará descargas, transferencias o la lista de ficheros a los orchestrators por medio del ID
orchestrator: recibe una URL como argumento para descargar, el nombre de un fichero para
una transferencia y si no recibe nada lista los ficheros que hay en el sistema.

##### Evaluación

Se harán las mismas comprobaciones que se indicaron en la PARTE 1. Además, el sistema debería
ser completamente funcional en un despliegue en dos hosts: nodos registry-node y
orchestrator-node en el Host 1 y downloads-node en el Host 2.

El .zip entregado ha de contener:

	- client.py: programa cliente.
	- client.config: configuración del cliente.
	- downloader_factory.py: factoría de objetos downloader.
	- transfer_factory.py: factoría de objetos transfer.
	- downloads-node.config: configuración del nodo de descargas.
	- orchestrator.py: programa de los servidores orchestrator.
	- orchestrator-node.config: configuración del nodo de los orchestrators.
	- registry-node.config: configuración del registry y su nodo.
	- trawlnet.ice: interfaz del sistema.
	- YoutubeDownloaderApp.xml: archivo con la configuración de la aplicación en IcegridGUI.
	- README.md: contendrá el enlace al repositorio, los nombres de los alumnos que componen el grupo y el manual de usuario con la especificación de cómo lanzar el sistema.
	- run_client.sh: script para la ejecución del cliente.
	- run_server.sh: script para la ejecución del lado del servidor.
	- Makefile: reglas para la ejecución del sistema.

Los scripts de ejecución y el Makefile serán proporcionados por los profesores. Serán utilizados
para la puesta en marcha del sistema, por lo que éste deberá ajustarse al despliegue que realizan
evitando en la medida de lo posible modificaciones por parte del alumno, salvo en aquellos
apartados en los que se especifique lo contrario.

También podrán entregarse librerías auxiliares (utils.py, por ejemplo).
