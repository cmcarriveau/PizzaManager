import tkinter as tk
from tkinter import *

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
root.mainloop()