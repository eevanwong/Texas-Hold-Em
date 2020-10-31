import pickle
import os
def readFile(file):
    data = []
    f = open(file)
    textData = f.readlines()
    for i in textData:
        i = i.split(";") # Splits with ; because i use commas in the help menus
        data.append(i)
    f.close()
    return (data) #returns items in a list


def strtoint(List):
    for i in range(len(List)):
        for j in range(len(List[i])):
            if "\n" in List[i][j]: # strips because it caused complications in the display of buttons
                List[i][j] = List[i][j].strip("\n")
            try:
                List[i][j] = int(List[i][j])    #Makes all values int, but if it contains string characters, then it will pass it
            except ValueError:
                pass
    return(List) #Returns list with all num turned into int, and and keeps the strings

def readpickle(file, struct): #recieves file name and what type of array it is 
    try:
        with open(file, 'r+b') as openFile: #first checks if it exists, if not, except statement will create the pickled file
            info = pickle.load(openFile)
    except EOFError:
        with open(file, 'w+b') as openFile:
            info = struct
    except IOError:
        with open(file, 'w+b') as openFile:
            info = struct
    print(info)
    return(info)



   
