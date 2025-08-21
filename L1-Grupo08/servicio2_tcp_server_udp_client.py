import socket
import datetime
import sys

def servicio2():
    # Configurar servidor TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind(('localhost', 8001))
    tcp_socket.listen(1)
    
    print("=== Servicio 2 (TCP Server/UDP Client) ===")
    print("Esperando conexión del Servicio 1...")
    
    try:
        while True:
            conn, addr = tcp_socket.accept()
            with conn:
                print(f"Conexión establecida desde: {addr}")
                
                data = conn.recv(1024)
                if not data:
                    continue
                
                mensaje_recibido = data.decode('utf-8')
                print(f"Mensaje recibido: {mensaje_recibido}")
                
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
                
                # Enviar al Servicio 3 via UDP
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    udp_socket.sendto(nuevo_formato.encode('utf-8'), ('localhost', 8002))
                    print(f"Mensaje enviado al Servicio 3: {nuevo_formato}")
                finally:
                    udp_socket.close()
                    
    except KeyboardInterrupt:
        print("\nCerrando Servicio 2...")
    finally:
        tcp_socket.close()

if __name__ == "__main__":
    servicio2()