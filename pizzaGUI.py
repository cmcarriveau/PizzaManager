import tkinter as tk
from tkinter import ttk
from tkinter import *
from toppingFunctions import loadToppings, addToppingWindow, deleteTopping, getEdit
from recipeFunctions import deleteRecipe, addRecipeWindow, loadRecipes, editRecipeWindow

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

        #print lists
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

        def refreshRecipes():
            #destroy all old listboxes and buttons
            for listbox in self.recipeListboxes:
                listbox.destroy()
            self.recipeListboxes = []

            for radiobutton in self.recipeRadiobuttons:
                radiobutton.destroy()
            self.recipeRadiobuttons = []

            recipeBook = loadRecipes()
            #create new listboxes and radiobuttons based on updated recipe data
            #and write new information into the listboxes and radiobuttons
            for i, recipe in enumerate(recipeBook.recipes):
                listbox = Listbox(self, width=27, height=(len(recipe.ingredients) + 1), selectmode=NONE)
                listbox.grid(row=i+4, column=1, padx=10, pady=10)
                self.recipeListboxes.append(listbox)

                listbox.insert(END, recipe.recipeName)
                for ingredient in recipe.ingredients:
                    listbox.insert(END, f"- {ingredient.name}")

                for i, recipe in enumerate(recipeBook.recipes):
                    rb = Radiobutton(self, text="Select", variable=self.selected, value=i, takefocus=False)
                    rb.grid(row=i+4, column=2, padx=(0, 10), pady=10)
                    self.recipeRadiobuttons.append(rb)
        
        #calls delete functions
        def callDelete():
            deleteRecipe(self.selected, errorLbl, self.recipeListboxes, self.recipeRadiobuttons)
            refreshRecipes()

        #calls add function
        def callAdd():
            addRecipeWindow(self, errorLbl, addCallback)

        #calls edit functions
        def callEdit():
            index = self.selected.get()
            if index == -1:
                #if none are selected, print error message
                errorLbl.config(text="Select a recipe to edit", fg="red")
            else:
                #get the name of the recipe to delete
                recipeBook = loadRecipes()
                toEdit = recipeBook.recipes[index]
                editRecipeWindow(self, errorLbl, addCallback, toEdit)

        #calls back from other window
        def addCallback(result):
            #when it is back call refreshRecipes
            if result:
                self.after(100, lambda: refreshRecipes())

        #home button
        homeBtn = Button(self, text="< Home", fg="blue", command=lambda: controller.display(HomePage))
        homeBtn.grid(row=0, column=0, pady=10, padx=10)

        #title label
        title = Label(self, text="Recipe Manager")
        title.config(font=('Helvetica bold', 18))
        title.grid(row=1, column=1, padx=10)

        #fetch recipe data
        recipeBook = loadRecipes()

        #load them in listbox
        # Create a listbox to display recipe names
        self.recipeListboxes = []
        self.recipeRadiobuttons = []
        self.selected = IntVar(value=-1)
        for i, recipe in enumerate(recipeBook.recipes):
            #list recipe names
            listbox = Listbox(self, width=27, height=(len(recipe.ingredients) + 1), selectmode=NONE)
            listbox.grid(row=i+4, column=1, padx=10, pady=10)
            self.recipeListboxes.append(listbox)
            
            #list ingredients
            recipe = recipeBook.recipes[i]
            self.recipeListboxes[i].insert(END, recipe.recipeName)
            for ingredient in recipe.ingredients:
                self.recipeListboxes[i].insert(END, f"- {ingredient.name}")
  
        #create radiobuttons for selection
        for i, recipe in enumerate(recipeBook.recipes):
            rb = Radiobutton(self, text="Select", variable=self.selected, value=i, takefocus=False)
            rb.grid(row=i+4, column=2, padx=(0, 10), pady=10)
            self.recipeRadiobuttons.append(rb)
         
        #error label
        errorLbl = Label(self, text = " ", fg="red")
        errorLbl.grid(row=3, column=1, pady=10, padx=10)
         
        #function buttons
        #add button
        addBtn = Button(self, text="Add", fg="green", command=lambda: callAdd())
        addBtn.grid(row=2, column=0, pady=10, padx=10)

        #edit button 
        editBtn = Button(self, text="Edit", fg="blue", command=lambda: callEdit())
        editBtn.grid(row=2, column=1, pady=10, padx=10)

        #delete button
        delBtn = Button(self, text="Delete", fg="red", command=lambda: callDelete())
        delBtn.grid(row=2, column=2, pady=10, padx=10)




