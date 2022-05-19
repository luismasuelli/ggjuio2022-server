GGJUIO 2022 Server
==================

Miniserver para montar el juego del GameJam 2022 en Quito.

Requisitos
----------

1. Linux, o activar el WSL en Windows 10 u 11.
2. Docker instalado (la versión gratis es la que más se usa y va re bien).
3. Python y, preferentemente, virtualenv.

Cómo se usa
-----------

1. Levantamos el server de MongoDB primero, invocando el script en development/sample-mongo.sh. Esto nos ocupa el puerto 27017.
2. Instalamos los requerimientos para el server (tal vez es buena idea hacer esto dentro de un virtualenv): pip install -r requirements.py.
3. Corremos el server (también dentro del mismo virtualenv, si estamos usando): python server.py.

Documentación
-------------

Este tiene un modelo choto de usuarios (una tabla de usuarios con nickname, password, login y las misiones). Usa la arquitectura de [Almacenamiento Remoto Estándar
](https://github.com/AlephVault/standard-http-mongodb-storage).
