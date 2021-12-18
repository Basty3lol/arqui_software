from ctypes import resize
import socket, sys, json, pickle
import os
from bdd import connectDb

collection=connectDb()["foro"]

class foro():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 25000)

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

                    if(commands[0]=="desplegar"):
                        messs = self.desplegar_preguntas()
                        connection.sendall(pickle.dumps(messs))
                        break
                    elif(commands[0]=="desplegar_cli"):
                        messs = self.desplegar_pregresp_cli(commands[1])
                        connection.sendall(pickle.dumps(messs))
                        break
                    elif(commands[0] == "responder"):
                        if(self.responder_pregunta(commands[1],commands[2])):
                            connection.sendall("Se ha cambiado el estado de la pregunta de forma existosa".encode())
                        else:
                            connection.sendall("Hubo un error al cambiar estado de pregunta".encode())
                        break
                    elif(commands[0] == "ingresar"):
                        if(self.insertar_pregunta(commands[1],commands[2])):
                            connection.sendall("Se ha publicado la pregunta de forma existosa".encode())
                        else:
                            connection.sendall("Hubo un error al publicar la pregunta".encode())
                        break
            finally:
                connection.close()

    def desplegar_preguntas(self):
        #sacar la wea de base de datos y enviar al loco
        datos = []
        for data in collection.find({"respondido":False},{"_id":0, "respondido":0}):
            datos.append(data)
        return datos

    def desplegar_pregresp_cli(self, correo):
        datos = []
        for data in collection.find({"correo":str(correo)},{"_id":0}):
            datos.append(data)
        return datos
    def responder_pregunta(self, ID, resp):
        try:
            respuesta = {
                "ID":int(ID),
                "correo":collection.find_one({"ID": int(ID),"tipo":"pregunta"},{"correo":1})["correo"],
                "descripcion":resp,
                "tipo":"respuesta"
            }
            collection.insert_one(respuesta)
            query = { "ID":int(ID) }
            change = { "$set": {"respondido":True} }
            collection.update_one(query,change)
            return True
        except:
            return False

    def insertar_pregunta(self, correo, mensaje):
        try:
            collection_temp = connectDb()["usuarios"]
            name = collection_temp.find_one({"correo": correo},{"nombre":1})["nombre"]
            maximo = 0
            for data in collection.find({},{"ID":1,"nombre":1}):
                if(data["ID"] > maximo):
                    maximo = data["ID"]
            
            pregunta = {
                "ID":maximo+1,
                "nombre":name,
                "correo":correo,
                "respondido":False,
                "descripcion":mensaje,
                "tipo":"pregunta"
            }

            collection.insert_one(pregunta)
            return True
        except:
            return False
foro()