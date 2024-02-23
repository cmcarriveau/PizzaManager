from pymongo import MongoClient

cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
client = MongoClient(cluster)

print(client.list_database_names())

db = client.test 

print(db.list_collection_names())
