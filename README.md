# Integrantes:

| Nombre                   | ROL            | Paralelo |
|--------------------------|--------------  |----------|
| Catalina Jara Broughton  | 202011512-5    |    200   |
| Beatriz Vasquez Cea      | 201904659-4    |    200   |
| Francisco Domínguez      | 202104520-1    |    200   |



## Archivos del Proyecto

- `servicio1.py`: Inicia la interacción y se comunica con el servicio 2 (TCP) y 4 (TCP).
- `servicio2.py`: Recibe de S1 (TCP) y envía a S3 (UDP).
- `servicio3.py`: Recibe de S2 (UDP) y envía a S4 (HTTP POST).
- `servicio4.py`: Servidor HTTP que recibe de S3, evalúa la frase y se comunica con S1 (TCP).

## Instrucciones de Ejecución

Para ejecutarlo debe iniciar cada servicio en orden del 4 al 1, ya que deben estar listos/escuchando los puertos cuando se inicialice.

Abra 4 terminales separadas en el directorio del proyecto y ejecute los siguientes comandos en el orden especificado:

1.  **Terminal 1 (Iniciar Servicio 4):**
    Este es el servidor HTTP, debe estar listo para recibir la primera solicitud.
    ```bash
    python servicio4.py
    ```

2.  **Terminal 2 (Iniciar Servicio 3):**
    Este servicio espera mensajes UDP del servicio 2.
    ```bash
    python servicio3.py
    ```

3.  **Terminal 3 (Iniciar Servicio 2):**
    Este servicio espera conexiones TCP del servicio 1.
    ```bash
    python servicio2.py
    ```

4.  **Terminal 4 (Iniciar Servicio 1 y solicitud de largo y palabra inicial):**
    ```bash
    python servicio1.py
    ```
    - Se le pedirá que ingrese el **largo mínimo** para la frase final.
    - Se le pedirá que ingrese la **palabra inicial** de la frase.

Una vez iniciado, el juego comenzará. Cada terminal (excepto la del servicio 4 al principio) le pedirá que ingrese una nueva palabra cuando sea su turno en la cadena.

El juego termina cuando la longitud de la frase acumulada supera o iguala el largo mínimo especificado al inicio. El mensaje final se guardará en un archivo de texto llamado `.txt`y luego los servicios se apagan en cadena.

## Consideraciones y supuestos
-Se asume que el usuario siempre ingresará una palabra cuando se solicite y no dejará el mensaje en blanco.
-Se entiende que se agregan palabras, por lo que cada palabra que se ingrese se le agrega un espacio para separar cada palabra ingresada(espacio que es considerado en el largo del mensaje).
-Se asume que siempre ingresaran un largo minimo del mensaje cuando se solicita al inicio.
-Servicio4 es el que maneja la finalizacion del programa. por lo que cuando el mensaje le llegue a el se verifica si termina o no.