import unittest
from unittest.mock import patch, Mock
from recipeData import Recipe, fetchRecipes, addRecipeData, deleteRecipeData, editRecipeData
from toppingData import fetchToppings, addData, deleteData, editData

#dummy data for recipes and toppings
recipe = Recipe("Sauce Pizza", [{"name": "Tomato Sauce"}])
topping = {
    "id": "1",
    "type": "toppings",
    "sauces": [
        {"name": "Marinara"},
        {"name": "Pesto"}
    ],
    "cheeses": [
        {"name": "Mozzarella"},
        {"name": "Cheddar"}
    ],
    "meats": [
        {"name": "Pepperoni"},
        {"name": "Sausage"}
    ],
    "veggies": [
        {"name": "Onions"},
        {"name": "Peppers"}
    ]
}

class TestDataFunctions(unittest.TestCase):

    #Tests if a recipe can be successfully added to the database
    @patch('pymongo.MongoClient')
    def test_add_recipe_success(self, mock):
        #mock successful connection and data retrieval
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = {}

        # Add the recipe and check success
        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append(ingredient.name)
        success = addRecipeData(recipe.recipeName, ingredients)
        #delete it when done 
        deleteRecipeData(recipe.recipeName)
        self.assertEqual(success, 1)

    #Tests if a a duplicate recipe will not be added
    @patch('pymongo.MongoClient')
    def test_add_recipe_existing(self, mock):
        #mock connection and existing recipe
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = {"recipes": [recipe.__dict__]}

        #try adding the same recipe and check for failure
        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append(ingredient.name)
        addRecipeData(recipe.recipeName, ingredients)
        success = addRecipeData(recipe.recipeName, ingredients)
        #delete it when finished
        deleteRecipeData(recipe.recipeName)
        self.assertEqual(success, 0)

    #Tests if a pre-existing recipe can be edited
    @patch('pymongo.MongoClient')
    def test_edit_recipe_success(self, mock):
        #mock connection and existing recipe
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = {"recipes": [recipe]}

        #edit the recipe and check success
        #add it before editing 
        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append(ingredient.name)
        addRecipeData(recipe.recipeName, ingredients)
        #edit
        new_ingredients = ["Pesto Sauce"]
        success = editRecipeData(recipe.recipeName, new_ingredients)
        #delete when done
        deleteRecipeData(recipe.recipeName)
        self.assertEqual(success, 1)

    #Tests that a non-existent recipe cannot be edited
    @patch('pymongo.MongoClient')
    def test_edit_recipe_not_found(self, mock):
        #mock connection and non-existent recipe
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = {"recipes": []}

        #edit a non-existent recipe and check for failure
        success = editRecipeData("Non-Existent Recipe", ["Ingredient A", "Ingredient B"])
        self.assertEqual(success, 2)

    #Tests that the recipes can be fetched from the database
    @patch('pymongo.MongoClient')
    def test_fetch_recipes_success(self, mock):
        #mock connection and data retrieval
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = {"recipes": [recipe]}

        #fetch recipes and check retrieved data
        #add recipe
        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append(ingredient.name)
        addRecipeData(recipe.recipeName, ingredients)
        #check to see if added recipe is at end of list
        recipes = fetchRecipes()
        self.assertGreater(len(recipes.recipes), 0)
        self.assertEqual(recipes.recipes[-1].recipeName, recipe.recipeName)
        #delete when done
        deleteRecipeData(recipe.recipeName)

    #Tests that the fetched recipe data is never empty
    @patch('pymongo.MongoClient')
    def test_fetch_recipes_not_empty(self, mock):
        #mock connection and empty data
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = None

        #fetch recipes and check empty list
        recipes = fetchRecipes()
        self.assertNotEqual(len(recipes.recipes), 0)

    #Tests that a recipe can be deleted
    @patch('pymongo.MongoClient')
    def test_delete_recipe_success(self, mock):
        # Mock connection and existing recipe
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = {"recipes": [recipe]}

        # Delete the recipe and check success
        #add recipe first
        ingredients = []
        for ingredient in recipe.ingredients:
            ingredients.append(ingredient.name)
        addRecipeData(recipe.recipeName, ingredients)
        #then delete the recipe and test
        success = deleteRecipeData(recipe.recipeName)
        self.assertEqual(success, 1)

    #Tests that a non-existing recipe cannot be deleted
    @patch('pymongo.MongoClient')
    def test_delete_recipe_not_found(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = {"recipes": []}

        #delete non-existent recipe
        success = deleteRecipeData("Non-Existent Recipe")
        self.assertEqual(success, 2)

    #Tests that toppings data can be fetched
    @patch('pymongo.MongoClient')
    def test_fetch_toppings_success(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping

        #add topping to determine if function grabs all toppings
        addData("sauces", "Cheese Sauce")
        #fetch
        toppings = fetchToppings()
        #delete added topping
        deleteData("sauces", "Cheese Sauce")
        self.assertEqual(toppings.sauces[-1].name, "Cheese Sauce")

    #Tests that fetched topping data is never empty
    @patch('pymongo.MongoClient')
    def test_fetch_toppings_not_empty(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping

        toppings = fetchToppings()
        #ensure that it recieved all toppings
        self.assertNotEqual(len(toppings.sauces), 0)
        self.assertNotEqual(len(toppings.cheeses), 0)
        self.assertNotEqual(len(toppings.meats), 0)
        self.assertNotEqual(len(toppings.veggies), 0)

    #Tests that a topping can be added
    @patch('pymongo.MongoClient')
    def test_add_data_success(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping

        #add data
        success = addData("sauces", "Arrabbiata Sauce")
        #delete when finished
        deleteData("sauces", "Arrabbiata Sauce")

        self.assertEqual(success, 1)

    #Tests that a duplicate topping cannot be added
    @patch('pymongo.MongoClient')
    def test_add_data_existing(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping

        #add data and duplicate data
        addData("sauces", "Arrabbiata Sauce")
        success = addData("sauces", "Arrabbiata Sauce")
        #delete when finished
        deleteData("sauces", "Arrabbiata Sauce")

        self.assertEqual(success, 0)

    #Tests that a toppoing can be deleted
    @patch('pymongo.MongoClient')
    def test_delete_data_success(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping
        
        #add data and delete when finished
        addData("sauces", "Arrabbiata Sauce")
        success = deleteData("sauces", "Arrabbiata Sauce")

        self.assertEqual(success, 1)

    #Tests that a non-existent topping cannot be deleted
    @patch('pymongo.MongoClient')
    def test_delete_data_not_found(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping

        #try to delete data that doesnt exist
        success = deleteData("sauces", "Non-existent Topping")

        self.assertEqual(success, 2)

    #Tests that a topping can be edited
    @patch('pymongo.MongoClient')
    def test_edit_data_success(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping

        #add data to edit
        addData("sauces", "Arrabbiata")
        success = editData("sauces", "Arrabbiata", "Arrabbiata Sauce")
        #delete when finished
        deleteData("sauces", "Arrabbiata Sauce")

        self.assertEqual(success, 1)

    #Tests that a non-existent topping cannot be edited
    @patch('pymongo.MongoClient')
    def test_edit_data_not_found(self, mock):
        #mock connection and existing topping
        mock.return_value = Mock()
        mock.return_value.find_one.return_value = topping

        success = editData("sauces", "Non-existent Topping", "Non-existent Topping")

        #assert that the edit was unsuccessful (returned 0)
        self.assertEqual(success, 2)
