import socket
import datetime
import sys

def servicio1():
    # Solicitar datos iniciales
    print("=== Servicio 1 (TCP Client) ===")
    largo_minimo = input("Ingrese el largo mínimo del mensaje final: ")
    palabra_inicial = input("Ingrese la palabra inicial: ")
    
    # Crear mensaje inicial
    timestamp = datetime.datetime.now().isoformat()
    mensaje = palabra_inicial
    largo_actual = len(mensaje)
    
    formato_mensaje = f"{timestamp}-{largo_minimo}-{largo_actual}-{mensaje}"
    
    # Conectar al Servicio 2 via TCP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 8001))  # Puerto del Servicio 2
            s.sendall(formato_mensaje.encode('utf-8'))
            print(f"Mensaje enviado al Servicio 2: {formato_mensaje}")
            
            # Esperar respuesta o señal de finalización
            data = s.recv(1024)
            if data:
                mensaje_recibido = data.decode('utf-8')
                if "FIN" in mensaje_recibido:
                    print("Señal de finalización recibida. Cerrando conexiones...")
                else:
                    print(f"Mensaje recibido: {mensaje_recibido}")
                    
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al Servicio 2")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    servicio1()