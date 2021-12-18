import socket, pickle
import sys
import os

def preguntas_foro(type_user, mail):
    
    # Accion que desea realizar el usuario en el foro
    while(True):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

        alo = ''
        if(type_user == 1 or type_user == 3): # Si el usuario es admin
            print("(1) Desplegar preguntas del foro\n(2) Responder\n(3) Volver al menu principal")
            selec = int(input("Seleccione: "))
            if(selec == 1):
                alo = "desplegar"
            elif(selec == 2):
                n = int(input("Ingrese ID de pregunta para responder: "))
                resp = input("Ingrese respuesta a publicar: ")
                alo = "responder|"+str(n)+"|"+resp
            elif(selec == 3):
                return
        elif(type_user == 2):
            print("(1) Publicar pregunta en el foro\n(2) Desplegar preguntas y respuestas\n(3) Volver al menu principal")
            selec = int(input("Seleccione: "))
            if(selec == 1):
                pal = input("Ingrese pregunta: ")
                alo = "ingresar|"+mail+"|"+pal
            elif(selec == 2):
                alo = "desplegar_cli|"+mail
            elif(selec == 3):
                return
        else:
            print("Debes registrarte para comentar en el foro.")
            return
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 25000)
        #print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)

        try:
            os.system('clear')
            # Send data
            message = alo.encode()
            #print('sending {!r}'.format(message))
            sock.sendall(message)
            if(type_user==1 or type_user == 3):
                if(selec == 1):
                    data = sock.recv(4096)
                    for i in pickle.loads(data):
                        print("=========== ID:",i["ID"],"============")
                        print("Nombre:",i["nombre"],"| Correo:",i["correo"])
                        print("Pregunta:",i["descripcion"])
                elif(selec == 2):
                    data = sock.recv(4096)
                    print(data.decode())
            elif(type_user == 2):
                if(selec == 1):
                    data = sock.recv(4096)
                    print(data.decode())
                elif(selec == 2):
                    data = sock.recv(4096)
                    for i in pickle.loads(data):
                        if(i["tipo"]=="pregunta"):
                            print("=========== ID:",i["ID"],"============")
                            print("Respondida: "+("si" if i['respondido'] else "no"))
                            print("Pregunta:",i["descripcion"])
                        else:
                            print("Respuesta:",i["descripcion"])
                
        finally:
                sock.close()