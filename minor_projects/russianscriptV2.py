'''
Script written by: 
Date 4/22/16


Description: Reads a CSV file of organized data and outputs number of time occurances happen and where they come from.

To use this script:

1. File to be read must a .csv file.  Python can read excel files but not without extra libraries that much be downloaded.  Save all excel files (.xls) as csv files and then it can be read.

2. Script works best if you toss out anything that isn't data to be read.  Move all ICLE-CN-UK-0 to column A and all the words to count and locate to column B.
The excel file given had "page 32 of 32" at the bottom of it, if manually removed by deleting it in the spreadsheet, run the script as is.  
If it is not removed, uncomment the line of code that looks like this: #Total_list.pop(-1) by deleting the # and the script will delete it for you.

3. Python must be installed to run python scripts.  Open a command window/powershell/terminal in the same directory as the script and data file to be read.
Once the command window/terminal is open, type the following:
python russianscript.py

4. In the command window will be a prompt to enter the name of the input file to be read (which should be the .csv file)
It will be followed by a prompt to name the output file generated after the script is ran.  
It can have any name as long as .txt is added to the end of the name to specifiy the file type

5. The file with the name specified should now exist in the same directory as the script.  

'''

import csv
import operator

inputfilename = input('Enter name of input file to be read (Should be a csv): ')
outputfilename = input('Enter name of output file (Outputs a .txt file): ')


Total_list = []  #A list with all data in it.  


#Loading entire contents from file into a list.  List is formatted like [Location, word phrase, location, word phrase]
file = open((inputfilename + '.csv') , 'r')
for line in file:
        line = line.strip().split(',')
        Total_list += line
    
string_placement_hold = Total_list[0]    

#filtering out unwanted data such as blank data, and footers of dataset.    
Total_list = filter(None, Total_list)    #Turns list into filter object after it filters it
Total_list = list(Total_list) #Turning filter object back into list
#if "page 32 x 32" is present on bottom of document, uncomment the line below by deleting the #
Total_list.pop(-1)

#Generating a list of unique words to search a list generated that is filled with all words
comparelist = [] 
list_filled_with_words = []
for i in range(1, len(Total_list), 2):
    list_filled_with_words.append(Total_list[i])
 
#making all items in list lowercase, generating a non lowercase list later for location comparison
list_filled_with_words = [x.lower() for x in list_filled_with_words]
 
#Generating compare list
for i in list_filled_with_words:
  if i not in comparelist:
    comparelist.append(i)
        
    
#Counting number of times it appears, Could have used Counter here but I found it unreliable so I wrote my own.
counter = 0
Count_Dictionary = {}
for unique in comparelist:
    for word in list_filled_with_words:
        if unique == word:
            counter += 1
    Count_Dictionary[unique] = counter
    counter = 0
    

#print(Count_Dictionary)

#Dictionary filled with words and reoccuring number of occurance now exists.  Will not use until programming written for finding locations is complete
        
#generating a dictionary of words as keys and where they appear as a list for values        
Location_Dictionary = {}
value_list = [] #value list is filled with locations, put into a dictionary and then wiped to be used again.

for unique in comparelist:
    for i in range(len(Total_list)):
        if Total_list[i].lower() == unique:#compare lowercased
            value_list.append(Total_list[(i-1)])
    Location_Dictionary[unique] = value_list
    value_list = []

#Must now remove the duplicates from the dictionary value lists
for key, value in Location_Dictionary.items():
    Location_Dictionary[key] = list(set(Location_Dictionary[key]))
      
      
      
#Getting range
'''
This will fail if the length of the string it's searching is less than this:
len(ICLE-CN-UK-0003.1)
16

It gets the min and max value by negative index to get the end number from the string and compare it.
'''
Range_Dictionary = {}
Fill_list = []
max_num = 0
min_num = 0
for key, location in Location_Dictionary.items():
    for i in range(len(location)): #Should be looking at the len of a list within the dictionary.  
        Fill_list.append(float(location[i][-6:]))
    max_num = max(Fill_list)
    min_num = min(Fill_list)
    Range_Dictionary[key] = (str(min_num) + ':' + str(max_num))
    max_num = 0
    min_num = 0
    Fill_list = []



sorted_c_dict = sorted(Count_Dictionary.items(), key=operator.itemgetter(1), reverse=True)

#writing an output file for locations and auxillery file for ordered.

         
string_writer = ''


for word, amount in Count_Dictionary.items():
    string_writer += ('--------------------------------------\n')
    string_writer += ( word + 'has occurred ' + str(amount) + ' time(s) and in these locations:\n')

    for key, location in Location_Dictionary.items():
        if key == word:
            string_writer += (', '.join(Location_Dictionary[word])) 
            string_writer += ('\nMinimum ID: ICLE'+ string_placement_hold[4:11] + ((str(Range_Dictionary[word].split(':')[0])).zfill(6)) + ' || Maximum ID: ICLE'+ string_placement_hold[4:11] + ((str(Range_Dictionary[word].split(':')[1]))).zfill(6))
            #Worlds longest line of code
    string_writer += ('\n--------------------------------------')

   
'''
#Will I ever get this working properly.... ????????????

for record in sorted_c_dict:
    string_writer += ('--------------------------------------\n')
    string_writer += ( record[0] + 'has occurred ' + str(record[1]) + ' time(s) and in these locations:\n')
  
    for key, location in Location_Dictionary.items():
        if record[0] == key:
            string_writer += (', '.join(Location_Dictionary[(record[0])])) 
            string_writer += ('\nMinimum ID: ICLE'+ string_placement_hold[4:11] + ((str(Range_Dictionary[record[0]].split(':')[0])).zfill(6)) + ' || Maximum ID: ICLE'+ string_placement_hold[4:11] + ((str(Range_Dictionary[record[0]].split(':')[1]))).zfill(6))
            #Worlds longest line of code
    string_writer += ('\n--------------------------------------')
'''  
    
    
string_writer2  = ''
for record in sorted_c_dict:
    string_writer2 += ( record[0] + 'has occurred ' + str(record[1]) + ' time(s)\n')
    
  
  
fileaux = open((outputfilename + '_occurances.txt'), "w")
fileaux.write(string_writer2)
fileaux.close()
  
text_file = open((outputfilename + '_locations.txt'), "w")  
text_file.write(string_writer)
text_file.close()









   
    