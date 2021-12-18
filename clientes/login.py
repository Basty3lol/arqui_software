import socket, pickle
import sys, json


def Login():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    usuario = input("Ingrese Correo: ")
    pw = input("Ingrese Password: ")
    print(f"usuario: {usuario}, Password: {pw}")
    post = str({'usuario': usuario, 'pw': pw}).replace("'",'"').encode()
    
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 5001)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    try: 
        sock.sendall(post)
        amount_received = 0
        amount_expected = len(post)

        while amount_received < amount_expected:
            data = sock.recv(4096)
            amount_received += len(data)
            print('received {!r}'.format(data))
            return data.decode("utf-8"), usuario
    finally:
        print('closing socket')
        sock.close()
        
        


