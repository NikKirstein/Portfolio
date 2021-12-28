'''
THIS IS FULLY FUNCTIONAL

but the way I did read_and_return
is hacky and probably not ideal since I'm literally making a list and then deleting duplicates
not the best way at all

But it works c:
'''
'''

TO DO FOR THE TO DO

Write now if you input a , anywhere, because thats what it splits on, the program will break.
To get around this I need to split on something new which will also make my read_and_return function not suck

This is by instead of writing from big string to the file all at once,
we write line by line
each line is a entry in in the to-do list
line 0 is first tasks name
line 1 is first tasks due date
line 2 is first tasks description
line 3 is second tasks name
and so on.
no longer need to split on the , for this to work but its still using the 0 to 3 method.
'''


ToDoList = []

ExtraNotes = {}



def main():
    '''
    Does the main stuff
    '''
    read_and_return()
    while(True):
        response = input('\nWhat would you like to do?\nType help for commands (case doesn\'t matter)\nType quit to quit (list saves upon quitting): ')
        if response == 'quit':
            Save()
            break
        else: 
            what_are_we_doing((response.lower()))

        
    
def read_and_return():
    file = open('ToDoList.txt', 'r')
    temp_list = []
    filler_list = []
    another_temp_list = []
    total_string = ''
    for line in file:
        total_string += line
        
    temp_list = total_string.split(',')
    temp_list = filter(None, temp_list)
    temp_list = list(temp_list)
    
    counter = 0
    stepper = 3
    
    End_point = len(temp_list)
    
    while(stepper < End_point):
        for i in range(counter, stepper):

            filler_list.append(temp_list[i])
            
        counter+=3 
        stepper +=3
        another_temp_list.append(filler_list)   
        filler_list = []
    
    for i in another_temp_list:
        if i not in ToDoList:
            ToDoList.append(i)
        
                
    
def Save():
    stringywrite = ''
    file_write = open('ToDoList.txt', 'w')
    for i in range(len(ToDoList)):
        for k in range(len(ToDoList)):
            stringywrite += ToDoList[i][0] + ','
            stringywrite += ToDoList[i][1] + ','
            stringywrite += ToDoList[i][2] + ','
    file_write.write(stringywrite)
    file_write.close()

def help():
    '''
    Displays all commands
    '''
    result = ( 
    '------------------------------\n'
    '\nDisplay: Displays the to-do list\n' +
    'Add: Triggers a prompt to add a task to the to-do list\n' +
    'Del: Triggers a prompt for a task name and will delete the task given\n' +
    'Help: Displays this useful message about things to type\n' + 
    '--------------------------------------\n')
    return print(result)

def addToDo():
    '''
    name is the name of the task
    dueDate is the due date of the task
    description is obviously, the description of the task
    '''
    ToDoSpecific = []
    name = input('Insert task name: ')
    dueDate = input('Insert Due Date: ')
    description = input('Insert Description of task: ')
    ToDoSpecific.append(name)
    ToDoSpecific.append(dueDate)
    ToDoSpecific.append(description)
    ToDoList.append(ToDoSpecific)
    
    return
    
    
def Del():
    to_delete = input('Insert name of task to delete: ')
    for i in range(len(ToDoList)):
            if ToDoList[i][0] == to_delete:
                del ToDoList[i]
    
def Display():
    result = '\n-----------------------------\n'
    for i in range(len(ToDoList)):
        result += '* ' + ToDoList[i][0] + '\n'
        result += 'Due Date: ' + ToDoList[i][1] + '\n'
        result += 'Desc: ' + ToDoList[i][2] + '\n'
        result += '-----------------------------\n'
    return print(result)
    
    
def what_are_we_doing(input):
    if input == 'display':
        Display()
        return
    if input == 'add':
        addToDo()
        return
    if input == 'del':
        Del()
        return
    if input == 'help':
        help()
        return
    else:
        print('Unknown command, try again.')
        return
    
    
    
main()
    
'''

Potential Design details.

So far the current method is a list of lists with each inner list comprised of three things so each inner list will be/has to be in the same format.
[['Eat Food', 'Due: 2/3/18', 'Eat a healthy Dinner!'], ['Do Laundry', 'Due: 3/5/15', 'Use soap and do your laundry!']]
etc etc etc.

An alternative solution is to map each task to a dictionary of things 

{Task1: {Name: 'Eat Food', Due: '2/3/18', Desc: 'Eat a healthy dinner!'}, Task2: {Name: 'Do Laundry', Due: '2/3/15', Desc: 'wishy washy'}}

Which is better?
The dictionary one seems more complicated honestly but I can get tasks simply by their intial key.

TBD
'''






































    