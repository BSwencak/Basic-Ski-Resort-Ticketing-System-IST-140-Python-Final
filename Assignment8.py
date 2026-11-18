"""
Author: Brady Swencak
Class: IST 140 001
Assignment: LM8 - Coding Assignment & Review
Date: 12/14/2025
"""

#Ski Resort Customer Ticketing System

customers = {} #intializes customer dictionary
signed_in = False #globally sets signed in to false forcing our user into signing in and to use later
user = "" #globally sets user blank so we can call back to it and use it outside the functions


'''Main Program Functions
- menu_1: Create User, Sign In, Exit
- menu_2: Purchase Ticket, Purchase Season Pass, Delete User, Sign Out
- menu_3: Display Customers, Import Customers, Export Customers, Delete Customer, Sign Out
'''


#creates ADMIN user, password could be better but this is just a demo project
customers["ADMIN"] = {"name": "ADMIN", "email": "ADMIN", "password": "ADMIN", "tickets":0, "season pass": "Y"}


'''Create User allows person to create their user in our system
taking a name, username, password and email
makes sure their username is unique and password is more than 8 characters'''
def create_user():
    name = input("\nEnter your name: ").strip().title() #takes name input, set first letters capital
    username = input("Enter a username: ").strip() #takes username input

    while username in customers: #checks for unique username
        username = input("\nThat username is taken. Please choose a different one.")

    email = input("Enter your email: ").strip().lower() #takes email inout, lowers to simplify search
    while email in [j["email"] for j in customers.values()]:
        email = input("Email already has an account, enter your email: ").strip().lower() # ensures email isn't already being used
    password = input("Enter your password: ").strip() #takes password input

    while not len(password) >= 8: #ensures password is more than 8 characters long
        password = input("Password MUST be more than 8 characters long!"
                         "\nEnter your password: ").strip()

    #adds customer/username to dictionary and adds the rest of their information, as well as setting their
    #tickets to a default of 0 and season pass to a default of N (no/none)
    customers[username] = {"name": name, "email": email, "password": password, "tickets": 0, "season pass": "N"}


'''Sign In allows a user to sign into our system
initiates globals of user and signed_in 
takes username and password input, confirms that user exists and password for user is correct, updates signed_in & user global'''
def sign_in():
    global user, signed_in #intiates global variables
    username = input("\nEnter your username: ").strip() #takes username input for login

    if username in customers: #checks that user is in the system
        password = input("Enter your password: ").strip() # takes password input for login

        if password == customers[username]["password"]: #checks that the password is correct to that user
            print("Welcome " + username + "!") #sends welcome message to user
            signed_in = True #updates signed_in global to be True stating that a user is signed in
            user = username #updates user global to the signed-in users username
        else:
            print("\nIncorrect password.") #if password for that user is incorrect
            signed_in = False #double checks that global signed_in stays False
    else:
        print("\nUser does not exist.") #if the user is not in the system
        signed_in = False #double checks that global signed_in stays False


'''Purchase Ticket allows a signed in user to buy ski tickets (tickets aren't for specific days just general passes)
makes sure that user is signed_in, takes amount for tickets wanting to be purchased, calculates cost (25%) of for season pass holders
takes money input, only exact amount as this system would only be used digitally and can't give money back
checks that payment is correct, allows transaction to be cancelled, updates user ticket amount in the dictionary'''
def purchase_ticket():
    if signed_in: #checks that user is signed in
        amount = 0 #initiates amount to be 0 so it can be used later and is confirmed clear

        while amount < 1: #checks that the user is actually purchasing tickets
            try:
                amount = int(input("How many tickets would you like to purchase?")) #while no error, takes input for ticket amount

                if amount > 0: #while the user is purchasing tickets
                    payment = 0 #payment initiated at 0 to confirm that it is clear
                    price = amount * 50 #updates price amount, $50 per ticket

                    if customers[user]["season pass"] == "Y": #checks if user is a season pass holder
                        print(f"You get 25% off tickets because you are a Season Pass holder, " #if user is a season pass holder they get 25% off
                              f"previous price: ${price}, new price ${price-(price*.25)}") #ensures no decimal in listed price
                        price = price-(price*.25) #updates discounted price

                    try:
                        payment = float(input(f"Enter payment for {amount} tickets, ${price} (must be exact, 0 to cancel): ")) #takes payment input

                    except ValueError: #if payment input is not a number, ensuring program continues on error
                        print("\nIncorrect monetary input.")

                    while payment != price: #while payment is not sufficient
                        if payment == 0: #if payment is 0 (cancel), user cancels the transaction
                            return #ensures menu return

                        else:
                            try:
                                #if payment is insufficient & not 0 to cancel, new payment is taken
                                payment = int(input(f"Enter payment for {amount} tickets, ${price} (must be exact, 0 to cancel): "))

                            except ValueError: #if payment input is not a number, ensuring program continues on error
                                print("\nIncorrect monetary input.")

                    customers[user]["tickets"] = customers[user]["tickets"] + amount #adds new tickets to users ticket amount

            except ValueError:
                print("\nIncorrect input.") #if ticket amount is not a number, ensures program continues on error

    else:
        #if user is not signed in, they cannot purchase tickets (this should not occur given how the system is set up but is here in case)
        print("You are NOT signed in, please sign in to purchase tickets.")
        return #ensures menu return


