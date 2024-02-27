import tkinter as tk
from tkinter import ttk
from tkinter import *
from toppingFunctions import loadToppings, addToppingWindow, deleteTopping, getEdit
from recipeData import fetchRecipes
from recipeFunctions import deleteRecipe

#class for displaying selected page
class tkinterManager(tk.Tk):
    #function to display current page used in class
    def display(self, i):
        frame = self.frames[i]
        frame.tkraise()

    #initalize tkinterManager class
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        #container for pages within window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #array to hold different pages
        self.frames = {}

        #iterate through differnt pages to initalize
        #a frame for each one
        for i in (HomePage, OwnerPage, ChefPage):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.display(HomePage)

#---------------HOME PAGE---------------
#home page layout
class HomePage(tk.Frame):
    #initalize home page class
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        #Labels
        welcome = Label(self, text="  Welcome to Pizza Manager!")
        welcome.config(font=('Helvetica bold', 18))
        welcome.grid(row=0, column=0, pady=10, padx=10, sticky=E)

        message = Label(self, text="Please select your job:")
        message.grid(row=1, column=0, pady=10, padx=10)

        #Buttons
        #brings user to owner manager page
        ownerBtn = Button(self, text="Store Owner", fg="blue", command=lambda: controller.display(OwnerPage))
        ownerBtn.grid(row=4, column=0, pady=10, padx=10)

        #brings user to chef manager page
        chefBtn = Button(self, text="Pizza Chef", fg="red", command=lambda: controller.display(ChefPage))
        chefBtn.grid(row=5, column=0, pady=10, padx=10)

#---------------OWNER PAGE---------------
#owner page layout
class OwnerPage(tk.Frame):
    #initalize owner page class
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        #home button
        homeBtn = Button(self, text="< Home", fg="blue", command=lambda: controller.display(HomePage))
        homeBtn.grid(row=0, column=0, pady=10, padx=10, sticky=W)

        #title label
        title = Label(self, text="Topping Manager")
        title.config(font=('Helvetica bold', 18))
        title.grid(row=1, column=1, padx=10)

        #load list
        toppings = loadToppings()

        #print list
        #sauce label
        saucesLabel = Label(self, text="Sauces:")
        saucesLabel.grid(row=3, column=0, pady=10, padx=10)
        #sauce listbox
        sauceNum = len(toppings.sauces)
        saucesListbox = Listbox(self, width=20, height=sauceNum)
        for sauce in toppings.sauces:
            saucesListbox.insert(END, sauce.name)
        saucesListbox.grid(row=3, column=1, pady=10, padx=10)

        #cheese label
        cheesesLabel = Label(self, text="Cheeses:")
        cheesesLabel.grid(row=4, column=0, pady=10, padx=10)
        #cheese listbox
        cheeseNum = len(toppings.cheeses)
        cheesesListbox = Listbox(self, width=20, height=cheeseNum)
        for cheese in toppings.cheeses:
            cheesesListbox.insert(END, cheese.name)
        cheesesListbox.grid(row=4, column=1, pady=10, padx=10)

        #meat label
        meatsLabel = Label(self, text="Meats:")
        meatsLabel.grid(row=5, column=0, pady=10, padx=10)
        #meat listbox
        meatsNum = len(toppings.meats)
        meatsListbox = Listbox(self, width=20, height=meatsNum)
        for meat in toppings.meats:
            meatsListbox.insert(END, meat.name)
        meatsListbox.grid(row=5, column=1, pady=10, padx=10)

        #veggie label
        veggiesLabel = Label(self, text="Veggies:")
        veggiesLabel.grid(row=6, column=0, pady=10, padx=10)
        #veggie listbox
        veggieNum = len(toppings.veggies)
        veggiesListbox = Listbox(self, width=20, height=veggieNum)
        for veggie in toppings.veggies:
            veggiesListbox.insert(END, veggie.name)
        veggiesListbox.grid(row=6, column=1, pady=10, padx=10)

        #dictionary for getting the type
        listboxType = {
            saucesListbox: "sauces",
            cheesesListbox: "cheeses",
            meatsListbox: "meats",
            veggiesListbox: "veggies"
        }

        #add button
        addBtn = Button(self, text="Add", fg="green", command=lambda: addToppingWindow(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, errorLbl, self))
        addBtn.grid(row=2, column=0, pady=10, padx=10, sticky=E)

        #edit button 
        editBtn = Button(self, text="Edit", fg="blue", command=lambda: getEdit(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, listboxType, errorLbl, self))
        editBtn.grid(row=2, column=1, pady=10, padx=10)

        #delete button
        delBtn = Button(self, text="Delete", fg="red", command=lambda: deleteTopping(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, listboxType, errorLbl, self))
        delBtn.grid(row=2, column=2, pady=10, padx=10, sticky=W)

        #error label 
        errorLbl = Label(self, text="", fg="red")
        errorLbl.grid(row=7, column=1, pady=10, padx=10)
        errorLbl.grid_remove()


#---------------CHEF PAGE---------------
#chef page layout
        
class ChefPage(tk.Frame):
    #initalize chef page class
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        #home button
        homeBtn = Button(self, text="< Home", fg="blue", command=lambda: controller.display(HomePage))
        homeBtn.grid(row=0, column=0, pady=10, padx=10)

        #title label
        title = Label(self, text="Recipe Manager")
        title.config(font=('Helvetica bold', 18))
        title.grid(row=1, column=1, padx=10)

        #fetch recipe data
        recipeBook = fetchRecipes()

        #load them in listbox
        # Create a listbox to display recipe names
        recipeListboxes = []
        selected = IntVar()
        for i, recipe in enumerate(recipeBook.recipes):
            #list recipe names
            listbox = tk.Listbox(self, width=27, height=(len(recipe.ingredients) + 1), selectmode=NONE)
            listbox.grid(row=i+3, column=1, padx=10, pady=10)
            recipeListboxes.append(listbox)
            
            #list ingredients
            recipe = recipeBook.recipes[i]
            recipeListboxes[i].insert(END, recipe.recipeName)
            for ingredient in recipe.ingredients:
                recipeListboxes[i].insert(END, f"- {ingredient.name}")
  
            #create radiobuttons for selection
            for i, recipe in enumerate(recipeBook.recipes):
                rb = Radiobutton(self, text="Select", variable=selected, value=i, takefocus=False)
                rb.grid(row=i+3, column=2, padx=(0, 10), pady=10)
         
        #function buttons
        #add button
        addBtn = Button(self, text="Add", fg="green")
        addBtn.grid(row=2, column=0, pady=10, padx=10, sticky=E)

        #edit button 
        editBtn = Button(self, text="Edit", fg="blue")
        editBtn.grid(row=2, column=1, pady=10, padx=10)

        #delete button
        delBtn = Button(self, text="Delete", fg="red", command=deleteRecipe(selected))
        delBtn.grid(row=2, column=2, pady=10, padx=10, sticky=W) 


