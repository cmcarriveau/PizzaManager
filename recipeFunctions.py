from recipeData import fetchRecipes

def deleteRecipe(selected):
            index = selected.get()
            recipeBook = fetchRecipes()
            toDelete = recipeBook.recipes[index]
            #call delete