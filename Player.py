class Player: #player information for the game
    def __init__(self,x,y):
        self.firstname = ''
        self.lastname = ''
        self.stuID = ''
        self. money = 25000
        self.hand = []
        self.x = x
        self.y = y
        self.initials = ''
        self.name = ''
        
    def resetPlayer(self):
        self.firstname = ''
        self.lastname = ''
        self.stuID = ''
        self. money = 25000
        self.hand = []
        self.initials = ''
        self.name = ''
