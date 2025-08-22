from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from datetime import datetime
import os
import time

#Configuración variables del servicio 4 (hosts, puertos y variable con nombre de archivo final)
HOST_S4 = 'localhost'
PORT_S4_SERVER = 8000
HOST_S1 = 'localhost'
PORT_S1_SERVER = 65431
MSG_FINAL = "mensaje.txt"

def send_tcp_message(host, port, mensaje):
    #Envía un mensaje a través de una conexión TCP.(misma logica que el servicio 1)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(mensaje.encode('utf-8'))
            print(f"S4 -> S1 (TCP): {mensaje}")
    except ConnectionRefusedError:
        print(f"Error: No se pudo conectar a {host}:{port} para enviar el mensaje de finalización.")

def handle_message(mensaje):
    """Procesa el mensaje recibido, decide si continuar o finalizar."""
    parts = mensaje.strip('[]').split(']-[')
    timestamp, largo_min_str, largo_actual_str, msg = parts[0], int(parts[1]), int(parts[2]), parts[3]
    if largo_min_str <= largo_actual_str:
        #si el largo actual es mayor o igual al largo minimo, guardar y finalizar
        log_msg = f"[{datetime.now()}]-[{msg}]"
        with open(MSG_FINAL, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
        print(f"[S4]Mensaje final guardado en {MSG_FINAL}.")

        # Iniciar finalización
        msg_finalizacion = f"[{datetime.now()}]-[FIN]"
        send_tcp_message(HOST_S1, PORT_S1_SERVER, msg_finalizacion)
        print("[S4] Iniciando finalización de servicios...")
        # cerrar limpio el servidor deteniendo serve_forever (ver do_POST)
        return "FIN"
    else:
        # Continuar el ciclo
        nueva_palabra = input("S4: Ingrese una nueva palabra para agregar: ").strip()
        mensaje_actualizado = f"{msg} {nueva_palabra}".strip()
        largo_actualizado = len(mensaje_actualizado)
        new_message = f"[{datetime.now()}]-[{largo_min_str}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
        send_tcp_message(HOST_S1, PORT_S1_SERVER, new_message)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
            try:
                content_length = int(self.headers.get('Content-Length', '0'))
                body = self.rfile.read(content_length).decode('utf-8', errors='replace')
            except Exception:
                self.send_response(400); self.end_headers()
                return

            print(f"S3 -> S4 (HTTP POST): {body}")

            if "FIN" in body:
                # Si S3 alguna vez propagara FIN por HTTP se pasam a S1 y cerramos.
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"FIN_RECEIVED")
                send_tcp_message(HOST_S1, PORT_S1_SERVER, body)
                # Cierre del servidor
                self.server.shutdown()
                return

            result = handle_message(body)
            if result == "FIN":
                try:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"FINAL")
                    time.sleep(0.1)  # Dar tiempo para enviar respuesta, sino puede generar error
                except ConnectionAbortedError:
                    print("[S4] Conexión cerrada por cliente durante respuesta OK.")
                finally:
                    print("[S4] Cerrando servidor HTTP...")
                    self.server.shutdown()
            else:
                try:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"OK")
                except ConnectionAbortedError:
                    print("[S4] Conexión cerrada por cliente, pero servidor continúa funcionando.")

def run_server():
    httpd = HTTPServer((HOST_S4, PORT_S4_SERVER), SimpleHTTPRequestHandler)
    print(f"Servicio 4 escuchando en el puerto {PORT_S4_SERVER}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Cerrando servidor por una interrupción de teclado.")
    finally:
        httpd.server_close()
        print("Servicio 4 terminado.")

if __name__ == "__main__":
    run_server()
