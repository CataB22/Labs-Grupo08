import socket
from datetime import datetime

HOST_S2 = 'localhost'
PORT_S2_SERVER = 65432  # S2 recibe de S1 (TCP)
HOST_S3 = 'localhost'
PORT_S3_SERVER = 65433  # S3 recibe de S2 (UDP)

def send_udp_message(host, port, mensaje):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(mensaje.encode('utf-8'), (host, port))
        print(f"S2 -> S3 (UDP): {mensaje}")

def start_tcp_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Servicio 2 (servidor TCP) escuchando en {host}:{port}")

        terminar = False
        while not terminar:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión TCP establecida desde {addr}")
                data = conn.recv(4096).decode('utf-8', errors='replace')
                if not data:
                    continue

                print(f"S1 -> S2 (TCP): {data}")

                # FIN
                if "FIN" in data:
                    print("S2: Señal FIN recibida. Propagando a S3 (UDP) y terminando S2.")
                    send_udp_message(HOST_S3, PORT_S3_SERVER, data)
                    terminar = True
                    break

                # Normal
                try:
                    parts = data.strip('[]').split(']-[')
                    timestamp, largo_min_str, largo_actual_str, mensaje = parts[0], parts[1], parts[2], parts[3]
                except Exception:
                    print("[Error] Mensaje malformado en S2.")
                    continue

                palabra = input("S2: Ingrese una nueva palabra para agregar: ").strip()
                mensaje_actualizado = (mensaje + " " + palabra).strip()
                largo_actualizado = len(mensaje_actualizado)

                new_message = f"[{datetime.now()}]-[{largo_min_str}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
                send_udp_message(HOST_S3, PORT_S3_SERVER, new_message)

        print("Servicio 2 terminado.")

if __name__ == "__main__":
    start_tcp_server(HOST_S2, PORT_S2_SERVER)
