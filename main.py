from tkinter import messagebox
from pizzaGUI import tkinterManager
import socket

#run window
#checks if there is an internet connection 
#because the database cannot be accessed without internet
#and the program requires the internet to be used
def hasConnection():
    try: 
        socket.create_connection(("www.google.com", 80)) 
        return True
    except OSError:
        pass
    return False

#if it is connected to the internet the program runs normally, 
#if not an error message asks the user to connect to the internet
connection = hasConnection()
if connection == True:
    root = tkinterManager()
    root.minsize(width=350, height=500)
    root.mainloop()
else:
    messagebox.showerror("No internet connection", "This program requires an internet connection to connect to the MongoDB Database. Please connect to the internet and re-run the program")