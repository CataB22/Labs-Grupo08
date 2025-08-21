from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from datetime import datetime
import os

# Configuración del servicio 4
HOST_S4 = 'localhost'
PORT_S4_SERVER = 8000
HOST_S1 = 'localhost'
PORT_S1_SERVER = 65431
MSG_FINAL = "mensaje.txt"

def send_tcp_message(host, port, mensaje):
    """Envía un mensaje a través de una conexión TCP."""
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

    if largo_actual_str >= largo_min_str:
        # Largo mínimo alcanzado, guardar y finalizar
        final_message_log = f"[{datetime.now()}]-[{msg}]"
        with open(MSG_FINAL, "a") as f:
            f.write(final_message_log + "\n")
        print(f"Mensaje final guardado en {MSG_FINAL}.")

        # Iniciar finalización
        termination_message = f"[{datetime.now()}]-[FIN]"
        send_tcp_message(HOST_S1, PORT_S1_SERVER, termination_message)
        print("Iniciando finalización de servicios...")
        print("Terminando Servicio 4.")
        # Salida forzada del programa
        os._exit(0)
    else:
        # Continuar el ciclo
        nueva_palabra = input("Ingrese una nueva palabra para agregar: ")
        mensaje_actualizado = f"{msg} {nueva_palabra}"
        largo_actualizado = len(mensaje_actualizado)
        
        new_message = f"[{datetime.now()}]-[{largo_min_str}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
        
        send_tcp_message(HOST_S1, PORT_S1_SERVER, new_message)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Manejador de solicitudes HTTP para el servicio 4."""
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        print(f"S3 -> S4 (HTTP POST): {body}")
        self.send_response(200)
        self.end_headers()

        # Procesar el mensaje
        if "FIN" in body:
            print("Señal de finalización recibida. Iniciando apagado en cadena.")
            send_tcp_message(HOST_S1, PORT_S1_SERVER, body)
            print("Terminando Servicio 4.")
            # Salida forzada del programa
            os._exit(0)
        else:
            handle_message(body)

def run_server():
    """Versión básica con HTTPServer estándar."""
    server_address = ('', PORT_S4_SERVER)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Servicio 4 (servidor HTTP básico) escuchando en el puerto {PORT_S4_SERVER}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando servidor por interrupción de teclado.")
        httpd.server_close()
        print("Servicio 4 terminado.")

if __name__ == "__main__":
    run_server()
