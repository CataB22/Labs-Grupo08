import socket

HOST = "192.168.1.179"
PORT = 9000

# creamos socket tcp
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conectamos al servidor
client_socket.connect((HOST, PORT))

#ciclo para solicitar comandos hasta que se ingresa el exit
while True:
    comando = input("Ingrese un comando (GET / JOKE / EXIT): ")
    client_socket.sendall(comando.encode())  

    # recibir respuesta
    data = client_socket.recv(1024).decode()
    print("Servidor:", data)

    if comando == "EXIT":
        print("Cerrando cliente...")
        break

client_socket.close()
