import socket
from datetime import datetime
import time

# Configuración variables del servicio 1 (host, puertos)
HOST_S1 = 'localhost'
PORT_S1_SERVER = 65431
PORT_S2_SERVER = 65432 


def send_tcp_message(host, port, mensaje):
    #Envía un mensaje a través de una conexión TCP.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(mensaje.encode('utf-8'))
            print(f"S1 -> S2 (TCP): {mensaje}")
    except ConnectionRefusedError:
        print(f"Error: No se pudo conectar a {host}:{port}. Asegúrese de que el servicio 2 esté en ejecución.")

def start_tcp_server(host, port):
    #Inicia un servidor TCP para escuchar conexiones entrantes
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servicio 1 (servidor) escuchando en {host}:{port}")
        
        should_terminate = False
        while not should_terminate:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión TCP establecida desde {addr}")
                data = conn.recv(4096).decode('utf-8')
                if not data:
                    continue
                
                print(f"S4 -> S1 (TCP): {data}")
                
                if "FIN" in data:
                    print("Señal de finalización recibida. Reenviando a Servicio 2 y terminando.")
                    send_tcp_message(HOST_S1, PORT_S2_SERVER, data)
                    should_terminate = True
                    break

                parts = data.strip('[]').split(']-[')
                timestamp, largo_min_str, largo_actual_str, mensaje = parts[0], parts[1], parts[2], parts[3]
                
                nueva_palabra = input("Ingrese una nueva palabra para agregar: ").strip()
                mensaje_actualizado = f"{mensaje} {nueva_palabra}"
                largo_actualizado = len(mensaje_actualizado)
                
                new_message = f"[{datetime.now()}]-[{largo_min_str}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
                
                # enviar al servicio 2
                send_tcp_message(HOST_S1, PORT_S2_SERVER, new_message)
        
        print("Servicio 1 terminado.")

def servicio1():
    largo_minimo = int(input("Ingrese el largo mínimo del mensaje final: "))
    palabra_inicial = input("Ingrese la palabra inicial: ").strip()

    mensaje = f"[{datetime.now()}]-[{largo_minimo}]-[{len(palabra_inicial)}]-[{palabra_inicial}]"

    # envia el mensaje inicial al servicio 2 S2 (cliente TCP)
    send_tcp_message(HOST_S1, PORT_S2_SERVER, mensaje)

    # inicia el servidor para "escuchar" al servicio 4 S4
    start_tcp_server(HOST_S1, PORT_S1_SERVER)

if __name__ == "__main__":
    servicio1()
