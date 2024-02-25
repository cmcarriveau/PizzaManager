import tkinter as tk
from tkinter import ttk
from tkinter import *
from data import fetchToppings, addData

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


#home page layout
class HomePage(tk.Frame):
    #initalize home page class
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        #Labels
        welcome = Label(self, text="Welcome to Pizza Manager!")
        welcome.config(font=('Helvetica bold', 18))
        welcome.grid(row=0, column=0, pady=10, padx=10)

        message = Label(self, text="Please select your job:")
        message.grid(row=1, column=0, pady=10, padx=10)

        #Buttons
        #brings user to owner manager page
        ownerBtn = Button(self, text="Store Owner", fg="red", command=lambda: controller.display(OwnerPage))
        ownerBtn.grid(row=4, column=0, pady=10, padx=10)

        #brings user to chef manager page
        chefBtn = Button(self, text="Pizza Chef", fg="red", command=lambda: controller.display(ChefPage))
        chefBtn.grid(row=5, column=0, pady=10, padx=10)


#function called to load and reload toppings list
def loadToppings():
    toppings = fetchToppings()
    return toppings

def addToppingWindow():
    def addTopping():
        name = newTopping.get()
        type = selected.get()
        addData(type, name)
        add_topping_window.destroy()

    #pop open new window
    add_topping_window = tk.Toplevel(root)
    add_topping_window.title("Add")
    add_topping_window.transient(root)
    add_topping_window.grab_set()
    add_topping_window.geometry("400x300")

    #title label
    addTitle = Label(add_topping_window, text="Add Topping")
    addTitle.config(font=('Helvetica bold', 18))
    addTitle.grid(row=0, column=0, pady=10, padx=10)

    #select type of topping
    typeLabel = Label(add_topping_window, text="Select Topping Type:")
    typeLabel.grid(row=1, column=0, pady=10, padx=10)

    #combo box for selecting topping type
    selected = StringVar()
    toppingCombo = ttk.Combobox(add_topping_window, textvariable=selected, state='readonly')
    toppingCombo['values'] = ('sauces', 'cheeses', 'meats', 'veggies')
    toppingCombo.grid(row=1, column=1, pady=10, padx=10)

    #label for new topping
    entryLabel = Label(add_topping_window, text="Topping Name:")
    entryLabel.grid(row=2, column=0, pady=10, padx=10)

    #text field for new topping
    newTopping = Entry(add_topping_window)
    newTopping.grid(row=2, column=1, pady=10, padx=10)

    #add button
    addTBtn = Button(add_topping_window, text="Add", command=addTopping)
    addTBtn.grid(row=3, column=1, pady=10, padx=10)

#owner page layout
class OwnerPage(tk.Frame):
    #initalize owner page class
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        #home button
        homeBtn = Button(self, text="< Home", fg="blue", command=lambda: controller.display(HomePage))
        homeBtn.grid(row=0, column=0, pady=10, padx=10)

        #title label
        title = Label(self, text="Topping Manager")
        title.config(font=('Helvetica bold', 18))
        title.grid(row=1, column=1, padx=10)

        #add button
        addBtn = Button(self, text="Add", command=addToppingWindow)
        addBtn.grid(row=2, column=1, pady=10, padx=10)
        #edit button 

        #delete button

        #load list
        toppings = loadToppings()

        #print list
        #sauce label
        saucesLabel = Label(self, text="Sauces:")
        saucesLabel.grid(row=3, column=0, pady=10, padx=10)
        #sauce listbox
        sauceNum = len(toppings.sauces)
        saucesListbox = Listbox(self, height=sauceNum)
        for sauce in toppings.sauces:
            saucesListbox.insert(END, sauce.name)
        saucesListbox.grid(row=3, column=1, pady=10, padx=10)

        #cheese label
        cheesesLabel = Label(self, text="Cheeses:")
        cheesesLabel.grid(row=4, column=0, pady=10, padx=10)
        #cheese listbox
        cheeseNum = len(toppings.cheeses)
        cheesesListbox = Listbox(self, height=cheeseNum)
        for cheese in toppings.cheeses:
            cheesesListbox.insert(END, cheese.name)
        cheesesListbox.grid(row=4, column=1, pady=10, padx=10)

        #meat label
        meatsLabel = Label(self, text="Meats:")
        meatsLabel.grid(row=5, column=0, pady=10, padx=10)
        #meat listbox
        meatsNum = len(toppings.meats)
        meatsListbox = Listbox(self, height=meatsNum)
        for meat in toppings.meats:
            meatsListbox.insert(END, meat.name)
        meatsListbox.grid(row=5, column=1, pady=10, padx=10)

        #veggie label
        veggiesLabel = Label(self, text="Veggies:")
        veggiesLabel.grid(row=6, column=0, pady=10, padx=10)
        #veggie listbox
        veggieNum = len(toppings.veggies)
        veggiesListbox = Listbox(self, height=veggieNum)
        for veggie in toppings.veggies:
            veggiesListbox.insert(END, veggie.name)
        veggiesListbox.grid(row=6, column=1, pady=10, padx=10)


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

        #function buttons 

root = tkinterManager()
root.minsize(width=350, height=500)
root.mainloop()