# Práctica 1: Uso de Hydra para romper contraseñas en un servidor web sencillo

En esta práctica vamos a aprender cómo usar Hydra, una herramienta de fuerza bruta, para romper contraseñas de un servidor web simple. Este servidor se ejecutará en Python y tendrá cinco niveles, cada uno con un inicio de sesión. El objetivo es comprender cómo utilizar Hydra dentro de Kali Linux en WSL (Windows Subsystem for Linux), conectándose a un servidor web que se ejecuta en el sistema local.

## 1. Instalación y configuración del entorno
Para hacer funcionar todo el entorno es necesario realizar unas instalaciones previas, además de verificar que todo funciona correctamente. 

### 1.1. Instalar WSL
WSL (Windows Subsystem for Linux) es una característica de Windows que permite ejecutar distribuciones de Linux directamente en Windows, sin necesidad de máquinas virtuales o dual boot. Proporciona un entorno compatible con Linux dentro de Windows, permitiendo usar herramientas y software de Linux como si estuvieran corriendo nativamente en el sistema operativo de Microsoft.
Para instalar WSL en Windows, seguimos estos pasos:
1. Abrimos PowerShell como administrador y ejecutamos el siguiente comando:

~~~
wsl --install
~~~

2. Le indicamos a WSL que use la versión 2:
~~~
wsl --set-default-version 2
~~~

3. Tras instalar WSL, marcamos las opciones Plataforma de máquina virtual, `Plataforma del hipervisor de Windows y Subsistema de Windows para Linux` en las características de Windows (si no las teníamos marcadas ya). Por último aceptamos y reiniciamos el equipo:

4. Para verificar que está instalado correctamente, pulsamos en cualquier ubicación del equipo Shift+Click derecho y debería aparecer la opción “Abrir shell de Linux aquí”

### 1.2. Instalar Kali Linux
Kali Linux es una distribución de Linux especializada en pruebas de penetración y seguridad informática. Viene con una gran cantidad de herramientas preinstaladas para realizar auditorías de seguridad, como escaneos de vulnerabilidades, ataques de fuerza bruta, análisis de redes, y más. Es ampliamente utilizada por profesionales de ciberseguridad.
Para instalar Kali, sigue los siguientes pasos:

1. Desde Microsoft Store, busca e instala Kali Linux.
2. Una vez instalado, abre Kali Linux desde el menú de inicio de Windows. Si instalamos WSL correctamente, la primera vez que iniciamos Kali nos pedirá que introduzcamos un nombre de usuario y una contraseña. Es muy importante no olvidar estos credenciales ya que pueden ser necesarios más adelante.

### 1.4. Instalar Hydra
Hydra es una herramienta de ataque por fuerza bruta que nos permite probar contraseñas de un servicio remoto. Es muy potente y soporta múltiples protocolos como HTTP, FTP, SSH, entre otros.

En esta práctica, vamos a usar Hydra para realizar un ataque contra el servidor web que hemos configurado. El ataque puede realizarse de dos formas:
Usando diccionarios de usuarios y/o contraseñas.
Usando fuerza bruta con combinaciones de contraseñas generadas por Hydra.

Hydra debería venir directamente instalado en Kali Linux. Para comprobarlo, ejecutamos el comando hydra en Kali y deberíamos ver una salida similar a la siguiente:

En caso de que Hydra no esté instalado y se muestre un error, simplemente ejecutamos el siguiente comando para instalar el paquete:
~~~
sudo apt install hydra
~~~

### 1.5. Instalar Python

Para instalar Python en Windows, seguimos los siguientes pasos:
1. Descargamos el instalador de aquí https://www.python.org/downloads/ (versión 3.13.0)
2. Seguimos los pasos del instalador, y cuando ha terminado verificamos que se ha instalado correctamente escribiendo el comando `python` en un cmd:

3. Si en lugar de abrir la consola de Python nos redirige a la Windows Store, tenemos que verificar que las variables de entorno están configuradas correctamente:

## 2. Clonado del servidor y la página web

Para lanzar el servidor en local, seguimos los siguientes pasos:
1. Clonamos este repositorio.
2. El código fuente se encuentra en la carpeta `source`. En dicha carpeta ejecutamos el siguiente comando:
~~~
python server.py
~~~
3. Si entramos a `localhost:8000` podremos acceder a la página.

## 3.  Clonado del repositorio de SecLists
SecLists es un repositorio de listas de contraseñas y nombres de usuario muy utilizado para pruebas de penetración. Vamos a clonar este repositorio para obtener los diccionarios que vamos a utilizar con Hydra:
1. Ejecutamos en Kali el comando:

~~~
git clone https://github.com/danielmiessler/SecLists.git
~~~

2. Una vez clonado, podemos ver la estructura del repositorio. Hay una carpeta Users con diferentes listas de usuarios, y otra Passwords con contraseñas:

## 4. Realizando el ataque con Hydra

### 4.1 Uso de diccionarios

