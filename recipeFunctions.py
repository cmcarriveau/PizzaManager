from tkinter import *
from recipeData import fetchRecipes, deleteRecipeData, addRecipeData
from toppingData import fetchToppings

def loadRecipes():
    recipes = fetchRecipes()
    return recipes

def deleteRecipe(root, selected, errorLbl, recipeListboxes, recipeRadiobuttons):
    index = selected.get()
    if index == -1:
        #if none are selected, print error message
        errorLbl.config(text="Select a recipe to delete", fg="red")
    else:
        #get the name of the recipe to delete
        recipeBook = fetchRecipes()
        toDelete = recipeBook.recipes[index].recipeName

        #call delete function
        result = deleteRecipeData(toDelete)

        #if it is deleted, then delete the listboxes and radio buttons
        if result == 1:
            print(index)
            #newRecipeList = refreshRecipes(root, recipeListboxes)    
            #newButtonList = refreshButtons(root, recipeRadiobuttons)
            recipeListboxes[index].delete(0, END)
            recipeListboxes[index].destroy()
            recipeRadiobuttons[index].destroy()
            errorLbl.config(text=f"{toDelete} was deleted!", fg="green")
            errorLbl.grid()
            #refreshRecipes(root, newRecipeList)    
            #refreshButtons(root, newButtonList)

def addRecipeWindow(root, errorLbl):         
    def addRecipe():
        ingredientList=[]
        print("add recipe")

        newName = newTopping.get()
        if newName:
            for checkbox in sauceCheckboxes:
                var = checkbox["variable"]
                if var.get():  
                    ingredientList.append(checkbox["checkbox"]["text"])
        
            for checkbox in cheeseCheckboxes:
                var = checkbox["variable"]
                if var.get():   
                    ingredientList.append(checkbox["checkbox"]["text"])

            for checkbox in meatCheckboxes:
                var = checkbox["variable"]
                if var.get():   
                    ingredientList.append(checkbox["checkbox"]["text"])

            for checkbox in veggieCheckboxes:
                var = checkbox["variable"]
                if var.get():    
                    ingredientList.append(checkbox["checkbox"]["text"])

            success = addRecipeData(newName, ingredientList)
            if success == 0:
                failed.grid()
                return success

            else:
                failed.grid_remove()
                add_recipe_window.destroy()
                errorLbl.config(text=f"{newName} was added!", fg="green")
                errorLbl.grid()   
                return success
                #newRecipeList = refreshRecipes(root, recipeListboxes)    
                #newButtonList = refreshButtons(root, recipeRadiobuttons)
        else:
             failed.config(text="Enter a recipe name")

    def close():
        add_recipe_window.destroy()

    print("create window")

    add_recipe_window = Toplevel(root)
    add_recipe_window.title("Add Recipe")
    add_recipe_window.transient(root)
    add_recipe_window.grab_set()

    #labels
    title = Label(add_recipe_window, text="Create Recipe")
    title.config(font=('Helvetica bold', 18))
    title.grid(row=0, column=1, pady=10, padx=10)

    recipeName = Label(add_recipe_window, text="Recipe Name:")
    recipeName.grid(row=1, column=0, pady=10, padx=10)

    #entry box for name
    newTopping = Entry(add_recipe_window)
    newTopping.grid(row=1, column=1, pady=10, padx=10)

    toppings = fetchToppings()

    #labels for checkboxes
    sauceLbl = Label(add_recipe_window, text="Sauces:")
    sauceLbl.grid(row=3, column=0, pady=10, padx=10)

    cheeseLbl =  Label(add_recipe_window, text="Cheeses:")
    cheeseLbl.grid(row=3, column=1, pady=10, padx=10)

    meatLbl = Label(add_recipe_window, text="Meats:")
    meatLbl.grid(row=3, column=2, pady=10, padx=10)

    veggieLbl = Label(add_recipe_window, text="Veggies:")
    veggieLbl.grid(row=3, column=3, pady=10, padx=10)

    #function buttons
    #add button
    addRecipeBtn = Button(add_recipe_window, text="Add", fg="green", command=lambda: addRecipe())
    addRecipeBtn.grid(row=1, column=2, pady=10, padx=10)

    #cancel button
    cancelAddBtn = Button(add_recipe_window, text="Cancel", fg="red", command=lambda: close())
    cancelAddBtn.grid(row=1, column=3, pady=10, padx=10)

    #error label
    failed = Label(add_recipe_window, text=" ", fg="red")
    failed.grid(row=2, column=1, pady=10, padx=10)

    #check boxes
    sauceCheckboxes = []
    for i, sauce in enumerate(toppings.sauces):
        var = BooleanVar(value=False)
        cb = Checkbutton(add_recipe_window, text=sauce.name, variable=var)
        cb.grid(row=i+4, column=0, sticky="w", padx=10, pady=5)
        sauceCheckboxes.append({"checkbox": cb, "variable": var})

    cheeseCheckboxes = []
    for i, cheese in enumerate(toppings.cheeses):
        var = BooleanVar(value=False)
        cb = Checkbutton(add_recipe_window, text=cheese.name, variable=var)
        cb.grid(row=i+4, column=1, sticky="w", padx=10, pady=5)
        cheeseCheckboxes.append({"checkbox": cb, "variable": var})

    meatCheckboxes = []
    for i, meat in enumerate(toppings.meats):
        var = BooleanVar(value=False)
        cb = Checkbutton(add_recipe_window, text=meat.name, variable=var)
        cb.grid(row=i+4, column=2, sticky="w", padx=10, pady=5)
        meatCheckboxes.append({"checkbox": cb, "variable": var})

    veggieCheckboxes = []
    for i, veggie in enumerate(toppings.veggies):
        var = BooleanVar(value=False)
        cb = Checkbutton(add_recipe_window, text=veggie.name, variable=var)
        cb.grid(row=i+4, column=3, sticky="w", padx=10, pady=5)
        veggieCheckboxes.append({"checkbox": cb, "variable": var})

    root.mainloop()
