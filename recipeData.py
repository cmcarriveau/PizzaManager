from pymongo import MongoClient

def fetchRecipes():
    data = getRecipeData()
    list = createRecipeList(data)
    return list

def getRecipeData():
    try:
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Recipes"]

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
                    "recipes": [
                        {
                        "name": "Database Error",
                        "ingredients": [
                            {"name": "Database Error"}
                        ]
                        }
                    ]
            }
            return fail
    
    #catch any errors
    except Exception as e:
        print("Error:", e)

#convert json file into object
def createRecipeList(data):
    
    #creates array to hold all the recipes
    recipes = []
    for recipe in data['recipes']:
        recipe = Recipe(recipe['recipeName'], recipe['ingredients'])
        recipes.append(recipe)
    recipeBook = RecipeBook(recipes)

    return recipeBook

def addRecipeData(name, ingredientsList):
    try:
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Recipes"]

        #find document
        document = collection.find_one()

        if document:
            existingRecipe = collection.find_one({"recipes.recipeName": name})
            if existingRecipe: 
                success = 0
            else: 
                #retrieve data
                newIngredients = []
                for ingredient in ingredientsList:
                    newIngredients.append({"name": ingredient})

                #create new recipe
                newRecipe = {
                    "recipeName": name,
                    "ingredients": newIngredients
                }

                #add recipe to document
                document["recipes"].append(newRecipe)

                #update ingredients list
                collection.update_one({"_id": document["_id"]}, {"$set": document})

                print(name, "was added to recipes")
                success = 1
        else:
            print("Not found")

        client.close()     

        return success

    #catch any errors
    except Exception as e:
        print("Error:", e)

def deleteRecipeData(name):
    try:
        success = 0
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Recipes"]

        document = collection.find_one()

        if document:
            #find the recipe name in the database
            exists = collection.find_one({"recipes.recipeName": name})

            #if it exists then update it by removing it
            if exists: 
                toDelete = collection.update_one(
                    {"recipes.recipeName": name},
                    {"$pull": {"recipes": {"recipeName": name}}}
                )
                if toDelete.matched_count > 0:
                    print(name, "was removed from the recipe book")
                    success = 1
                else:
                    print(name, "could not be deleted from the recipe book") 
                    success = 0   
            else:
                print(name, "in section does not exist in the database")
                success = 0

        client.close()   

        return success        
    #catch any errors
    except Exception as e:
        print("Error:", e)

def editRecipeData(toEdit, ingredientsList):
    try:
        success = 0
        #connect to database
        cluster = "mongodb+srv://carissa:Sj67IbVeK2byWQ9G@clusters.ngx304e.mongodb.net/?retryWrites=true&w=majority&appName=Clusters"
        client = MongoClient(cluster)

        #access database and collection 
        db = client["PizzaData"]
        collection = db["Recipes"]

        document = collection.find_one()

        if document:
            #tests if the topping exists
            newIngredients = []
            for ingredient in ingredientsList:
                newIngredients.append({"name": ingredient})

            exists = collection.find_one({"recipes.recipeName": toEdit.recipeName})
            if exists: 
                edited = collection.update_one(
                    {"recipes.recipeName": toEdit.recipeName},  # Filter for the recipe name
                    {"$set": {"recipes.$.ingredients": newIngredients}}    
                )
                if edited.matched_count > 0:
                    print(toEdit.recipeName, "was changed!")
                    success = 1
                else:
                    print(toEdit.recipeName, "could not be changed") 
                    success = 0   
            else:
                print(toEdit.recipeName, "does not exist in the database")
                success = 0

        client.close()   

        return success        
    #catch any errors
    except Exception as e:
        print("Edit Error:", e)

class Ingredient:
    def __init__(self, name):
        self.name = name

class Recipe:
    def __init__(self, recipeName, ingredients):
        self.recipeName = recipeName
        self.ingredients = [Ingredient(ing["name"]) for ing in ingredients]

class RecipeBook:
    def __init__(self, recipes):
        self.recipes = recipes