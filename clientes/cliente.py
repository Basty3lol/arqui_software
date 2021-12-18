import socket, sys, json
import os
import pickle

def print_menu1():
    print ('1 -- Desplegar los productos' )
    print ('2 -- Filtrar busqueda' )
    print ('3 -- Exit' )

def print_categorias():
    print ('audifonos')
    print ('monitores' )
    print ('memorias' )
    print ('mouse' )
    print ('teclado')

def catalogo():
    #seteo del socket
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((socket.gethostname(),6000))

    while True:
        print_menu1()
        option = input('Seleccione una opcion: ')
        if option =='1':
            s.send(bytes(str(option),"utf-8"))
            msg = s.recv(4096)
            os.system('clear')
            for prod in pickle.loads(msg):
                print("========== ID",prod["idprod"],"==========")
                print("nombre:",prod["nombre_producto"])
                print("precio:",prod["precio"])
                print("stock:",prod["stock"])

            x=input('Presione una tecla para continuar...')
            break
        elif option =='2':
            s.send(bytes(str(option),"utf-8"))
            print_categorias()
            filtro = input('Ingrese la categoria: ')
            s.send(bytes(str(filtro),"utf-8"))
            msg2 = pickle.loads(s.recv(4096))
            #print(msg2)
            for prod in msg2:
                print("========== ID",prod["idprod"],"==========")
                print("nombre:",prod["nombre_producto"])
                print("precio:",prod["precio"])
                print("stock:",prod["stock"])
            break

        elif option =='3':
            exit()
        else:
            print('Ingrese numeros entre el 1 y el 3')


