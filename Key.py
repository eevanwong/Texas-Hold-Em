class Keys: #if i need a method to check the key entry for info, I basically need a new class
    def __init__(self):
        self.enabled = False
        self.info = ''
        self.x = 0
        self.y = 0
        self.ts = 25
        self.minlen = 3
        self.maxlen = 10
        self.acceptedchars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        self.enteraction = None
        
    def display(self):
        fill(255)
        textSize(self.ts)            #displays keys in name menu interface
        text(self.info, self.x, self.y)
        rectMode(CENTER)
        noFill()
        stroke(255)
        rect(self.x, self.y , 200, 40)
        if self.enabled:
            ellipse(self.x-100, self.y,25,25)

    
    def update(self, keyinput):
        if self.enabled:
            if len(self.info) < self.maxlen and keyinput != CODED and str(keyinput).upper() in self.acceptedchars:
                    self.info += str(keyinput).upper()
            elif keyinput == BACKSPACE and len(self.info) > 0:
                self.info = self.info[:-1]
            elif keyinput == ENTER and len(self.info) >= self.minlen:
                self.enteraction()
