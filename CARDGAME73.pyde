from Menu import *
from Buttons import *
from Game import *
from Player import *
from Key import Keys

def setup():
    global modelist, helplist, currentMode, highscores, font
    global infoInput 
    global game, prevmode
    global rectx, recty, rectx2,recty2, incrx, incry
    global stuNum, firstName, lastName, keyList
    global playerindex, playagain
    size(900,650)
    font = createFont("Qanelas-Black.otf", 50, True)
    score = 0
    infoInput = False
    rectx = 100
    recty = 100
    rectx2 = 250
    recty2 = 200
    incrx = 5
    incry = 5
   #Via the Menu class, each function reads a file through the readfile function in FileFunctions and each one is an instance that is continuously loaded. 
    main = Menu()
    main.getimages("MainMenuImg.txt")
    main.tbuttons("MainButtons.txt")
    buttonlist = main.txtbtns
    buttonlist[0].action = toplay
    buttonlist[1].action = h2back     #currentmode = helplist[0]
    buttonlist[2].action = toscore
    buttonlist[3].action = Exit
    
    play = Menu()
    play.getimages("PlayMenuImg.txt")
    play.tbuttons("PlayButtons.txt")
    buttonlist = play.txtbtns #fold,check,raise index 5,6,7
    buttonlist[0].action = tomenu
    buttonlist[2].action = h2back
    buttonlist[3].action = toscore
    buttonlist[4].action = Exit
    buttonlist[5].action = fold                 #buttons for game setup
    buttonlist[6].action = checkorcall
    buttonlist[7].action = showbuttons #raise button
    buttonlist[8].action = Raise500
    buttonlist[9].action = Raise1000
    buttonlist[10].action = Raise2000
    
    buttonlist[8].showbutton = False
    buttonlist[9].showbutton = False
    buttonlist[10].showbutton = False
    
    nameinterface = Menu()
    nameinterface.getimages("NameImg.txt")
    nameinterface.Text("NameText.txt")
    nameinterface.tbuttons("NameButtons.txt")

    buttonlist = nameinterface.txtbtns
    buttonlist[0].action = back
    buttonlist[1].action = stuNumButton
    buttonlist[2].action = firstNameButton
    buttonlist[3].action = lastNameButton
    buttonlist[4].action = confirmAction
    playagain = Menu()
    playagain.tbuttons("playagainButtons.txt")
    playagain.Text("playagainText.txt")
    buttonlist = playagain.txtbtns
    buttonlist[0].action = playAgain
    buttonlist[1].action = newGame
    buttonlist[2].action = Exit
    
    scores = Menu()
    scores.getimages("ScoreImg.txt")
    scores.tbuttons("BackButton.txt")
    scores.Text("ScoreText.txt")
    
    buttonlist= scores.txtbtns
    buttonlist[0].action = back
    
    highscores = Menu() #Not apart of mode list
    highscores.currentinfo("setup.txt") #calls database, initializes it
    
    
    h1 = Menu()
    h1.Text("RulesText1.txt")
    h1.tbuttons("BackButton.txt")
    h1.imgbuttons("RulesImgBtn1.txt")
    
    buttonlist = h1.txtbtns
    buttonlist[0].action = back #help menu 1 and the buttons setup
    
    buttonlist = h1.imgbtns
    buttonlist[0].action = h1next

    
    h2 = Menu()
    h2.Text("RulesText2.txt")
    h2.imgbuttons("RulesImgBtn2.txt")

    buttonlist = h2.imgbtns            #buttonlist represents specific buttons in the help menu, vary dependingon

    buttonlist[0].action = h2next   
    buttonlist[1].action = h2back 
    
    h3 = Menu()
    h3.Text("RulesText3.txt")
    h3.imgbuttons("RulesImgBtn3.txt")

    buttonlist = h3.imgbtns
    buttonlist[0].action = h3next  
    buttonlist[1].action = h3back   
    
    
    h4 = Menu()
    h4.getimages("RulesImg4.txt")
    h4.imgbuttons("RulesImgBtn4.txt")
    
    buttonlist = h4.imgbtns
    buttonlist[0].action = h4back   

    quit = Menu()

    
    modelist = [main, nameinterface, play, scores, quit, playagain]
    helplist = [h1, h2, h3, h4]
    currentMode = modelist[0]
    prevmode = modelist[0]
    game = Game()
    
    game.addplayer(Player(175,400))
    game.addplayer(Player(575,135))

    playerindex = 0
    
    keyList = []
    stuNum = Keys() 
    stuNum.x,stuNum.y = 450,240
    stuNum.acceptedchars = "1234567890"
    stuNum.minlen = 6
    stuNum.maxlen = 6
    stuNum.enteraction = stuNumEnter
    
    firstName = Keys()
    firstName.x, firstName.y = 450,340    
    firstName.acceptedchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    firstName.minlen = 2
    firstName.maxlen = 10
    firstName.enteraction = firstNameEnter
    
    lastName = Keys()
    lastName.x, lastName.y = 450, 440
    lastName.acceptedchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lastName.minlen = 2
    lastName.maxlen = 10
    lastName.enteraction = lastNameEnter
    keyList.extend([stuNum, firstName, lastName])

    
