import socket
from datetime import datetime
import time

HOST_S1 = 'localhost'
PORT_S1_SERVER = 65431  # S1 escucha a S4 (TCP)
HOST_S2 = 'localhost'
PORT_S2_SERVER = 65432  # S2 escucha a S1 (TCP)

def send_tcp_message(host, port, mensaje, max_retries=30, delay=1.0):
    """Envía un mensaje TCP con reintentos controlados (no recursivo)."""
    for intento in range(1, max_retries + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(mensaje.encode('utf-8'))
                print(f"S1 -> S2 (TCP): {mensaje}")
                return True
        except ConnectionRefusedError:
            print(f"No se pudo conectar a {host}:{port}. Reintentando en {delay}s... (intento {intento}/{max_retries})")
            time.sleep(delay)
        except Exception as e:
            print(f"[Error TCP] {e}")
            time.sleep(delay)
    print("[Error] No se pudo conectar tras múltiples intentos.")
    return False

def start_tcp_server(host, port):
    """Escucha mensajes entrantes desde S4 y los procesa."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Servicio 1 (servidor) escuchando en {host}:{port}")

        should_terminate = False
        while not should_terminate:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión TCP establecida desde {addr}")
                data = conn.recv(4096).decode('utf-8', errors='replace')
                if not data:
                    continue

                print(f"S4 -> S1 (TCP): {data}")

                # Señal de finalización
                if "FIN" in data:
                    print("Señal de finalización recibida en S1. Reenviando a S2 y cerrando...")
                    send_tcp_message(HOST_S2, PORT_S2_SERVER, data)
                    should_terminate = True
                    break

                # Mensaje normal
                try:
                    parts = data.strip('[]').split(']-[')
                    timestamp, largo_min_str, largo_actual_str, mensaje = parts[0], parts[1], parts[2], parts[3]
                except Exception:
                    print("[Error] Mensaje malformado recibido en S1.")
                    continue

                nueva_palabra = input("S1: Ingrese una nueva palabra para agregar: ").strip()
                mensaje_actualizado = (mensaje + " " + nueva_palabra).strip()
                largo_actualizado = len(mensaje_actualizado)

                new_message = f"[{datetime.now()}]-[{largo_min_str}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
                send_tcp_message(HOST_S2, PORT_S2_SERVER, new_message)

        print("Servicio 1 terminado.")

def servicio1():
    # Inicio: pedir datos y enviar primer mensaje a S2
    largo_minimo = input("Ingrese el largo mínimo del mensaje final: ").strip()
    palabra_inicial = input("Ingrese la palabra inicial: ").strip()

    mensaje_inicial = f"[{datetime.now()}]-[{largo_minimo}]-[{len(palabra_inicial)}]-[{palabra_inicial}]"
    send_tcp_message(HOST_S2, PORT_S2_SERVER, mensaje_inicial)

    # escuchando a S4
    start_tcp_server(HOST_S1, PORT_S1_SERVER)

if __name__ == "__main__":
    servicio1()
