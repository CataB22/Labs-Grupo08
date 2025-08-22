import socket
from datetime import datetime

# Configuración variables del servicio 2 (hosts, puertos)
HOST_S2 = 'localhost'
PORT_S2_SERVER = 65432  # Puerto para escuchar/recibir al servicio 1
HOST_S3 = 'localhost'
PORT_S3_SERVER = 65433  # Puerto del servicio 3. S2 envia a S3

def send_udp_message(host, port, mensaje):
    #Envía un mensaje a través de una conexión UDP.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(mensaje.encode('utf-8'), (host, port))
        print(f"S2 -> S3 (UDP): {mensaje}")

def start_tcp_server(host, port):
    #Inicia un servidor TCP para recibir las conexiones entrantes.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servicio 2 (servidor TCP) escuchando en {host}:{port}")
        bool_finalizar = False
        while not bool_finalizar:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión TCP establecida desde {addr}")
                data = conn.recv(4096).decode('utf-8')
                if not data:
                    continue
                
                print(f"S1 -> S2 (TCP): {data}")

                # Procesamos mensaje de finalización
                if "FIN" in data:
                    print("Señal de finalización recibida. Reenviando a Servicio 3.")
                    send_udp_message(HOST_S3, PORT_S3_SERVER, data)
                    print("Terminando Servicio 2.")
                    bool_finalizar = True
                    break

                # Procesamos mensaje normal
                parts = data.strip('[]').split(']-[')
                timestamp, largo_min_str, largo_actual_str, mensaje = parts[0], parts[1], parts[2], parts[3]
                
                palabra = input("S2: Ingrese una nueva palabra para agregar: ")
                mensaje_actualizado = f"{mensaje} {palabra}".strip()
                largo_actualizado = len(mensaje_actualizado)
                
                new_message = f"[{datetime.now()}]-[{largo_min_str}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
                
                send_udp_message(HOST_S3, PORT_S3_SERVER, new_message)
        
        print("Servicio 2 terminado.")

if __name__ == "__main__":
    start_tcp_server(HOST_S2, PORT_S2_SERVER)
