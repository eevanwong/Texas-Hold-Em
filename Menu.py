from Buttons import * 
from FileFunctions import *


class Menu:
    def __init__(self):
        #Each list holds the instances of images, text, buttons that are text and buttons that are images
        self.imgList = []
        self.txtList = []
        self.txtbtns = []
        self.imgbtns = []
        
        self.highscores = []
        self.dict = {}
        self.IA=[]
        self.report = []
        self.players = []
        self.date = (str(year()) + "-" + str(month()) + "-" + str(day()))
        
        #Each function utilizes the specific text file given, and use the file functions that make it usable, then (except for just general images and text) call on the buttons class. 
        #They're then all displayed either using the button function or just text() and image().
    def getimages(self, file):
        self.imglist = readFile(file)
        self.imgList = strtoint(self.imglist)
        numImages = len(self.imgList)
        for i in range(numImages):
            self.imglist[i][0] = loadImage(self.imgList[i][0])
    
    def Text(self, file):
        self.txtList = readFile(file)
        self.txtList = strtoint(self.txtList)
        
    def tbuttons(self,file):
        self.txtbtns = readFile(file)
        self.txtbtns = strtoint(self.txtbtns)
        numtxtBtn = len(self.txtbtns)
        for i in range(numtxtBtn):
            if len(self.txtbtns[i]) == 5: #text size differs, and it is already instantiated. So some instances may have 5 attributes while others have 6
                self.txtbtns[i] = Buttons(self.txtbtns[i][0],self.txtbtns[i][1],self.txtbtns[i][2], self.txtbtns[i][3], self.txtbtns[i][4])
            else:
                self.txtbtns[i] = Buttons(self.txtbtns[i][0],self.txtbtns[i][1],self.txtbtns[i][2], self.txtbtns[i][3],self.txtbtns[i][4],self.txtbtns[i][5])
    
    def imgbuttons(self,file):
        self.imgbtns = readFile(file)
        self.imgbtns = strtoint(self.imgbtns)
        numimgbtns = len(self.imgbtns)
        for i in range(numimgbtns):
            self.imgbtns[i] = ImageButtons(self.imgbtns[i][0], self.imgbtns[i][1], self.imgbtns[i][2], self.imgbtns[i][3], self.imgbtns[i][4])
    