def draw():
    global currentMode, modelist, H1, H2, H3, H4 
    global game 
    global prevmode
    global rectx, recty, rectx2,recty2, incrx, incry

    background(0)
    currentMode.display()

    if currentMode == modelist[0]:
        prevmode = modelist[0]
        
    if currentMode == modelist[1]: 
        for i in keyList:
            i.display()
        
    if currentMode == modelist[2]:
        prevmode = modelist[2]
        game.display()
        if game.finish:
            currentMode = modelist[5]
    
    if currentMode == modelist[3]:
        highscores.display()
        
    elif currentMode == modelist[5]:
        textSize(35)

        if game.scenario == 3: #displays different things depending on if one player wins or if its a tie
            text("TIE (tied in both card combo and high card)",450,150) 
        else:
            text(game.playerlist[game.currentplayer].name + " WON",450,80)
    
        y = 155
        for i in game.playerlist:
            text(i.firstname + ' ' +i.lastname + "'s Score: " + str(i.money), 450,y) 
            y += 50
        if game.finish:    
            for i in game.playerlist:
                highscores.newinfo(i.stuID, i.firstname, i.lastname, i.money)
            game.finish = False
        
    elif currentMode == modelist[4]:
        #COLLISION ANIMATION (Note, I made only one moving so I could show that it could collide at all sides)
        if 0 >= rectx or rectx + game.cardw >= width:
            incrx = -incrx
      
        if 0 >= recty or recty + game.cardh >=  height:
            incry = -incry
        
        if rectx + game.cardw + incrx > rectx2 and rectx + incrx < rectx2 + 400 and recty + game.cardh > recty2 and recty < recty2 + 290:
            incrx = -incrx 
            
        if recty + game.cardh + incry > recty2 and recty + incry < recty2 + 290 and rectx + game.cardw > rectx2 and rectx < rectx2 + 400:
            incry = -incry
            
                                
        rectx += incrx
        recty += incry
        
        copy(game.cards, 4*game.cardw, 1* game.cardh, game.cardw, game.cardh, rectx, recty, game.cardw, game.cardh)
        stroke(255)
        textSize(28)
        text('HOPE YOU ENJOYED PLAYING',450,300)
        text(':D',450,350)
        noFill()
        rectMode(CORNER)
        rect(rectx2,recty2,400,290) 
        if millis() >= delayTime:
            exit()

def mousePressed():
    global currentMode

    for i in currentMode.txtbtns:
        if i.hitbox:
            i.hitbox = False
            i.action()
    for i in currentMode.imgbtns:
        if i.hitbox:
            i.hitbox = False
            i.action()           

    
#for name, I utilized keyTyped and a Name class to load the text and input the name, P2name, ID, score, and date of the player
def keyTyped(): #Do I put this in menu tab? 
    if key == ENTER and currentMode == modelist[1]:
        confirmAction()
    for i in keyList:
        i.update(key)
    

