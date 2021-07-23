import pymongo

password = "TestPassword123"

myFirstDatabase = "Neptune"

connectionURL ="mongodb+srv://neptuneorbital:{password}@cluster0.k2azk.mongodb.net/Cluster0?retryWrites=true&w=majority".format(password=password)

#, myFirstDatabase=myFirstDatabase)

client = pymongo.MongoClient(connectionURL)

db = client.test