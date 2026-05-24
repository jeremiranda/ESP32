#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Configuración del WebServer                #
#############################################

import socket
import json
import gc

from templates import HTML

def iniciar_servidor(get_data):

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()

    # 🔥 reutilizar socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)

    s.listen(2)

    # 🔥 timeout importante
    s.settimeout(2)

    print("WebServer iniciado")

    while True:

        cl = None

        try:

            # =========================
            # ESPERAR CLIENTE
            # =========================
            cl, addr = s.accept()

            # 🔥 timeout cliente
            cl.settimeout(2)

            req = cl.recv(1024)

            if not req:
                cl.close()
                continue

            req = req.decode()

            # =========================
            # API JSON
            # =========================
            if "/data" in req:

                data = get_data()

                response = json.dumps(data)

                cl.send(
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                cl.send(response)

            # =========================
            # HTML
            # =========================
            else:

                cl.send(
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                cl.send(HTML)

            # =========================
            # CERRAR
            # =========================
            cl.close()

            # 🔥 liberar memoria
            gc.collect()

        except Exception as e:

            print("WebServer error:", e)

            try:
                if cl:
                    cl.close()
            except:
                pass

            gc.collect()