#DATABASE CODE - INVOLVES CURRENTINFO,NEWINFO, and STOREINFO functions
    def currentinfo(self,filename): #initializes, database
        self.dict = readpickle("scores.pickle", {}) #dictionary
        self.IA= readpickle("Indirectarray.pickle", [])
        self.highscores = readpickle("highscores.pickle",[])
        
        if not self.dict: #checks if theres anything inside the dict, if not, then it will look for 'setup.txt'
            try:
                with open(filename,'r') as filecontent:
                    info = filecontent.readlines()
                    for i in info:
                        i = i.split(',')
                        if '\n' in i[4]:
                            i[4] = i[4].strip('\n')
                        i[3] = int(i[3])
                        self.dict[i[0]] = [i[1],i[2],i[3],i[4]] #creating the dictionary from the setup
                        
                        
                        item = [i[0],i[1],i[2],i[3],i[4]]
                        
                        if len(self.highscores) == 0:       #Highscores are inserted into new highscores list
                            self.highscores.insert(0, item)
                        else:
                            index = 0
                            for j in range(len(self.highscores)):
                                if self.highscores[index][3] >= i[3]:
                                    index += 1
                            self.highscores.insert(index, item)
                
                with open('report.txt', 'w') as f: #ALL FILES MUST BE WRITTEN TO IN ONE GO (I.E AFTER YOU PRESS EXIT (Does animation and stuff)) (WHEN FIRST OPENED, REPORT NEEDS TO WRITE DATE AND THE INFO OF 5 PPL FROM SETUP.txt
                    f.write(self.date + '///' + '\n')
                    for i in self.dict:
                        f.write('%s - %s%s: new player added'%(i,self.dict[i][0],self.dict[i][1]) + '\n')
                        
                #!!!!!! 
                NotFound = True
                for i in self.dict:#indirect array
                    for j in range(len(self.IA)):
                        if i ==self.IA[j][1]:
                            NotFound=False#NA means not there
                                
                    if NotFound:
                        Combinedname=self.dict[i][0]+self.dict[i][1]         #checks if name is already in indirect array, if not then it will insert it based on name
                        if len(self.IA)==0:
                            self.IA.insert(0,[Combinedname,i])
                        else:
                            location=0
                            for k in range(len(self.IA)):
                                if self.IA[location][0]<Combinedname:
                                    location += 1
                            self.IA.insert(location,[Combinedname,i])
    
                    NotFound = True
                
                
                for i in range(len(self.IA)):
                    for j in self.dict:
                        Combinedname = self.dict[j][0] + self.dict[j][1]
                        if self.IA[i][0] == Combinedname:
                            self.players.insert(i,[self.dict[j][0] + self.dict[j][1],self.dict[j][2],self.dict[j][3],j])

            except IOError:
                print('CANT RUN GAME, SETUP NOT FOUND')
                exit()
        else:
            with open('report.txt','r') as readFile: #in report file, it will check latest date report was written on
                if self.date in readFile.read(): #if latest date is today, wont do anything,                             
                    pass                         #else, it will insert it into the beginning of list, which will be written to the file later 
                else:
                    with open('report.txt','a') as appendFile:
                        appendFile.write(self.date + '///' + '\n')
                        
            with open('players.txt','r') as playerFile:
                info = playerFile.readlines()
                for i in info:
                    i = i.split(',')
                    if '\n' in i[3]:
                        i[3] = i[3].strip('\n')
                    self.players.append([i[0],i[1],i[2],i[3]])

            
    def newinfo(self, ID, firstname, lastname, score): 
        item = [ID,firstname,lastname,score,self.date]
        
        if len(self.dict) > 0:
            if ID not in self.dict:                           #checks if new player
                self.dict[ID] = [firstname, lastname,score, self.date]
                print('%s - %s%s: new player added'%(item[0],item[1],item[2]))
                self.report.append('%s - %s%s: new player added'%(item[0],item[1],item[2]))
                
            else:
                for i in self.dict:
                    if i == ID and self.dict[i][2] < score:
                        self.dict[ID] = [firstname, lastname, score,self.date] #will overwrite the original key
                        print('%s - %s%s: new highscore'%(i,self.dict[i][0],self.dict[i][1]))
                        self.report.append('%s - %s%s: new highscore (%s)'%(i,self.dict[i][0],self.dict[i][1],self.dict[i][2]))
                        
                    elif i == ID and self.dict[i][3] != self.date:   #checks if score is higher, if so that players score will be updated (along with date)
                        self.dict[i][3] = self.date
                        print('%s - %s%s: played again'%(i,self.dict[i][0],self.dict[i][1]))
                        self.report.append('%s - %s%s: played again'%(i,self.dict[i][0],self.dict[i][1]))
            
        NotFound = True
        index = 0     
        higherscore = True
                            #inserts new score, if number of scores exceeds 8, will pop last item in list

        for i in range(len(self.highscores)): #needs to insert higher score... also needs to make sure that, if its the same player, it will need to update that player's score 
            if self.highscores[i][0] == item[0]:
                if self.highscores[i][3] <= item[3]:
                    self.highscores.pop(i)          #removes the old entry if new entry of same player has greater score, it then finds new location based on new score
                else:
                    self.highscores[i][4] = item[4] #updates date
                    higherscore = False
                    
                for j in range(len(self.highscores)):
                    if self.highscores[index][3] >= item[3]:
                        index += 1 
                
                NotFound = False    
                break
                            
        if NotFound:
            for i in range(len(self.highscores)):
                if self.highscores[index][3] >= item[3]:
                    index += 1
        
        if higherscore:
            self.highscores.insert(index, item)    #if higherscore is found, then it will insert, else it will just pass the score
        elif index == 8:
            pass 

        NotFound = True
        Combinedname = firstname + lastname
        for i in range(len(self.IA)):
            if firstname + lastname == self.IA[i][0]:
                NotFound = False                             #if found, it will update the information for the particular player in self.players if the score is greater
                for j in self.players:
                    print(self.IA[i][0], j[0])
                    if self.IA[i][0] == j[0]:                        
                        if j[1] <= score:
                            j[1] = score
                        j[2] = self.date
        
        if NotFound:
            location = 0
            for i in range(len(self.IA)):
                if self.IA[location][0] <= Combinedname:
                    location += 1
            self.IA.insert(location,[Combinedname,ID])
            self.players.insert(location,[Combinedname, self.dict[ID][2],self.dict[ID][3],ID]) #inserts information along with indirect array

        #print(self.IA)
        
    def storeinfo(self):
        
        with open("scores.pickle",'w+b') as scoreFile:          #when quitting, all information is put into the files
            pickle.dump(self.dict, scoreFile)
    
        with open('highscores.pickle','w+b') as openFile:
            pickle.dump(self.highscores,openFile)
            
        with open('report.txt', 'a') as reportFile:
            for i in self.report:
                reportFile.write('%s'%i + '\n')
        
        with open('players.txt','w') as playerFile:
            for i in self.players:
                playerFile.write('%s,%s,%s,%s'%(i[0],i[1],i[2],i[3]) + '\n') #combined name, score, date, student ID
                
        with open("Indirectarray.pickle", 'w+b') as openFile:
            pickle.dump(self.IA, openFile)
            
    def display(self):
        for img in self.imgList:
            imageMode(CENTER)
            tint(255)
            image(img[0], img[1], img[2])
        
        for txt in self.txtList:
            textAlign(CENTER,CENTER)
            textMode(CENTER)
            textSize(txt[3])
            fill(255)
            text(txt[0],txt[1],txt[2])
            
        for btn in self.txtbtns:
            btn.display()
        
        for imgbtn in self.imgbtns:
            imgbtn.displaybutton()

        for pos in range(len(self.highscores)):
            textAlign(CENTER,CENTER)
            textMode(CENTER)
            textSize(25)
            fill(255)
            text(self.highscores[pos][0], 199, 157 + pos * 65)
            text(self.highscores[pos][1], 345, 157 + pos * 65)
            text(self.highscores[pos][2], 445, 157 + pos * 65)
            text(self.highscores[pos][3], 599, 157 + pos * 65)
            text(self.highscores[pos][4], 800, 157 + pos * 65)
        
        
            
            
