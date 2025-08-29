import socket
HOST = "192.168.1.179"
PORT_UDP = 9001
joke = "¿Sabes por qué se extinguieron los mamuts? Porque faltaban Paputs"

# inicializamos cliente UDP 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Enviar el contenido del JOKE obtenido en el paso anterior
sock.sendto(joke.encode("utf-8"), (HOST, PORT_UDP))

# Esperar respuesta del servidor
data, addr = sock.recvfrom(4096) 
respuesta = data.decode("utf-8", errors="replace")

sock.close()

print("FRASE FILOSÓFICA (UDP)")
print(respuesta)