'''Purchase Season Pass allows signed in user to purchase a season pass
makes sure user is signed in, takes amount of season pass, only allows one per user
allows user to cancel transaction, updates user season pass status in the dictionary'''
def purchase_season_pass():
    if signed_in: #checks user is signed in
        if customers[user]["season pass"] == "Y": #checks if user has season pass
            return #returns to menu if user has season pass

        payment = 0 #initiates payment as 0 to clear it

        while payment!=500: #ensure user enters proper payment amount
            try:
                payment = int(input("Season Pass will cost $500, please enter payment (must be exact amount, 0 to cancel): ")) #takes payment input

                if payment == 0: #if payment is 0 (cancel) cancels transaction
                    return #ensures menu return

                else:
                    customers[user]["season pass"] = "Y" #if payment is sufficient updates user to have season pass, Y (yes)

            except ValueError:
                print("\nIncorrect monetary input.") #if payment amount is not a number, ensures program continues on error

    else:
        # if user is not signed in, they cannot purchase tickets (this should not occur given how the system is set up but is here in case)
        print("You are NOT signed in, please sign in to purchase season.")
        return #ensures menu return


'''Delete User allows user to delete their account
they must re enter their password to delete their account
can only delete their account and no others, if user ADMIN, account cannot be deleted (program only works for user but this is just in case)
ensures password is correct to that account before deleting'''
def delete_user():
    password = input("\nEnter your password to delete your account: ").strip() #takes password input for account deleting

    if customers[user]["password"] == password: #ensures that they have the correct password for their account
        if user == "ADMIN":
            print("CANNOT DELETE ADMIN USER") #makes sure if user is admin account can't be deleted (this should not occur)
            return #ensures menu return

        else:
            print(f"Your account, {user} has been deleted, sorry to see you go.") #goodbye statement to user
            del customers[user] #deletes user and their information from dictionary

    else:
        print("\nIncorrect password.") #if user password is incorrect doesn't allow user to delete their account



'''Delete Customer allows ADMIN to delete any customer from the system
ensure that the username they're deleting cannot be ADMIN'''
def delete_customer():
    username = input("\nEnter username you want to delete: ").strip() #takes username input for deletion

    if username in customers: #checks that user exists in the dictionary
        if username == "ADMIN":
            print("CANNOT DELETE ADMIN USER") #makes sure if user entered for delete is ADMIN that they cannot delete it
            return #ensures menu return

        else:
            print(f"The user, {username} has been DELETED.") #confirmation statement as to user deletion
            del customers[username] #deletes user and their information from the dictionary

    else:
        print(f"\nUser, {username} does NOT exist.") #if user stated does not exist in the dictionary


'''Display Customers, allows ADMIN to display a full, neat, list of customers and their information'''
def display_customers():
    if not customers == {}: #checks if there is customer information in the dictionary
        print("\nCustomers:") #title

        for customer, j in customers.items(): #goes through all customers in dictionary and their email, password & season pass
            print(f"Username: {customer:<25}   Name:{j["name"]:<25}   Email: {j["email"]:<25}  Password: {j["password"]:<30}  Tickets:{j["tickets"]:<5}  Season Pass: {j["season pass"]:<5}") #outputs player name, email, and attendance cleanly
            #PRINTS CUSTOMER LIST NEATLY

    else: #if there are no customers in the dictionary (there should always be ADMIN but just in case)
        print("\nCurrently no users.\n")

    print("") #spacer


