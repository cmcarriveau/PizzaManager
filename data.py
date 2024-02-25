from pymongo import MongoClient

#begins fetching the topping object
def fetchToppings():
    data = getToppingData()
    list = createToppingsList(data)
    return list

#retrieves data from MongoDB database
def getToppingData():
    try:
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Toppings"]

        #retrieve data
        data = collection.find_one()

        #close connection
        client.close()

        return data
    
    #catch any errors
    except Exception as e:
        print("Error: ", e)

#convert json file into object
def createToppingsList(data):

    toppingList = Toppings(
        id = data['id'],
        type=data['type'],
        sauces=data['sauces'],
        cheeses=data['cheeses'],
        meats=data['meats'],
        veggies=data['veggies']
    )

    return toppingList

def addData(type, name):
    try:
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Toppings"]

        document = collection.find_one({"id": "1"})

        if document:
            newTopping = {"name": name}
            document[type].append(newTopping)

            collection.update_one({"_id": document["_id"]}, {"$set": document})
            print(name, "was added to", type)
        else:
            print("Not found")


        #close connection
        client.close()
    
    #catch any errors
    except Exception as e:
        print("Error: ", e)

class Topping:
    def __init__(self, name):
        self.name = name

#Toppings class where the data will be stored
class Toppings:
    #initializr class
    def __init__(self, id, type, sauces, cheeses, meats, veggies):
        self.id = id
        self.type = type
        self.sauces = [Topping(sauce['name']) for sauce in sauces]
        self.cheeses = [Topping(cheese['name']) for cheese in cheeses]
        self.meats = [Topping(meat['name']) for meat in meats]
        self.veggies = [Topping(veggie['name']) for veggie in veggies]