A continuación vamos a ver cuál sería la sintaxis del comando necesario para usar diccionarios:
~~~
hydra -l/-L [RutaFicheroUsuarios / Usuario directamente] -P [RutaFicheroContraseñas] [IP] -s [Puerto] http-post-form "/:[Parámetros del formulario en formato JSON]:F=[Mensaje de error]" -f
~~~

💡Asegúrate de usar correctamente -l o -L según corresponda.

Un ejemplo atacando a `localhost:1234` teniendo campo username (que siempre es “user” ) y password, y que devuelve un error que contiene la palabra “incorrecto” sería:

~~~
hydra -l user -P SecLists/Passwords/Leaked-Databases/rockyou-20.txt 127.0.0.1 -s 1234http-post-form "/:{\"username\":\"user\",\"password\":\"^PASS^\"}:F=incorrecto" -f
~~~

Explicación del comando:
* -l user: Especifica el usuario que vamos a usar en el ataque (en este caso, `user`).
* -P SecLists/Passwords/Leaked-Databases/rockyou-20.txt: Indica el diccionario de contraseñas a usar. En este caso, el archivo rockyou-20.txt que hemos clonado desde SecLists.
* 127.0.0.1: Es la dirección IP de la máquina que ejecuta el servidor Python, que hemos obtenido previamente.
* -s 1234: El puerto en el que el servidor web está escuchando (puede variar según la configuración del servidor).
* http-post-form "/:{\"username\":\"user\",\"password\":\"^PASS^\"}:F=Invalid": Indica que Hydra debe realizar un ataque POST a la página de inicio de sesión del servidor, pasando el usuario y las contraseñas en el formulario.
* -f: Indica que Hydra debe detenerse en el momento en elq ue encuentre la primera contraseña válida.

### 4.1 Uso de combinaciones de caracteres

Si no tenemos un diccionario adecuado o preferimos generar combinaciones de contraseñas, podemos usar el modo de fuerza bruta. El comando sería el siguiente:

~~~
hydra -l user -x 
[NúmeroMínimoCaracteres:NúmeroMáximoCaracteres:Charset] [IP] -s [Puerto] http-post-form "/:[Parámetros del formulario en formato JSON]:F=[Mensaje de error]" -f
~~~

Las opciones para el valor Charset son las siguientes:
* a: incluye letras minúsculas (a-z).
* A: incluye letras mayúsculas (A-Z).
* 1: incluye números (0-9).
* s: incluye caracteres especiales (!@#$%^&*(), etc.).
* b: incluye todos los caracteres de ASCII (más amplio que solo letras y números).

Por ejemplo, si sabemos que la contraseña tiene 5 caracteres y solo está compuesta por letras minúsculas y números usaríamos el siguiente comando:

~~~
hydra -l user -x 5:5:a1 127.0.0.1 -s 1234 http-post-form "/:{\"username\":\"user\",\"password\":\"^PASS^\"}:F=Invalid" -f
~~~

Explicación del comando:
* -l user: Especifica el usuario a usar.
* -x 5:5:a1: Especifica el rango y tipo de caracteres que se generarán en la fuerza bruta. En este caso, genera contraseñas de 5 caracteres de largo que pueden contener letras (mayúsculas y minúsculas) y números.
* El resto de parámetros son los mismos que en el comando anterior.

## Consideraciones y herramientas útiles

### WSL y Windows

Cuando trabajamos con WSL y tratamos de acceder a localhost (127.0.0.1) desde dentro de WSL, el tráfico hacia localhost no siempre se enruta correctamente debido a cómo Windows y WSL manejan las redes de forma aislada. Esto significa que el localhost de Windows no es directamente accesible desde WSL.
Para solucionar esto, debemos usar la IP que muestra el siguiente comando (en WSL/Kali):

~~~~
ip route | grep default
~~~~

Esta IP es la dirección de la interfaz de red qde WSL que está directamente conectada a la red local.

### CeWL

CeWL (Custom Word List generator) es una herramienta capaz de generar diccionarios personalizados para usar en ataques de fuerza bruta. Para ello recopila todas las palabras mencionadas en un determinado sitio web. Su sintaxis es la siguiente:

~~~~
cewl [opciones] <URL>
~~~~

Pudiendo ser las opciones las siguientes:
* -w <archivo>: Especifica el archivo de salida para guardar la lista de palabras generada.
* -d <n>: Define la profundidad de la búsqueda en el sitio web (cuántos enlaces seguir, por defecto es 2).
* -m <n>: Establece la longitud mínima de las palabras (por ejemplo, -m 5 para solo palabras de 5 caracteres o más).


## 5. Verificación y evaluación
Teniendo todo el entorno instalado y sabiendo cómo funciona Hydra, es el momento de intentar averiguar las cinco contraseñas de cada nivel. En cada uno de ellos encontrarás diferentes pistas para acotar los intentos hechos por Hydra. 

La entrega de esta práctica debe ser un fichero en formato PDF con capturas del comando realizado y su salida (únicamente si se ha logrado romper la contraseña, los demás comandos ejecutados se consideran intentos que no son necesario documentar).


