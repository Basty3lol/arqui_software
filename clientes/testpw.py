from typing import Collection
import pymongo
from pymongo import MongoClient
import hashlib


#insertar cosas a la base de datos
#crear usuario

print("Ingrese su contraseña")
password=input()
safepass = hashlib.sha256(password.encode('utf-8')).hexdigest()