'''Import Customers, allows ADMIN to batch import previous customer lists from a .txt file found in the same folder as the project file
ensures that program continues on line error, input .txt must have all 6 data fields filled out to import an account
if account in the .txt does not have all 6 data fields, account will be skipped'''
def import_customers():
    customers_file = input("Enter filename (including .txt): ").strip()  # takes input for the .txt, only works in same folder
    try:
        file_in = open(customers_file, "r")  # opens the file and sets it to read only
        customers_in = 0  #initiates counter for how many players are inputted

        for line in file_in:  #iterates over all lines in the .txt filed
            line = line.strip()  #strips the line of blank space

            try:
                username_in, name_in, email_in, password_in, tickets_in, sp_in = line.split(",")  #splits lines in the .txt file by commas

                if username_in in customers:
                    raise ValueError("Username already exists.")  #ensures user doesn't already exist

                elif email_in in [j["email"] for j in customers.values()]:
                    raise ValueError("Email already used.") #ensures email isn't already being used

                elif sp_in.strip().upper() not in ("Y","N"):
                    raise ValueError("Season Pass must be Y or N.") #ensure proper values for season pass status


            except ValueError as e:  #if there is an issue with the input value on a line, errors
                print(f"Error on line, {line}")  #error message
                print(f"Reason: {e}\n") #reason message if previously stated
                continue  #continues the import despite the error

            username_in = username_in.strip() #strips whitespace from username
            password_in = password_in.strip() #strips whitespace from password
            name_in = name_in.strip().title()  #strips whitespace from name and makes it proper case
            email_in = email_in.strip().lower()  #strips whitespace from email and makes it lower
            tickets_in = int(tickets_in.strip()) #strips white space from ticket amount
            sp_in = sp_in.strip() #strips white space from season pass status

            #creates user and adds information listed to that user
            customers[username_in] = {"name": name_in, "email": email_in, "password": password_in, "tickets": tickets_in, "season pass": sp_in}

            customers_in += 1  #adds to number of customers imported

        #states the file and that it succeeded and how many were imported
        print(f"{customers_file} successfully imported {customers_in} customers into the dictionary.\n")

        file_in.close()  #closes the file

    except FileNotFoundError:  #if the file is not found
        #states that the file isn't found and needs to be in same folder as project and end with .txt
        print(f"File {customers_file} not found. File MUST be in the same folder as python file and .txt MUST be included.\n")


'''Export Customers, allows ADMIN to output a full, neat, list of customers and their information to be imported else where
or to be saved as a .txt file for other use outside of the project
any name can be chosen for the export as it creates a new file
ensures ADMIN user is not exported'''
def export_customers():
    customers_file = input("Enter filename (including .txt): ").strip()
    #takes input for the .txt, will create the .txt file in the same folder as project, it will write to this file
    customers_out = 0 #initiates customers_out counter at 0

    try:
        if not customers_file.endswith(".txt"): #checks that file has .txt at the end
            raise FileNotFoundError #raises error if not

        file_out = open(customers_file, "w")  #opens the file and sets it to write only

        for username, j in customers.items(): #iterates through all customers
            if username == "ADMIN": #ensures ADMIN user is not exported
                print("Cannot export user ADMIN.")
                continue #skips exporting ADMIN

            #splits data up to be correctly outputted onto .txt files' lines
            line = f"{username}, {j["name"]}, {j["email"]}, {j["password"]}, {j["tickets"]}, {j["season pass"]}\n"
            file_out.write(line) #writes the created line to the file
            customers_out+=1 #increments the customers_out counter

        #confirms number of customers exported and to what file
        print(f"{customers_out} customers have been successfully exported to file {customers_file}.\n")
        file_out.close()  #closes the file


    except FileNotFoundError: #error if file is not found allowing program to continue still
        print(f"\nFile,{customers_file} MUST END with .txt")


