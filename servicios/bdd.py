from pymongo import MongoClient

def connectDb():

    cluster=MongoClient("mongodb+srv://admin:admin@arquibdd.uj011.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db=cluster["project"]
    return db
    