import socket
import sys, json


def Register():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 5002)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    print("Ingrese su nombre")
    nombre=input()
    print("Ingrese su direccion")
    direccion=input()
    print("Ingrese su RUT")
    rut=input()
    print("Ingrese su correo electronico")
    correo=input()
    print("Ingrese su contraseña")
    password=input()
    post = str({'nombre': nombre, 'pw': password, 'direccion':direccion, 'rut':rut, 'correo': correo}).replace("'",'"').encode()  
    try: 
        sock.sendall(post)
        amount_received = 0
        amount_expected = len(post)

        while amount_received < amount_expected:
            data = sock.recv(4096)
            amount_received += len(data)
            print('received {!r}'.format(data))
            return data.decode("utf-8") 
    finally:
        print('closing socket')
        sock.close()
        
        
