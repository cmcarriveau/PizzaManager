from tkinter import *

#---------button functions---------
#function to display pizza topping manager for store owners
def loadOwner():
    #change page titles
    welcome.grid_forget()
    message.configure(text="Manage Pizza Toppings")

    #remove old buttons
    ownerBtn.grid_forget()
    chefBtn.grid_forget()

#function to display pizza manager for chefs
def loadChef():
    #change page titles
    welcome.grid_forget()
    message.configure(text="Manage Pizza Recipes")

    #remove old buttons
    ownerBtn.grid_forget()
    chefBtn.grid_forget()


#create root window
root = Tk()

#name window
root.title("Pizza Manager")

#set geometry widthxheight
root.geometry('750x500')
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)

#---------home page---------
#information labels
welcome = Label(root, text="Welcome to Pizza Manager!")
welcome.grid(row=0, column=0)

message = Label(root, text="Please select your job:")
message.grid(row=1, column=0)

#brings user to owner manager page
ownerBtn = Button(root, text="Store Owner", fg="red", command=loadOwner)
ownerBtn.grid(row=4, column=0)

#brings user to chef manager page
chefBtn = Button(root, text="Pizza Chef", fg="red", command=loadChef)
chefBtn.grid(row=5, column=0)

#---------store owner page---------


#---------pizza chef page---------

#execute
root.mainloop()