import socket, sys, json
import os
import pickle

from pymongo import collection
sys.path.append('../')
from servicios.bdd import connectDb

collection1 = connectDb()["productos"]
collection2 = connectDb()["compra"]
collection3 = connectDb()["usuarios"]

def compras(carro_productos, correo):
    os.system('clear')
    print("Estos son los articulos de tu carrito")
    print_carrito(carro_productos)
    selec = str(input("Desea confirmar la compra? si=1 no=2: "))
    if(selec == '1'):
        
        max_id = 0
        for data in collection2.find({},{"idcompra":1}):
            if(int(data["idcompra"]) > int(max_id)):
                max_id = data["idcompra"]
        #print("alooooo1")
        dic = {}
        for prod in carro_productos:
            if(prod["idprod"] in dic):
                dic[prod["idprod"]][1] += 1
            else:
                dic[prod["idprod"]]=[prod["nombre_producto"],1,prod["precio"]]
        #print("alooooo2")
        for i in dic:
            stock_act = int(collection1.find_one({"idprod": i},{"stock":1})["stock"])
            if( stock_act < int(dic[i][1]) ):
                print("No hay suficiente stock de",dic[i][0],"queda",stock_act,"en stock, porfavor revise su carrito")
                return
        #print("alooooo3")
        for j in dic:
            suma = 0
            suma += dic[j][1]*dic[j][2]
            stock_act = int(collection1.find_one({"idprod": j},{"stock":1})["stock"])

            query = { "idprod":j }
            change = { "$set": {"stock": stock_act - int(dic[j][1])} }
            collection1.update_one(query,change)

            compra = {
                "idproducto": j,
                "rutcliente": collection3.find_one({"correo": correo},{"rut":1})["rut"],
                "cantidad": int(dic[j][1]),
                "precio":suma,
                "idcompra":str(int(max_id)+1),
                "retirado":False
            }
            
            collection2.insert_one(compra)
            print("compra realizada con exito")
            carro_productos = []
            return carro_productos
    elif(selec == '2'):
        print("no se compro nada")
        return carro_productos

    
def print_menu1():
    print ('1 -- Agregar productos al carro de compras' )
    print ('2 -- Mostrar carrito' )
    print ("3 -- Quitar algo del carrito")
    print ('4 -- Volver al menu principal' )

def print_carrito(carro_productos):
    os.system('clear')
    print("=========== Carrito ============")
    dic = {}
    for prod in carro_productos:
        if(prod["idprod"] in dic):
            dic[prod["idprod"]][1] += 1
        else:
            dic[prod["idprod"]]=[prod["nombre_producto"],1,prod["precio"]]
    suma = 0
    for i in dic:
        suma += dic[i][1]*dic[i][2]
        print(i,"| nombre:",dic[i][0],"| precio:",dic[i][2],"| cantidad:",dic[i][1])
    print("Precio Total:",suma)

def maincarrito(carro_productos):
    while(True):
        print_menu1()
        option = input('Seleccione una opcion: ')
        if option =='1':
            while(True):
                #seteo del socket
                s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((socket.gethostname(),6001))
                idprod = input('Ingrese id del producto que desea agregar: ')
                s.send(bytes(str(idprod),"utf-8")) #envio el id del producto
                

                msg = pickle.loads(s.recv(4096)) #recibo el producto de ese id
                carro_productos.append(msg)
                    #producto anterior agregado
                res=input('Desea agregar otro producto al carro? Si==1 No==2: ')

                if res =='2':
                    break

                s.close()
                #x=input('Presione una tecla para continuar...')
                #os.system('cls')
                #break
        elif option == '2':
            print_carrito(carro_productos)
        elif option == '3':
            p = input("coloque id del producto que desea eliminar del carrito: ")
            for prod in range(len(carro_productos)):
                if(carro_productos[prod]["idprod"] == str(p)):
                    carro_productos.pop(prod)
                    break
        elif option == '4':
            return carro_productos

    
def general(carro_productos=[]):
    x=maincarrito(carro_productos)
    return x