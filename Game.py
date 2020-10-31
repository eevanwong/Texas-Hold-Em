import random
class Game:
    def __init__(self):
        self.deck = [[True]*4 for i in range(13)]
        self.cards = loadImage('cards.png') #(949,392) #load this later
        self.cardw = self.cards.width/13
        self.cardh = self.cards.height/4
        
        self.community = []
        self.cardsdrawn = 0
        self.roundnum = 1
        self.playerlist = []
        self.currentplayer = 0
        self.pot = 0
        self.prevpot = 0            #prevpot represents the amount of money that the person bets (i.e, when someone bets a certain amount, adds to prev pot, when person raises, they add money on top of the prevpot)
        self.finish = False
        self.scenario = -1         #scenario represents which scenario did the game end in. Did one player fold? Did one win in the final round? Did they tie?

        
    def addplayer(self,Player): #add instance of player
        self.playerlist.append(Player)     #works so that for every player theres another player that plays in the game
        
    def newround(self):  
        self.roundnum += 1
        if self.roundnum == 2: 
            self.flopround()
            
        elif self.roundnum == 3 or self.roundnum == 4:
            self.lastrounds()

        elif self.roundnum == 5:
            self.finishturn()
             
    
    def getcard(self):
        cardexists = False
        if self.cardsdrawn == 52:
            self.resetdeck()
            self.cardsdrawn = 0
            
        while not(cardexists):
            suit = random.randint(0,3)
            card = random.randint(0,12)
            if self.deck[card][suit]:
                self.cardsdrawn += 1
                self.deck[card][suit] = False
                cardexists = True

        
        return(card,suit)
    
    def addcard(self): #displays all cards
        for i in range(2):
            for i in self.playerlist:        #at beginning, every player gets 2 cards
                i.hand.append(self.getcard()) 
    
    def resetgame(self):
        self.deck = [[True]*4 for i in range(13)]
        self.community = []
        self.cardsdrawn = 0
        self.roundnum = 1
        self.currentplayer = 0
        self.pot = 0
        self.prevpot = 0            
        self.finish = False
        self.scenario = -1
        
        for i in self.playerlist:
            i.money -= 500
            self.pot += 500
        
        for i in range(2):
            for j in self.playerlist:        #at beginning, every player gets 2 cards
                j.hand.append(self.getcard())
                
   
    def flopround(self):
        for i in range(3):    
            self.community.append(self.getcard())
            
    def lastrounds(self):
        self.community.append(self.getcard())
        
            
    def finishturn(self):#after 4th round, this runs and compares the ranking
        print('endgame')
        Phand = []
        for i in self.playerlist:
            Phand.append(i.hand + self.community) 
        cardvalues = []
        for player in Phand:
            cardvalues.append([i[0] for i in player])
        
            #i.hand.extend(self.community)
        playerranks = [checkrank(i) for i in Phand] #checks hand of each player and replaces it with a value (highest being the royal flush, and lowest being the highest one card)
        print(playerranks)
        
        if playerranks[0][0] > playerranks[1][0]: #compares rank
            self.scenario = 1
        elif playerranks[0][0] < playerranks[1][0]:
            self.scenario = 2
        else:
            self.scenario = tie(playerranks[0][1],playerranks[1][1], cardvalues, self.scenario) #if by chance index 1 is the high card that was caluclated in the functions
       # print(max(Phand[0],max(Phand[1]))    
        self.endgame()
        
    def resetdeck(self,deck):
        self.deck = [[True]*4 for i in range(13)]
        return(self.deck)
    
    
    def endgame(self):  #function will only run if 1) the game has reached the end, or 2) someone has folded

        if self.scenario == 1: #player 1 wins
            #self.playerlist.pop(1)
            self.playerlist[0].money += self.pot
            self.pot = 0
            print(str(self.playerlist[0].name) + ' win')
            self.currentplayer = 0
            
        elif self.scenario == 2: #player 2 wins
            #self.playerlist.pop(0)
            self.playerlist[1].money += self.pot
            print(str(self.playerlist[1].name) + ' win')
            self.pot = 0
            self.currentplayer = 1
            
        elif self.scenario == 3: #tie, both players get half of the pot
            for i in range(len(self.playerlist)):
                self.playerlist[i].money += self.pot/2
                self.pot = 0
        
        self.finish = True 


    
    def display(self):
        x = 200
        for i in self.community: #displays community card
            x+=75
            copy(self.cards,i[0]*self.cardw,i[1]*self.cardh,self.cardw,self.cardh,x,265, self.cardw,self.cardh)
        
        for i in self.playerlist: #displays cards in player hand
            x = i.x
            y = i.y
            for j in i.hand:
                copy(self.cards,j[0]*self.cardw,j[1]*self.cardh,self.cardw,self.cardh,x,y, self.cardw,self.cardh)
                x += 75
            
                
        if self.currentplayer == len(self.playerlist):   #if current player is the last player, it will go back to first player
            self.currentplayer = 0
            self.newround()
            self.prevpot = 0         #amount of money bet per player resets to 0 each round
            
        if len(self.playerlist) > 0:
            fill(255,255,100)
            #rect(self.playerlist[self.currentplayer].x - 100, self.playerlist[self.currentplayer].y, 100,50)   #rect that corresponds with whos turn it is
            textAlign(CENTER,CENTER)
            fill(255)
            textSize(20)
            text(self.playerlist[self.currentplayer].initials + "'s" + " turn", self.playerlist[self.currentplayer].x-50, self.playerlist[self.currentplayer].y+25)
        
        for i in self.playerlist: #displays amount of money each player has
            x = i.x
            y = i.y
            fill(255)
            textSize(25)
            text(str(i.initials) + "'s Money: " + str(i.money), x-25,y-25)
        text("Pot: " + str(self.pot), 450 , 375)
       # text(
        #A bunch of the functions are outside because it doesnt matter if its with the class or not (if they were they would have a bunch of self statements)

