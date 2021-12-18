from ctypes import resize
import socket, sys, json, pickle
import os
from bdd import connectDb

collection=connectDb()["productos"]

class inventario():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 25001)

        #self.client_dbb = MongoClient("")

        self.sock.bind(self.server_address)

        # Listen for incoming connections
        self.sock.listen(1)
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.sock.accept()

            try:
                print('connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(4096).decode()
                    commands = data.split('|')
                    print('received',commands)

                    if(commands[0]=="anadir"):
                        if(self.add_product(commands[1],commands[2],commands[3],commands[4])):
                            messs = "Se realizo la accion de forma exitosa"
                            connection.sendall(messs.encode())
                        else:
                            messs = "Hubo un error al realizar la accion"
                            connection.sendall(messs.encode())
                        break
                    if(commands[0]=="editar_stock"):
                        if(self.edit_stock(commands[1],commands[2])):
                            messs = "Se realizo la accion de forma exitosa"
                            connection.sendall(messs.encode())
                        else:
                            messs = "Hubo un error al realizar la accion"
                            connection.sendall(messs.encode())
                        break
                    if(commands[0]=="add_stock"):
                        if(self.add_stock(commands[1],commands[2])):
                            messs = "Se realizo la accion de forma exitosa"
                            connection.sendall(messs.encode())
                        else:
                            messs = "Hubo un error al realizar la accion"
                            connection.sendall(messs.encode())
                        break
            finally:
                connection.close()

    def add_product(self, n_producto, stock, precio,categoria):
        try:
            max_id = 0
            for prod in collection.find({},{"idprod":1}):
                if(int(prod["idprod"]) > max_id):
                    max_id = int(prod["idprod"])

            post={
                "nombre_producto":n_producto,
                "stock":int(stock),
                "precio":int(precio),
                "categoria":categoria,
                "idprod":str(max_id+1)
            }
            collection.insert_one(post)
            return True
        except:
            return False

    def edit_stock(self,id,new_value):
        try:
            query = { "idprod":id }
            change = { "$set": {"stock": new_value} }
            collection.update_one(query,change)
            return True
        except:
            return False

    def add_stock(self,id,new_stock):
        try:
            query = { "idprod":id }
            change = { "$set": {"stock": int(collection.find_one({"idprod": id},{"stock":1})["stock"])+int(new_stock)} }
            collection.update_one(query,change)
            return True
        except:
            return False
a = inventario()