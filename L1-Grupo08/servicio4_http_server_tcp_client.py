import socket
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json

class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/mensaje':
            content_length = int(self.headers['Content-Length'])
            post_data = self.r.read(content_length).decode('utf-8')
            
            print(f"Mensaje recibido via HTTP: {post_data}")
            
            # Procesar mensaje
            self.procesar_mensaje(post_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Mensaje recibido correctamente")
        else:
            self.send_response(404)
            self.end_headers()
    
    def procesar_mensaje(self, mensaje):
        partes = mensaje.split('-', 3)
        if len(partes) < 4:
            print("Formato de mensaje incorrecto")
            return
        
        timestamp, largo_minimo_str, largo_actual_str, mensaje_texto = partes
        
        try:
            largo_minimo = int(largo_minimo_str)
            largo_actual = int(largo_actual_str)
        except ValueError:
            print("Error en formato de números")
            return
        
        # Verificar si cumple con el largo mínimo
        if largo_actual >= largo_minimo:
            print(f"Mensaje cumple con largo mínimo ({largo_actual}/{largo_minimo})")
            # Guardar en archivo
            with open('mensaje_final.txt', 'a', encoding='utf-8') as f:
                f.write(f"{timestamp}: {mensaje_texto}\n")
            
            # Iniciar cadena de finalización
            self.iniciar_finalizacion()
        else:
            print(f"Mensaje no cumple con largo mínimo ({largo_actual}/{largo_minimo})")
            # Solicitar nueva palabra y enviar al Servicio 1
            nueva_palabra = input("Ingrese una nueva palabra para agregar: ")
            mensaje_actualizado = f"{mensaje_texto} {nueva_palabra}"
            largo_actual_actualizado = len(mensaje_actualizado)
            
            nuevo_timestamp = datetime.datetime.now().isoformat()
            nuevo_formato = f"{nuevo_timestamp}-{largo_minimo}-{largo_actual_actualizado}-{mensaje_actualizado}"
            
            # Enviar al Servicio 1 via TCP
            self.enviar_a_servicio1(nuevo_formato)
    
    def enviar_a_servicio1(self, mensaje):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 8000))  # Puerto del Servicio 1
                s.sendall(mensaje.encode('utf-8'))
                print(f"Mensaje enviado al Servicio 1: {mensaje}")
        except Exception as e:
            print(f"Error enviando a Servicio 1: {e}")
    
    def iniciar_finalizacion(self):
        timestamp = datetime.datetime.now().isoformat()
        mensaje_fin = f"{timestamp}-FIN"
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 8000))  # Enviar FIN al Servicio 1
                s.sendall(mensaje_fin.encode('utf-8'))
                print("Señal FIN enviada al Servicio 1")
        except Exception as e:
            print(f"Error enviando señal FIN: {e}")

def run_http_server():
    server = HTTPServer(('localhost', 8003), HTTPHandler)
    print("=== Servicio 4 (HTTP Server/TCP Client) ===")
    print("Servidor HTTP iniciado en puerto 8003")
    server.serve_forever()

if __name__ == "__main__":
    # Iniciar servidor HTTP en hilo separado
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Mantener el programa principal ejecutándose
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nCerrando Servicio 4...")