import socket
import datetime
import sys

def enviar_http_request(mensaje):
    """Enviar solicitud HTTP al Servicio 4"""
    http_request = (
        f"POST /mensaje HTTP/1.1\r\n"
        f"Host: localhost:8003\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(mensaje)}\r\n"
        f"\r\n"
        f"{mensaje}"
    )
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 8003))
            s.sendall(http_request.encode('utf-8'))
            
            # Recibir respuesta (opcional)
            response = s.recv(1024)
            print(f"Respuesta HTTP recibida: {response.decode('utf-8')}")
            
    except Exception as e:
        print(f"Error enviando HTTP request: {e}")

def servicio3():
    # Configurar servidor UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('localhost', 8002))
    
    print("=== Servicio 3 (UDP Server/HTTP Client) ===")
    print("Esperando mensajes UDP...")
    
    try:
        while True:
            data, addr = udp_socket.recvfrom(1024)
            mensaje_recibido = data.decode('utf-8')
            print(f"Mensaje recibido de {addr}: {mensaje_recibido}")
            
            # Parsear mensaje
            partes = mensaje_recibido.split('-', 3)
            if len(partes) < 4:
                print("Formato de mensaje incorrecto")
                continue
            
            timestamp, largo_minimo, largo_actual, mensaje = partes
            
            # Solicitar nueva palabra
            nueva_palabra = input("Ingrese una nueva palabra para agregar: ")
            mensaje_actualizado = f"{mensaje} {nueva_palabra}"
            largo_actual_actualizado = len(mensaje_actualizado)
            
            # Crear nuevo mensaje
            nuevo_timestamp = datetime.datetime.now().isoformat()
            nuevo_formato = f"{nuevo_timestamp}-{largo_minimo}-{largo_actual_actualizado}-{mensaje_actualizado}"
            
            # Enviar al Servicio 4 via HTTP
            print(f"Enviando a Servicio 4: {nuevo_formato}")
            enviar_http_request(nuevo_formato)
            
    except KeyboardInterrupt:
        print("\nCerrando Servicio 3...")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    servicio3()