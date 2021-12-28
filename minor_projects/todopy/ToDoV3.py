'''
ClassToDo.py
Nik Kirstein

This is a todo list shell application that functions using two classes.
One class handles a single todo, it's name, desc, due date, and if it's complete
The other class handles a section which can be made up of many or one todos.
'''

import os
import sys
import platform

'''
#Might use later, leaving for now.  Trying to always print todos for sections
#based on duedate, even if they were added in random order.
def sorting(L):
    splitup = L.split('/')
    return splitup[2], splitup[1], splitup[0]
'''

def sort_todo_list(input_list):
    '''
    Takes a todo_list, a list of todo objects and sorts
    them on the duedate
    '''
    sorted_list = sorted(input_list, key=lambda x: x.duedate, reverse=False)
    return sorted_list

class todo:
    def __init__(self, name, desc, duedate, completetoggle):
        self.name = name
        self.desc = desc
        self.duedate = duedate
        self.completetoggle = completetoggle

    def __repr__(self):
        return (self.name + ": " + self.desc + "\nDue: " + self.duedate +
        "\nCompletion Status: " + str(self.completetoggle) + '---\n')


class section:
    def __init__(self, section_name):
        self.section_name = section_name
        self.todo_list = []

    def __repr__(self):
        print_string = "-" * 20 + self.section_name + "-" * 20 + "\n"
        sorted_todo_list = sort_todo_list(self.todo_list)
        for todo in sorted_todo_list:
            print_string += str(todo) + "\n"
        return print_string

    def add(self, new_todo):
        self.todo_list.append(new_todo)

    def new(self):
        new_todo = todo(input("Insert Name: "), input("Desciption: "), input("Due Date (mm/dd/yy): "), False)
        #we always assume a todo added is False or not complete
        #Why would you add a completed task to a todo list?
        #It's possible it's needed/wanted but we won't handle it for now.
        self.add(new_todo)

    def del_todo(self):
        todo_to_delete = input("Input name of todo item to delete, must be exact")
        found = 0
        for todo in self.todo_list:
            if todo.name == todo_to_delete.name:
                self.todo_list.pop(todo)
                print("Todo list item found, deleting...")
                found = 1
        if found == 0:
            print("Todo item not found, try again")



def main():
    sections = []

    while(True):
        print("Main Menu")
        print("1: New Section | 2. Add todo to existing section | 3. Print todo | 4. Clear screen")
        response = int(input())
        if response == 1:
            new_section = section(input("Input section name: "))
            print("Add first todo (name, desc, duedate)")
            new_section.new()
            print(new_section)
            sections.append(new_section)
        if response == 2:
            #Can we do anything to reduce this to one for loop?
            horizontal_string = ""
            for existing_section in sections:
                horizontal_string += (existing_section.section_name)
            print("Chose Section to add new todo:", horizontal_string + " | ")
            response = input()
            found = 0
            for existing_section in sections:
                if response == existing_section.section_name:
                    print("Section found, add new todo")
                    found = 1
                    existing_section.new()
            if found == 0:
                print("Section not found, try again")
        if response == 3:
            for existing_section in sections:
                print(existing_section)
        if response == 4:
            if platform.system() != 'Windows':
                os.system('clear')
            else:
                os.system('cls')



if __name__ == '__main__':
    main()
