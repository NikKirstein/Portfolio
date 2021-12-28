'''
listToDo.py
Nik Kirstein

This is a todo list tracking program that uses reading and writing files
as well as populating a dictionary from reading a file as it's main form
of tracking todos.  There is no GUI and no completion indicator of todos.

It's simply a todo list generator and modifier.

'''

#Potential changes:
#Detect the operating system so we know which version of shell clearing to use
#"clear" or "cls"
#Automatically clear the screen before displaying new information like before
#displaying the todo list or the menus for maximum shell space.  Remove
#the ability to do that manually or just simply add both.

import os
#Uses os to call command line commands so we can clear terminals

def create_todo_txt(file_name):
    '''
    file_name is the name of the file to be opened and given a blank string
    I dont know if a blank string is actually proper but it seemed logical

    returns nothing. Used in main
    '''
    with open(file_name, "w") as f:
        f.write("")


def read_and_populate_dictionary(file_name, in_dict):
    '''
    Opens a file_name and reads it line by line and parses it according
    to a specific scheme

    In this case, Lines that begin with | are section headers, and once found
    the section is put into a dictionary as a key and given a blank list
    as a value, to be populated when we parse the next lines

    Because we assume the next lines after | are going to be it's todos that
    start with "-", we don't check for sure, we just treat it as such.

    Returns nothing, reads a file into a dictionary basically
    '''
    f = open(file_name, "r")
    #Skip first line
    f.readline()
    for line in f:
        #print("LINE: ", line)
        if line[0] == "|":
            #print("FOUND |: ", line)
            newline = line.replace("-", "")
            newline = newline.split("|")
            in_dict[newline[1]] = []
        elif line[0] != "|" and line[0] != "-":
            #print("FOUND -: ", line)
            in_dict[newline[1]].append((line.replace("\n", "")).split(":")[1])
            '''
            Failed attempt at the above line
            while(line[0] != "|"):
                print("while loop firing")
                in_dict[newline[1]].append(line)
                print("key", newline[1], "value", line)
                line = f.readline()
            '''


def write_and_save(file_name, in_dict):
    '''
    Generates a string to overwrite a file.  Using the dictionary (in_dict) created
    in read_and_populate_dictionary, we write out todo list from scratch
    and write it out to file_name.

    Returns nothing
    '''
    #"THE PYTHON LIST-TO-DO" is 21 characters long
    #total characters is 21 + 21 + 22 = 64 not counting the newline
    write_string = ("-"* 21+ "THE PYTHON LIST-TO-DO" + "-"*22 + "\n")
    with open(file_name, "w") as f:
        for key, value in in_dict.items():
            dash_fill = (64 - len(str(key))) // 2
            write_string += ("|" + "-"*dash_fill + str(key) + "-"*dash_fill + "|\n")
            for i, list_item in enumerate(value, 1):
                write_string += str(i) + ":" + str(list_item) + "\n"
        f.write(write_string)


def add_section(in_dict):
    '''
    Gets a new section name from a user and adds it to the dictionary
    used for tracking sections and todo.  in_dict is the dictionary of
    sections and todos that we are tracking.  We use a while True loop and checking for empty input to get multi line user input

    Returns nothing
    '''
    response = input("Enter Section Name\n")
    in_dict[response] = []
    print("Insert list items. Enter a blank line to end")
    while(True):
        line = input()
        if line != "":
            in_dict[response].append(line)
        elif line == "":
            break
    #print(in_dict)


def edit_section(in_dict):
    '''
    Displays all the sections in the dictionary in_dict in one
    string on one line. Asks input from the user on which section to edit.
    If the section exists, we basically wipe it's todos and ask for
    new ones, it's a command line program so editing in real time as if its
    a text editor doesn't seem feasible.  Haven't tried though.

    returns nothing
    '''
    horizontal_dispay = ""
    for key in in_dict:
        horizontal_dispay += key + ", "
    print("SECTIONS: "+ horizontal_dispay)
    to_edit = input("Enter section name to edit\n")
    if to_edit in in_dict:
        print("Section found, Now Editing: ")
        in_dict[to_edit] = []
        while(True):
            line = input()
            if line != "":
                in_dict[to_edit].append(line)
            elif line == "":
                break
    else:
        print("section not found, try again")
        return


def del_section(in_dict):
    '''
    Displays the sections (keys) from in_dict, the dictionary that tracks
    all the sections and todos, and asks the user which one they want to delete.

    Does a final call and if so, pops the section out and does nothing with it.
    Effectivly tossing it.  If no section can be found based on user input
    it asks again.

    returns nothing
    '''
    horizontal_dispay = ""
    for key in in_dict:
        horizontal_dispay += key + ", "
    print("SECTIONS: "+ horizontal_dispay)
    to_delete = input("Enter section name to delete\n")
    if to_delete in in_dict:
        final_call = (input("Section found, now deleting, are you sure you want to do this? Y/N\n")).upper()
        if final_call == "Y":
            in_dict.pop(to_delete, None)
        elif final_call == "N":
            print("Returning to Menu")
            return
    else:
        print("Section not found, try again")
        return


def edit_menu(file_name, in_dict):
    '''
    The edit menu for the todo list branching off the main menu.
    1. Add section, 2. Edit section 3. Delete section 4. Back

    Calls the add, edit, and del functions for each of these as well as
    write_and_save after each one.  This function uses file_name and the
    todo tracking dictionary in_dict in order to call the other functions.

    returns nothing
    '''
    print("1.Add section\n2.Edit section\n3.Delete section\n4.Back")
    response = input()
    if response == "1":
        add_section(in_dict)
        write_and_save(file_name, in_dict)
    elif response == "2":
        edit_section(in_dict)
        write_and_save(file_name, in_dict)
    elif response == "3":
        del_section(in_dict)
        write_and_save(file_name, in_dict)
    elif response == "4":
        return
    else:
        print("Please enter a number 1-4")


def main():
    '''
    Makes a file_name and an empty dictionary.

    If the file does not exist, we create one if the user wants to
    if not, we exit.

    If a list does exist, we read the file and populate the todo list dictionary
    Afterwards, we display a menu giving the ability to display the file in
    the shell, as well as edit it. There is an option to clear the terminal
    screen because I found it nice and a debug option to simply print
    the totatility of the todo list dictionary.

    returns nothing
    '''
    todo_file_name = "todoList.txt"
    todo_dictionary = {}

    if not os.path.exists(todo_file_name):
        response = (input("No existing todo file found, would you like to create one now? Y/NDOCUMENTATION\n").lower())
        if response == "y":
            create_todo_txt(todo_file_name)
        elif response == "n":
            print(":c I don't blame you\nGoodbye")
            return
        else:
            print("Please enter Y/N")


    print("\nToDo list file found!")
    read_and_populate_dictionary(todo_file_name, todo_dictionary)
    #print_dictionary(todo_dictionary)
    while(True):
        response = input("What would you like to do? (Pick a number)\n1.Display ToDo\n2.Edit ToDo\n3.Clear Screen\n4.Exit\n")
        if response == "1":
            with open(todo_file_name, "r") as f:
                print(f.read())
        elif response == "2":
            edit_menu(todo_file_name, todo_dictionary)
        elif response == "3":
            os.system('clear')
            #os.system('cls')
        '''
        #Debug option
        elif response == "3.5":
            for key in todo_dictionary:
                print("Key: ", key, "| Value: ", todo_dictionary[key])
        '''
        elif response == "4":
            print("Exiting\nGoodbye!")
            return
        else:
            print("Not an option, please pick a number between 1-4")


if __name__ == '__main__':
    main()