def tie(P1,P2, hand, scenario):
    if P1 > P2:   #comparison for highest card of combination
        return(1)
    elif P1 < P2:
        return(2)
    else:  
        #if all else fails, highest single card
        hand[0].sort()
        hand[1].sort()
        for i in range(len(hand[0])):
            if max(hand[0]) > max(hand[1]):
                return(1)
            elif max(hand[1]) > max(hand[0]):
                return(2)
            elif max(hand[1]) == max(hand[0]):
                hand[0].pop()
                hand[1].pop()
            else:
                return(3)

#copy(image source,x of source upper left corner, y of source upper left corner, img width, img height,x,y,w,h)

def checkrank(hand): #everything is outside because if it was inside it would require a lot of self.
    print(hand)
    card = [i[0] for i in hand]
    repofcardvalues = {} 
    for i in card:
        if i in repofcardvalues:     
            repofcardvalues[i] += 1
        else:
            repofcardvalues[i] = 1
            
    checksf = checkstraightflush(repofcardvalues, card,hand)
    check4 = check4ofkind(repofcardvalues)
    checkfh = checkfullhouse(repofcardvalues)
    checkf = checkflush(hand)
    checks = checkstraight(repofcardvalues,card)
    check3 = checktrip(repofcardvalues)
    check2p = check2pair(repofcardvalues)
    checkp = checkpair(repofcardvalues)
    #print(checkstraight(repofcardvalues,card))
    #if checkroyalflush(hand):
        #return(10)  
    if checksf[0]:    #checks straight flush, recieves boolean and highest card (incase of tie)
        return(9,checksf[1]) #the [0] represents the boolean value that the check function will return (because it returns boolean and highest card)
    elif check4[0]:        #check 4 of kind
        return(8,check4[1])
    elif checkfh[0]:        #check full house
        return(7,checkfh[1])
    elif checkf[0]:           #check flush
        return(6,checkf[1])
    elif checks[0]:           #check straight
        return(5,checks[1])
    elif check3[0]:                #check trips
        return(4,check3[1])
    elif check2p[0]:   #check 2 pairs
        return(3,check2p[1])
    elif checkp[0]: #check pair
        return(2,checkp[1])
    else:
        return(1,max(card))

        #ALL FUNCTIONS CHECK WHAT THE HIGHEST CARD IS IN CASE OF TIE BETWEEN 2 PLAYERS
        
            #a is the repetition of card values

