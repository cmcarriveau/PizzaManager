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
                    "id": "2",
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