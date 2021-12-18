import socket, sys, json
import os
import pickle 
from bdd import connectDb

#seteo del socket
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),6001))
s.listen(1)
collection=connectDb()["productos"]


def print_menu1():
    print ('1 -- Desplegar los productos' )
    print ('2 -- Filtrar busqueda' )
    print ('3 -- Exit' )

def print_categorias():
    print ('monitores' )
    print ('memorias' )
    print ('mouse' )

def filtro_productos(filtro):
    datos = collection.find({"categoria":{'$eq':filtro}},{"_id":0} )
    aux=''
    aux1=[]
    for i in datos:
        aux1.append(str(i))
    return pickle.dumps(aux1)



def main():
    while True:
        print('waiting for a connection')
        # Receive the data in small chunks and retransmit it
        while True:
            
            clientsocket, address = s.accept()
            print(f"La conexion con {address} fue establecida")
            #print_menu1()
            #option = int(input('Seleccione una opcion: ')) 
            idprod = clientsocket.recv(4096).decode("utf-8")
            datos = collection.find_one({"idprod":{'$eq':idprod}},{"_id":0} )
            # for i in datos:
            #      producto.append((i))
            clientsocket.sendall(pickle.dumps(datos))


main()

#datos = collection.find({"categoria":{'$eq':'mouse'}},{"_id":0} )
#for i in datos:
#    print(str(i))
    #datos.append(data)
#print(datos)
    



#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('localhost', 5000)
#sock.connect(server_address)