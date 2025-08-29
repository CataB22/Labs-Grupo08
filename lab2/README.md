# Integrantes:

| Nombre                   | ROL            | Paralelo |
|--------------------------|--------------  |----------|
| Catalina Jara Broughton  | 202011512-5    |    200   |
| Beatriz Vasquez Cea      | 201904659-4    |    200   |
| Francisco Domínguez      | 202104520-1    |    200   |



## Archivos del Proyecto

- `TCP.py`: Inicia la interacción y se obtienen la frase JOKE y los puertos a utilizar en las siguientes fases.
- `TCP-HTTP.py`: Se le envía el post con el body la frase y el numero de grupo y recibe confirmacion.
- `UDP.py`: Recibe la frase filosofica del servidor.

## Instrucciones de Ejecución

Para ejecutarlo debe iniciar cada servicio en orden del 4 al 1, ya que deben estar listos/escuchando los puertos cuando se inicialice.

Abra en la terminal primero el archivo TCP  para obtener los puertos y la frase JOKE, luego asigne el puerto y la frase en el codigo y ejecute el archivo UDP.py, luego asigne la frase, el grupo y el puerto en el codigo y ejecute el archivo TCP-HTTP.py. Todo esto con el siguiente codigo:

1.  **Terminal 1 (TCP):**
    Este es el cliente TCP.
    ```bash
    python TCP.py
    ```
    - Se le pedira ingresar el comando segun lo que necesite siendo "JOKE" el comando para obtener la frase, GET para obtener los puertos y EXIT para salir del programa.

2.  **Terminal 2 (UDP):**
    Este es el cliente UDP que envía el JOKE al servidor.
    ```bash
    python UDP.py
    ```

3.  **Terminal 3 (HTTP.TCP):**
    Este cliente envia el post HTTP y recibe la confirmacion.
    ```bash
    python TCP-HTTP.py
    ```