#SPECIFIC ACTIONS FOR EACH BUTTON AND ENTER
#!!!!!!!!!!!!!!!!!!!ADDON BUTTONS, CLICK ON THE SPECIFIC AREAS TO INPUT ID,NAME
def stuNumButton(): 
    stuNum.enabled = True
    firstName.enabled = False
    lastName.enabled = False

def firstNameButton():
    stuNum.enabled = False
    firstName.enabled = True
    lastName.enabled = False

def lastNameButton():
    stuNum.enabled = False
    firstName.enabled = False
    lastName.enabled = True
    
def stuNumEnter():
    stuNum.enabled = False
    if keyList[0].info in highscores.dict:
        keyList[1].info = highscores.dict[keyList[0].info][0]
        keyList[2].info = highscores.dict[keyList[0].info][1]
    else:
        firstName.enabled = True
    
def firstNameEnter():             #CHECKS THROUGH BINARY SEARCH IF FIRST AND LAST NAME EXISTS
    firstName.enabled = False
    if not highscores.dict:    
        if len(keyList[1].info)!=0 and len(keyList[2].info)!=0:#string
            name=keyList[1].info+keyList[2].info
            first=0
            last=len(highscores.IA)-1
            Middle=(first+last)//2
            while name!=highscores.IA[Middle][0]and first<=last:
                if highscores.IA[Middle][0]>name:
                    last=Middle-1
                else:
                    first=Middle+1
                Middle=(first+last)//2
            if name==highscores.IA[Middle][0]:
                keyList[0].info=highscores.IA[Middle][1]
            
    lastName.enabled = True
def lastNameEnter():
    lastName.enabled = False
    if not highscores.dict:    
        if len(keyList[1].info)!=0 and len(keyList[2].info)!=0:#string
            name=keyList[1].info+keyList[2].info
            first=0
            last=len(highscores.IA)-1
            Middle=(first+last)//2
            while name!=highscores.IA[Middle][0]and first<=last:
                if highscores.IA[Middle][0]>name:
                    last=Middle-1
                else:
                    first=Middle+1
                Middle=(first+last)//2
            if name==highscores.IA[Middle][0]:
                print(highscores.IA[Middle][0])
                keyList[0].info=highscores.IA[Middle][1]
    stuNum.enabled = True
def confirmAction():
    global currentMode, playerindex, infoInput
    if len(keyList[0].info) == 6 and len(keyList[1].info) >= 2 and len(keyList[2].info) >= 2:                  #After entering info, will move on to next player
        lastNameEnter()
        game.playerlist[playerindex].stuID = keyList[0].info
        game.playerlist[playerindex].firstname = keyList[1].info
        game.playerlist[playerindex].lastname = keyList[2].info
        keyList[0].info = ''                    #resets keycapture 
        keyList[1].info = ''
        keyList[2].info = ''
        game.playerlist[playerindex].name = game.playerlist[playerindex].firstname + game.playerlist[playerindex].lastname
        game.playerlist[playerindex].initials = game.playerlist[playerindex].firstname[0] + game.playerlist[playerindex].lastname[0]
        playerindex += 1
        lastName.enabled = False
        firstName.enabled = False
        stuNum.enabled = True
        currentMode.txtList[0][0] = "Second Player's Student ID"
        currentMode.txtList[1][0] = "Second Player's First Name"
        currentMode.txtList[2][0] = "Second Player's Last Name"
        
        if playerindex > 1:
            game.resetgame()
            currentMode = modelist[2]
            keyList[0].info = ''                    
            keyList[1].info = ''
            keyList[2].info = ''
            infoInput = True
        
    
def back(): #to previous mode (either menu or play)
    global currentMode
    currentMode = prevmode

def tomenu(): #to menu 
    global currentMode 
    currentMode = modelist[0]

def toplay():
    global currentMode
    global infoInput
    if not(infoInput): #If they're true 
        currentMode = modelist[1]
        stuNum.enabled = True
    else:
        game.resetgame()
        currentMode = modelist[2]

def toscore():
    global currentMode 
    currentMode = modelist[3] #to score menu
            
def h1next():
    global currentMode
    currentMode = helplist[1] #to help pg 2 menu
    
def h2next():
    global currentMode         #to help pg 3 menu
    currentMode = helplist[2]
    
