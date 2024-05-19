import os
import socket
import threading
import socketserver
from pathlib import Path
import binascii
from datetime import datetime


# global HOST
global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):
    def guardar_log_server(*args):
        BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        ruta = os.path.join(BASE_DIR, "servidor_logs.txt")
        log_function = open(ruta, "a")
        print(
            datetime.now().strftime("%H:%M:%S--%d/%m/%y"),
            "- Servidor",
            "\nDatos enviados desde el cliente:",
            args[1],
            "\n",
            file=log_function,
        )

    def handle(self):
        print("---"*25)
        data = self.request[0].strip()
        socket = self.request[1]

        # ####################################################
        #   String
        # ####################################################
        print(data.decode("UTF-8"))
        self.guardar_log_server(data.decode("UTF-8"))
        
        # ####################################################
        #   Paquete e
        # ####################################################

        value2 = 0xA0
        packed_data_2 = bytearray()
        packed_data_2 += value2.to_bytes(1, "big")
        socket.sendto(packed_data_2, self.client_address)
        print("---"*25)
    



if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
