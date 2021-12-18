import socket, sys, json, pickle
import os

def inventario_cli():
    while(True):
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

            alo = ''
           
            print("(1) Anadir producto nuevo\n(2) Editar stock de algun producto\n(3) Anadir stock a un producto\n(4) Volver al menu principal")
            selec = int(input("Seleccione: "))
            if(selec == 1):
                print("Ingrese el nombre del producto")
                n_producto=input()
                print("Ingrese su stock")
                stock=input()
                print("Ingrese el precio")
                precio=input()
                print("Agregue la categoria")
                categoria=input()
                alo = "anadir|"+n_producto+"|"+stock+"|"+precio+"|"+categoria
            elif(selec == 2):
                n = input("Ingrese id del producto para editar el stock: ")
                new_value = input("Ingrese valor nuevo de stock: ")
                alo = "editar_stock|"+n+"|"+new_value
            elif(selec == 3):
                n = input("Ingrese id del producto para agregar stock: ")
                new_value = input("Ingrese el valor: ")
                alo = "add_stock|"+n+"|"+new_value
            elif(selec == 4):
                return
            else:
                print("Opcion invalida")
            
            # Connect the socket to the port where the server is listening
            server_address = ('localhost', 25001)
            #print('connecting to {} port {}'.format(*server_address))
            sock.connect(server_address)

            try:
                # Send data
                message = alo.encode()
                #print('sending {!r}'.format(message))
                sock.sendall(message)
                
                data = sock.recv(4096)

                print(data.decode())
                    
            finally:
                    sock.close()