def h3next():
    global currentMode          #to help pg 4 menu
    currentMode = helplist[3]
    
def h2back():
    global currentMode        #to help pg 1 menu
    currentMode = helplist[0] 
    
def h3back():                  
    global currentMode            #to help pg 2 menu
    currentMode = helplist[1] 
    
def h4back():                   #to help pg 3 menu
    global currentMode
    currentMode = helplist[2] 
    
def Exit():
    global delayTime, currentMode
    delayTime = millis() + 10000
    highscores.storeinfo()
    currentMode = modelist[4]

#########FUNCTIONS TO RESET GAME

def playAgain():          #if both players want to play again
    global currentMode
    canPlay = True 
    for i in game.playerlist:
        i.money = 20000
        i.hand = []
    game.resetgame()
    currentMode = modelist[2]

def newGame():
    global currentMode, infoInput, playerindex
    for i in game.playerlist:
        i.resetPlayer()
    playerindex = 0
    infoInput = False
    currentMode = modelist[0]
    modelist[1].txtList[0][0] = "First Player's Student ID"
    modelist[1].txtList[1][0] = "First Player's First Name"
    modelist[1].txtList[2][0] = "First Player's Last Name"
    
    #need to reset key capture for different players
    
    #function to reset 
    
def hidebuttons():
    currentMode.txtbtns[8].showbutton = False
    currentMode.txtbtns[9].showbutton = False          #if raise button isnt clicked on, they buttons to bet will not show
    currentMode.txtbtns[10].showbutton = False
    
def showbuttons():
    if game.prevpot != 0:
        currentMode.txtbtns[8].t = '%s'%(500+game.prevpot)
        currentMode.txtbtns[9].t = '%s'%(1000+game.prevpot)
        currentMode.txtbtns[10].t = '%s'%(2000+game.prevpot)
    else:
        currentMode.txtbtns[8].t = '500'
        currentMode.txtbtns[9].t = '1000'
        currentMode.txtbtns[10].t = '2000'
    currentMode.txtbtns[8].showbutton = True
    currentMode.txtbtns[9].showbutton = True
    currentMode.txtbtns[10].showbutton= True
    

def Raise500():
    game.prevpot += int(currentMode.txtbtns[8].t)
    print(game.prevpot)
    game.playerlist[game.currentplayer].money -= int(currentMode.txtbtns[8].t) #Raise 500 
    game.pot += int(currentMode.txtbtns[8].t)
    game.currentplayer += 1
    hidebuttons()
    currentMode.txtbtns[6].t = 'Call'
    
    if game.currentplayer == 2:
        currentMode.txtbtns[6].t = 'Check'

    
def Raise1000():
    game.prevpot += int(currentMode.txtbtns[9].t)
    game.playerlist[game.currentplayer].money -= int(currentMode.txtbtns[9].t) #Raise 1000
    game.pot += int(currentMode.txtbtns[9].t)
    game.currentplayer += 1
    hidebuttons()
    currentMode.txtbtns[6].t = 'Call'
    if game.currentplayer == 2:
        currentMode.txtbtns[6].t = 'Check'

def Raise2000():
    game.prevpot += int(currentMode.txtbtns[10].t)
    game.playerlist[game.currentplayer].money -= int(currentMode.txtbtns[10].t) #Raise 2000
    game.pot += int(currentMode.txtbtns[10].t)
    game.currentplayer += 1
    hidebuttons()
    currentMode.txtbtns[6].t = 'Call'
    if game.currentplayer == 2:
        currentMode.txtbtns[6].t = 'Check'
    
def fold():
    global currentMode    #When fold, player instance is removed from the list of players in game
    if game.currentplayer == 0:
        game.scenario = 2
    elif game.currentplayer == 1:
        game.scenario = 1 
        
    game.endgame()

def checkorcall():
    if currentMode.txtbtns[6].t == 'Call':
        game.playerlist[game.currentplayer].money -= game.prevpot
        game.pot += game.prevpot                               #Swap between call or check depending on if player 1 has raised or not.
    game.currentplayer += 1
    if game.currentplayer == 2:
        currentMode.txtbtns[6].t = 'Check'
    #add anti, so that each turn you still bet some money
