# PizzaManager
 A program where chefs can manage pizza and their toppings.

* How to build and run the program locally *
1. Download the project folder from Github 
2. Unzip the folder
3. Double click main.exe to build and run the program on your machine

* How to run the tests *
1. Open the project folder in your IDE
2. Open the terminal in the IDE and ensure that python is installed by typing python --version
    -If it's not installed, then download it to your IDE
3. Type the command python -m unittest tests.py to run the unit testing script

* About the program *
Database
- All of the information is stored using MongoDb online database. Since the program needs to connect to the database to run, it
    requires internet.

Home Page
- This page allows the user to access the Store owner page or the Pizza chef page.

Store Owner Page
- Toppings can be managed on this page.
- Add topping: A separate window opens where users can choose what type of topping they want to add (sauces, cheeses, meats, and veggies),
    and it allows the users to name their topping. They cannot add two of the same topping with the same type.
- Edit topping: After the user selects a pre-existing topping from the list, the edit page opens. Here users can change the name of the topping.
- Delete topping: Once the user selects a pre-existing topping from the list, they can select the delete button, and it is automatically removed.

Pizza Chef Page
- Pizza recipes can be managed on this page.
- Add recipe: A separate window opens where the user can see all of the toppings that are available. They can select the toppings they want to 
    add to their recipe by clicking the checkbox. Once they select their toppings and name the recipe, they can add the recipe to the list.
- Edit topping: After the user selects a recipe using the radio button, they can click the edit button and open a new window. The new window
    displays all the toppings that are already in the recipe by have their buttons pre-selected. The user can remove or add new toppings to the
    recipe.
- Delete topping: After the user selects a recipe using the radio button, they can click the delete button, and the recipe is removed.