def checkpair(a): #check a pair 
    for i in a:
        if a[i] == 2:
            return(True, i)   #if false, value returns 0, as functions dont work if only given boolean
    return(False,0)

def check2pair(a): #check 2 pairs
    highcard = 0
    numpairs = 0
    for i in a:
        if a[i] == 2:
            numpairs += 1
            if i > highcard:
                highcard = i
    if numpairs == 2:
        return(True, highcard)
    else:
        return(False,0)

def checktrip(a): #check 3 of a kind
    highcard = 0
    numtrip = 0  
    for i in a:
        if a[i] == 3:       #dont need to consider how many triples there are, as it wouldve checked in the full house
            numtrip += 1
            highcard = i
    if numtrip == 1:
        return(True,highcard)
    else:
        return(False,0)


#cardrange = max(card[i:i+5]) - min(card[i:i+5]):
def checkstraight(a,card): #check straight
    card.sort()    
    if len(card) >= 5:    
        highcard = 0
        foundstraight = False
        for i in range(len(card)-4):  #i represents the lowest amount of the comparison, [i:i+5] splices the entire list but the next 4 items in the sorted cards, checking if it is a straight
            cardrange = card[i:i+5][4] - card[i:i+5][0]
            if 0 in card and [card[0],card[i+1],card[i+2],card[i+3],card[i+4]] == [0,9,10,11,12]:   #code for royal flush (because its essentially a straight except for ace)
                return(True,13)            #the moment it returns, the rest of the function passes, so if its a royal flush itll return that value
            if cardrange == 4:
                numsingle = 0
                #print(card[i:i+5])
                for j in card[i:i+5]:     #To find highest card, goes through straights (if there is more than one combination) and finds the highest of each combination
                    if a[j] == 1:
                        numsingle += 1
                if numsingle == 5:
                    foundstraight = True
                    if highcard < card[i:i+5][4]:   #card[i:i+5][4] represents the final/highest card of the straight combination
                        highcard = card[i:i+5][4]
        if foundstraight:
            return(True,highcard)
    return(False,0)
                
def checkflush(hand): #check flush
    suit = [i[1] for i in hand] #gets hand instead of a because it checks suit, not card number
    suitofflush = 0  # suit of the flush
    highcard = 0
    repofsuits = {} 
    cardsofsuit = [] 
    flushexists = False                        
    for i in suit:
        if i in repofsuits:
            repofsuits[i] += 1
        else:
            repofsuits[i] = 1
    for i in repofsuits:
        if repofsuits[i] >= 5:
            suitofflush = i
            flushexists = True
    for i in hand:
        if i[1] == suitofflush:
            cardsofsuit.append(i[0])
    if flushexists:
        highcard = max(cardsofsuit)
        return(True,highcard)
    else:
        return(False,0)

def checkfullhouse(a): #check full house 
    numpairs = 0       #highest card is dependent on the highest triple combination
    numtrips = 0
    highcard = 0
    for i in a:
        if a[i] == 2:
            numpairs += 1
        elif a[i] == 3:
            numtrips += 1
            if i > highcard:
                highcard = i
    if numpairs >= 1 and numtrips >= 1:
        return(True,highcard)
    else:
        return(False,0)
            
def check4ofkind(a): #4 of a kind
    highcard = 0
    for i in a:
        if a[i] == 4:
            highcard = i
            return(True,highcard)
        else:
            return(False,0)
        
def checkstraightflush(a,card,hand): #straight flush - only requires 
    if checkstraight(a,card)[0] and checkflush(hand)[0]:
        return(True, checkstraight(a,card)[1])
    else:
        return(False,0) #counts for royal flush as well, as the numerical value returned will be higher than a regular straight flush
