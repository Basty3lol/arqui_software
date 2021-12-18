from typing import Collection
import pymongo
from pymongo import MongoClient
import hashlib

cluster=MongoClient("mongodb+srv://admin:admin@arquibdd.uj011.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=cluster["project"]
collection=db["usuarios"]

#insertar cosas a la base de datos
#crear usuario
print("Ingrese su correo nombre")
nombre=input()
print("Ingrese su direccion")
direccion=input()
print("Ingrese su RUT")
rut=input()
print("Ingrese su correo electronico")
correo=input()
print("Ingrese su contraseña")
password=input()
safepass = hashlib.sha256(password.encode('utf-8')).hexdigest()
post={"correo":correo,"contraseña":safepass,"nombre":nombre,"direccion":direccion,"rut":rut, "isAdmin":False}
collection.insert_one(post)
