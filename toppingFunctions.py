import tkinter as tk
from tkinter import ttk
from tkinter import *
from toppingData import fetchToppings, addData, deleteData, editData

#function called to load and reload toppings list
def loadToppings():
    toppings = fetchToppings()
    return toppings

def addToppingWindow(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, errorLbl, root):
    #adds topping to database
    def addTopping():
        name = newTopping.get()
        type = selected.get()
        if name and type:
            empty.grid_remove()
            success = addData(type, name)
            if success == 0:
                failed.grid()
            else:
                #refresh and close after adding
                failed.grid_remove()
                add_topping_window.destroy()
                refresh(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox)
                errorLbl.config(text=f"{name} was added!", fg="green")
                errorLbl.grid()        
        else:
             empty.grid()
    
    #closes when cancel button pressed
    def close():
        add_topping_window.destroy()
        
    #pop open new window
    add_topping_window = tk.Toplevel(root)
    add_topping_window.title("Add Topping")
    add_topping_window.transient(root)
    add_topping_window.grab_set()
    add_topping_window.geometry("450x300")

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
    addTBtn = Button(add_topping_window, text="Add", fg="green", command=addTopping)
    addTBtn.grid(row=3, column=1, pady=10, padx=10)

    #cancel button
    cancelBtn = Button(add_topping_window, text="Cancel", fg="red", command=close)
    cancelBtn.grid(row=4, column=1, pady=10, padx=10)

    #warning label
    failed = Label(add_topping_window, text="This topping already exists!", fg="red")
    failed.grid(row=5, column=1, pady=10, padx=10)
    failed.grid_remove()

    #enter fields label
    empty = Label(add_topping_window, text="Please enter all fields!", fg="red")
    empty.grid(row=4, column=1, pady=10, padx=10)
    empty.grid_remove()

#function to delete topping
def deleteTopping(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, listboxType, errorLbl, root):
    #get current listbox
    listbox = root.focus_get()

    #get listbox type
    if listbox in listboxType:
       
        #get index of current selection
        index = listbox.curselection()
        if index:
            #get type and name
            selected = listbox.get(index)
            toppingType = listboxType[listbox]
            
            #call delete function
            result = deleteData(toppingType, selected)
            if result == 1:
                 #delete from listbox and refresh
                 listbox.delete(index)
                 refresh(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox)
                 errorLbl.config(text=f"{selected} was deleted!", fg="green")
                 errorLbl.grid()
        else:
            errorLbl.config(text="Topping could not be deleted.", rg="red")
            errorLbl.grid()
    else:
         errorLbl.config(text="Select a topping to delete first.", rg="red")
         errorLbl.grid()

def getEdit(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, listboxType, errorLbl, root):
     #get current listbox
    listbox = root.focus_get()

    #get listbox type
    if listbox in listboxType:
       
        #get index of current selection
        index = listbox.curselection()
        if index:
            #get type and name
            selected = listbox.get(index)
            toppingType = listboxType[listbox]
            editToppingWindow(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, errorLbl, root, toppingType, selected)
        else:
            errorLbl.config(text="Topping could not be changed.", fg="red")
            errorLbl.grid()
    else:
        errorLbl.config(text="Select a topping to edit first.", fg="red")
        errorLbl.grid()

#function to change topping
def editToppingWindow(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox, errorLbl, root, type, name):
    def editTopping():
        newName = newTopping.get()
        if name and type:
            #calls function to edit data in database
            success = editData(type, name, newName)
            if success == 0:
                #tells user the topping already exists
                failed.grid()
            else:
                #close window
                failed.grid_remove()
                edit_window.destroy()
                #refresh list boxes
                refresh(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox)
                errorLbl.config(text=f"{name} was changed!", fg="green")
                errorLbl.grid()        
        else:
             #ask user to fill all fields
             empty.config(text="Please enter all fields!")
    
    #closes when cancel button pressed
    def close():
        edit_window.destroy()

    #pop open new window
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Toppings")
    edit_window.transient(root)
    edit_window.grab_set()
    edit_window.geometry("450x300")

    #title label
    addTitle = Label(edit_window, text="Edit Topping")
    addTitle.config(font=('Helvetica bold', 18))
    addTitle.grid(row=0, column=0, pady=10, padx=10)

    #select type of topping
    typeLabel = Label(edit_window, text="Topping Type:")
    typeLabel.grid(row=1, column=0, pady=10, padx=10)

    #combo box for selecting topping type
    toppingCombo = Label(edit_window, text=type)
    toppingCombo.grid(row=1, column=1, pady=10, padx=10)

    #label for new topping
    entryLabel = Label(edit_window, text="Topping Name:")
    entryLabel.grid(row=2, column=0, pady=10, padx=10)

    #text field for new topping
    newTopping = Entry(edit_window)
    newTopping.grid(row=2, column=1, pady=10, padx=10)
    newTopping.insert(0, name)

    #add button
    addTBtn = Button(edit_window, text="Change", fg="blue", command=editTopping)
    addTBtn.grid(row=3, column=1, pady=10, padx=10)

    #cancel button
    cancelBtn = Button(edit_window, text="Cancel", fg="red", command=close)
    cancelBtn.grid(row=4, column=1, pady=10, padx=10)

    #warning label
    failed = Label(edit_window, text="This topping already exists!", fg="red")
    failed.grid(row=5, column=1, pady=10, padx=10)
    failed.grid_remove()

    #enter fields label
    empty = Label(edit_window, text=" ", fg="red")
    empty.grid(row=4, column=1, pady=10, padx=10)

     
def refresh(saucesListbox, cheesesListbox, meatsListbox, veggiesListbox):
    #get toppings objects
    toppings = loadToppings()

    #delete previous data from listboxes
    saucesListbox.delete(0, END)
    cheesesListbox.delete(0, END)
    meatsListbox.delete(0, END)
    veggiesListbox.delete(0, END)

    #updated listboxes
    for sauce in toppings.sauces:
            saucesListbox.insert(END, sauce.name)
    saucesListbox.config(height=len(toppings.sauces))
    for cheese in toppings.cheeses:
            cheesesListbox.insert(END, cheese.name)
    cheesesListbox.config(height=len(toppings.cheeses))
    for meat in toppings.meats:
            meatsListbox.insert(END, meat.name)
    meatsListbox.config(height=len(toppings.meats))
    for veggie in toppings.veggies:
            veggiesListbox.insert(END, veggie.name)
    veggiesListbox.config(height=len(toppings.veggies))