import socket, sys, json
import os
import pickle 
from bdd import connectDb

#seteo del socket
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),6000))
s.listen(5)
collection=connectDb()["productos"]

def filtro_productos(filtro):
    datos = collection.find({"categoria":{'$eq':filtro}},{"_id":0} )
    aux1=[]
    for i in datos:
        aux1.append(i)
    #print(aux1)
    return pickle.dumps(aux1)

def main():
    while True:
        print('waiting for a connection')
        # Receive the data in small chunks and retransmit it
        while True:
            datos=[]
            clientsocket, address = s.accept()
            print(f"La conexion con {address} fue establecida")
            #print_menu1()
            #option = int(input('Seleccione una opcion: ')) 
            option = int(clientsocket.recv(4096).decode("utf-8"))
            if option == 1:
                for data in collection.find({},{"_id":0}):
                    datos.append(data)
                clientsocket.sendall(pickle.dumps(datos))
                break
            elif option == 2:
                print('Esperando filtro...')
                filtro=clientsocket.recv(4096).decode("utf-8")
                clientsocket.sendall(filtro_productos(filtro))
                break
            elif option == 3:
                print('chaito')
                exit()
            else:
                print('Opcion invalida, por favor elija numero entre 1 y 3.')
                main()


main()

#datos = collection.find({"categoria":{'$eq':'mouse'}},{"_id":0} )
#for i in datos:
#    print(str(i))
    #datos.append(data)
#print(datos)
    



#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('localhost', 5000)
#sock.connect(server_address)