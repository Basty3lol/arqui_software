import socket, sys, json
import os
from bdd import connectDb
import hashlib


collection=connectDb()["usuarios"]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 5002)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(4096).decode()
            data = json.loads(data)
            print('received {!r}',data)
            safepass = hashlib.sha256(data["pw"].encode('utf-8')).hexdigest()
            post={"correo":data["correo"],"contraseña":safepass,"nombre":data["nombre"],"direccion":data["direccion"],"rut":data["rut"], "isAdmin":2}
            collection.insert_one(post)            
            print('ESTES ES X: ',post)
            messs = '2'
            if post != None:
                print('sending data back to the client')
                connection.sendall(messs.encode())
                break
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()

