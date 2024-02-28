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

        if data:
            return data
        else:
            #will return empty object in the case of a database error
            print("no data found")
            fail = {
                "id":"1",
                "type":"toppings",
                "sauces":[
                    {"name":"Database Error"}
                ],
                "cheeses":[
                    {"name":"Database Error"}
                ],
                "meats":[
                    {"name":"Database Error"}
                    ],
                "veggies":[
                    {"name":"DataBase Error"}
                ]
            }
            return fail
    
    #catch any errors
    except Exception as e:
        print("Error:", e)

#convert json file into object
def createToppingsList(data):

    toppingList = Toppings(
        id = data['id'],
        type = data['type'],
        sauces = data['sauces'],
        cheeses = data['cheeses'],
        meats = data['meats'],
        veggies = data['veggies']
    )

    return toppingList

def addData(type, name):
    try:
        #variable that tells whether it was successfully added
        success = 0

        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Toppings"]

        document = collection.find_one({"id": "1"})

        if document:
            existingTopping = collection.find_one({"type": "toppings", f"{type}.name": name})
            if existingTopping:
                success = 0
            else:
                newTopping = {"name": name}
                document[type].append(newTopping)

                collection.update_one({"_id": document["_id"]}, {"$set": document})
                print(name, "was added to", type)
                success = 1
        else:
            print("Not found")

        #close connection
        client.close()

        return success
    
    #catch any errors
    except Exception as e:
        print("Error:", e)

def deleteData(type, name):
    try:
        success = 0
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Toppings"]

        document = collection.find_one({"id": "1"})

        if document:
            #find the recipe name in the database
            exists = collection.find_one({"type": "toppings", f"{type}.name": name})
            
            #if it exists then update it by removing it
            if exists: 
                toDelete = collection.update_one(
                    {"type": "toppings", f"{type}.name": name},  
                    {"$pull": {f"{type}": {"name": name}}}    
                )
                if toDelete.matched_count > 0:
                    print(name, "was removed from", type)
                    success = 1
                else:
                    print(name, "could not be deleted from", type) 
                    success = 0   
            else:
                print(name, "in section", type, "does not exist in the database")
                success = 0

        client.close()   

        return success        
    #catch any errors
    except Exception as e:
        print("Error:", e)

def editData(type, name, newName):
    try:
        success = 0
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Toppings"]

        document = collection.find_one({"id": "1"})

        if document:
            #tests if the topping exists
            exists = collection.find_one({"type": "toppings", f"{type}.name": name})
            if exists: 
                toEdit = collection.update_one(
                    {"type": "toppings", f"{type}.name": name},  
                    {"$set": {f"{type}.$.name": newName}}    
                )
                if toEdit.matched_count > 0:
                    print(type, "was changed to", newName)
                    success = 1
                else:
                    print(name, "could not be changed") 
                    success = 0   
            else:
                print(name, "in section", type, "does not exist in the database")
                success = 0

        client.close()   

        return success        
    #catch any errors
    except Exception as e:
        print("Error:", e)

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
