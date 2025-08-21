import socket
from datetime import datetime

# Configuración del servicio 3
HOST_S3 = 'localhost'
PORT_S3_SERVER = 65433  # Puerto para escuchar al servicio 2
HOST_S4 = 'localhost'
PORT_S4_SERVER = 8000  # Puerto del servidor HTTP (servicio 4)

def main():
    """Función principal del servicio 3."""
    start_udp_server(HOST_S3, PORT_S3_SERVER)

def send_http_post(host, port, mensaje):
    """Envía una solicitud HTTP POST con el mensaje en el cuerpo."""
    
    # Construir la solicitud HTTP POST
    request_body = mensaje
    request_line = f"POST / HTTP/1.1\r\n"
    headers = f"Host: {host}:{port}\r\n" \
              f"Content-Type: text/plain\r\n" \
              f"Content-Length: {len(request_body)}\r\n" \
              f"\r\n"
    http_request = request_line + headers + request_body

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(http_request.encode('utf-8'))
        print(f"S3 -> S4 (HTTP POST): {mensaje}")

def start_udp_server(host, port):
    """Inicia un servidor UDP para escuchar mensajes."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Servicio 3 (servidor UDP) escuchando en {host}:{port}")
        
        should_terminate = False
        while not should_terminate:
            data, addr = s.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"S2 -> S3 (UDP) desde {addr}: {message}")

            if "FIN" in message:
                print("Señal de finalización recibida. Terminando Servicio 3.")
                should_terminate = True
                break

            parts = message.strip('[]').split(']-[')
            timestamp, largo_min_str, largo_actual_str, msg = parts[0], parts[1], parts[2], parts[3]
            
            nueva_palabra = input("Ingrese una nueva palabra para agregar: ")
            mensaje_actualizado = f"{msg} {nueva_palabra}"
            largo_actualizado = len(mensaje_actualizado)
            
            new_message = f"[{datetime.now()}]-[{largo_min_str}]-[{largo_actualizado}]-[{mensaje_actualizado}]"
            
            send_http_post(HOST_S4, PORT_S4_SERVER, new_message)
        
        print("Servicio 3 terminado.")

if __name__ == "__main__":
    main()
