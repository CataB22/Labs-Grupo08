from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from datetime import datetime
import os

HOST_S4 = 'localhost'
PORT_S4_SERVER = 8000
HOST_S1 = 'localhost'
PORT_S1_SERVER = 65431
MSG_FINAL = "mensaje.txt"

def send_tcp_message(host, port, mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(mensaje.encode('utf-8'))
            print(f"S4 -> S1 (TCP): {mensaje}")
    except Exception as e:
        print(f"[S4] Error enviando a S1: {e}")

def handle_message(mensaje):
    """Decide si continuar o finalizar. Si finaliza, guarda y envía FIN a S1."""
    try:
        parts = mensaje.strip('[]').split(']-[')
        # partes: 0 ts, 1 Lmin, 2 Lact, 3 msg
        largo_min = int(parts[1]); largo_act = int(parts[2]); msg = parts[3]
    except Exception:
        print("[S4] Mensaje malformado.")
        return

    if largo_act >= largo_min:
        final_message_log = f"[{datetime.now()}]-[{msg}]"
        with open(MSG_FINAL, "a", encoding="utf-8") as f:
            f.write(final_message_log + "\n")
        print(f"[S4] Mensaje final guardado en {MSG_FINAL}.")

        termination_message = f"[{datetime.now()}]-[FIN]"
        print("[S4] Disparando FIN...")
        send_tcp_message(HOST_S1, PORT_S1_SERVER, termination_message)
        # cerrar limpio el servidor deteniendo serve_forever (ver do_POST)
        return "FIN"
    else:
        nueva = input("S4: Ingrese una nueva palabra para agregar: ").strip()
        mensaje_actualizado = (msg + " " + nueva).strip()
        largo_actualizado = len(mensaje_actualizado)
        new_message = f"[{datetime.now()}]-[{largo_min}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
        send_tcp_message(HOST_S1, PORT_S1_SERVER, new_message)
        return "CONTINUE"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(content_length).decode('utf-8', errors='replace')
        except Exception:
            self.send_response(400); self.end_headers()
            return

        print(f"S3 -> S4 (HTTP POST): {body}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

        if "FIN" in body:
            # Si S3 alguna vez propagara FIN por HTTP se pasam a S1 y cerramos.
            send_tcp_message(HOST_S1, PORT_S1_SERVER, body)
            # Cierre del servidor
            self.server.shutdown()
            return

        result = handle_message(body)
        if result == "FIN":
            # Detener el HTTPServer para terminar S4
            self.server.shutdown()

def run_server():
    httpd = HTTPServer((HOST_S4, PORT_S4_SERVER), SimpleHTTPRequestHandler)
    print(f"Servicio 4 (HTTP) escuchando en {HOST_S4}:{PORT_S4_SERVER}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Servicio 4 terminado.")

if __name__ == "__main__":
    run_server()
