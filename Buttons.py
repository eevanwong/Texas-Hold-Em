class Buttons: 
    def __init__(self, x, y, w, h, t, ts=30):     
        self.x = x
        self.y = y
        self.w = w

        self.h = h
        self.t = t
        
        self.bigts = ts + 4
        self.ts = ts
        self.smallts = ts
        
        self.action = self.k 
        
        self.hitbox = False
        self.font = createFont("Qanelas-Black.otf", 50, True)

        self.showbutton = True        
    
    def k(self):       #placeholder function for the action of a button
        print('k')
        #pass
    def display(self):
        
        if self.showbutton:
            
            self.hitbox = self.x - self.w/2 <= mouseX <= self.x + self.w/2 and self.y - self.h/2 <= mouseY <= self.y + self.h/2
            if self.hitbox:
                self.ts = self.bigts
                
            else:
                self.ts = self.smallts
                
            
            textFont(self.font)
            textMode(CENTER)
            textAlign(CENTER,CENTER)
            textSize(self.ts)
            fill(255)
            text(self.t, self.x, self.y)
            
          
class ImageButtons:
    def __init__(self,x, y, w, h, img):
        self.img = img
        self.loadedimg = loadImage(img)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hitbox = self.x - self.w/2 <= mouseX <= self.x + self.w/2 and self.y - self.h/2 <= mouseY <= self.y + self.h/2
        self.action = self.k 

    def k(self):
        print('k')
        #pass
        
    def displaybutton(self):
        self.hitbox = self.x - self.w/2 <= mouseX <= self.x + self.w/2 and self.y - self.h/2 <= mouseY <= self.y + self.h/2
        if self.hitbox:
            tint(125)
        else:
            tint(255)
            
        image(self.loadedimg, self.x, self.y)
            


    