'''Menu 1 initiates global variables (user, signed_in)
outputs menu options and ensures proper input response
chooses what to do based on menu choice'''
def menu_1():
    global user, signed_in #initiates global variables

    menu_items = ["Create User", "Sign In", "Exit"] #initiates menu options

    #header, states to user that nothing can be done without signing in
    print("\nPlease sign in to purchase tickets and manage account.")

    while True: #ensures while loop continues while True
        print("Menu Options:") #menu title

        for count, items in enumerate(menu_items, start=1):
            output = str(count) + ": " + str(items)
            print(output)
            # outputs menu

        try:
            choice = int(input("Enter your menu choice(must be 1-3): "))
            #validates for correct menu choice

        except ValueError: #ensures program continues on error
            print("Invalid Choice. Try again.\n")
            continue

        if choice == 1:
            create_user() #if choice 1, function create_user is called allowing user to create an account
            print("USER CREATED") #confirms that user has been created, does not sign user, in only creates account

        elif choice == 2:
            sign_in() #if choice 2, allows user to sign in
            if signed_in: #checks that user is signed in before choosing next menu option
                if user == "ADMIN": #checks if user is ADMIN
                    menu_3() #if user is ADMIN, ADMIN is entered into the ADMIN menu, menu_3
                else:
                    menu_2() #otherwise if user is signed in to a regular account, they get menu_2
                return #ensures menu return

            else:
                #if user fails to sign in, explains that user needs to be signed in to use the system
                print("\nPlease sign in to purchase tickets and manage account.")

        elif choice == 3: #if choice is 3, program exits
            exit()

        else:
            print("\nInvalid Choice. Try again.\n") #if none of the choices are chosen, reasks for new choice


'''Menu 2, this menu is only for regular users, not for ADMIN
initiates global variables (user, signed_in)
lists the menu 2 menu options and ensures correct choice
chooses what to do based on menu choice'''
def menu_2():
    global signed_in, user #initiates global variables

    menu_items = ["Purchase Ticket", "Purchase Season Pass", "Delete User", "Sign Out"] #initiates menu options
    choice = 0 #initiates choice variable to 0

    while signed_in: #ensures this only occurs while user is signed in
        print("\nMenu Options:") #menu title
        for count, items in enumerate(menu_items, start=1):
            output = str(count) + ": " + str(items)
            print(output)
            #outputs menu

        try:
            choice = int(input("Enter your menu choice(must be 1-4): ")) #validates for correct menu choice
        except ValueError:
            print("Invalid Choice. Try again.\n") #if choice is not an int, ensures program continues on error

        if choice == 1:
            purchase_ticket() #if choice 1, allows signed-in user to purchase tickets

        elif choice == 2:
            purchase_season_pass() #if choice 2, allows signed-in user to purchase season pass

        elif choice == 3:
            delete_user() #if choice 3, allows user to delete their account

            if user not in customers: #checks if their user was deleted
                signed_in = False #if their user was deleted, global signed_in gets reset
                user = "" #if their user was deleted, global user get reset
                return #ensure menu return

        elif choice == 4:
            print(f"Signing out {user}") #if choice 4 user gets signed out
            signed_in = False #resets global signed_in
            user = "" #resets global user
            return #ensures menu return

        else:
            print("\nInvalid Choice. Try again.\n") #if menu choice is invalid


'''Menu 3, this menu is only for ADMIN, regular users cannot access
initiates global variables (user, signed_in)
lists the menu 3 menu options and ensures correct choice
chooses what to do based on menu choice'''
def menu_3():
    global signed_in, user #initiates global variables
    menu_items = ["Display Customers", "Import Customers", "Export Customers", "Delete Customer", "Sign Out"] #initiates menu options
    choice = 0 #initiates choice variable to 0

    while signed_in and user == "ADMIN": #ensures this only occurs while user is signed in and user is ADMIN
        print("\nMenu Options:") #menu title
        for count, items in enumerate(menu_items, start=1):
            output = str(count) + ": " + str(items)
            print(output)
            #outputs menu

        try:
            choice = int(input("Enter your menu choice(must be 1-5): ")) #validates for correct menu choice

        except ValueError:
            print("Invalid Choice. Try again.\n") #if choice is not a number, ensures program continues on error

        if choice == 1:
            display_customers() #if choice 1, displays customer list

        elif choice == 2:
            import_customers() #if choice 2, allows ADMIN to import customer lists

        elif choice == 3:
            export_customers() #if choice 3, allows ADMIN to export customer lists

        elif choice == 4:
            delete_customer() #if choice 4, allows ADMIN to delete customers from the dictionary

        elif choice == 5:
            print(f"Signing out {user}") #if choice 5, signs out user ADMIN, and gives conformation
            signed_in = False #resets global, signed_in
            user = "" #resets global, user
            return #ensures menu return

        else:
            print("\nInvalid Choice. Try again.") #if choice is invalid



print(f"{"\n\nWelcome to Swencak Ski Resort!":^100}") #System Title

while True: #ensures menu_1 continues when users sign out menu_2 or menu_3, until menu_1 is exited
    menu_1() #calls to menu_1 to start the program until menu_1 exits