#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Configuración del WebServer                #
#############################################

import socket
import json
from templates import HTML

def iniciar_servidor(get_data):

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    while True:
        cl, addr = s.accept()
        req = cl.recv(1024).decode()

        if "/data" in req:
            data = get_data()
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
            cl.send(json.dumps(data))
        else:
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            cl.send(HTML)

        cl.close()