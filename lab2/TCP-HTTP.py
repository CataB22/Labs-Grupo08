import socket
host = '192.168.1.179'
port = 1080

frase = 'Que es el ser sin la mitad faltante'
grupo_id = 8

body = f"frase={frase} y grupo={grupo_id}"

solicitud_http = (
    f"POST /frase/ HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    f"Content-Type: text/plain\r\n"
    f"Content-Length: {len(body)}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
    f"{body}"
)


print(solicitud_http)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(solicitud_http.encode('utf-8'))
    # Recibir y mostrar la respuesta completa del servidor
    respuesta_http = s.recv(4096).decode('utf-8')
    print("\nRespuesta del servidor HTTP recibida:")
    print(respuesta_http)

