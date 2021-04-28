import  pygame,os,Sound
class button():
    def __init__(self, farbe, x,y,breite,hoehe, text=''):
        self.farbe = farbe
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.text = text
        

    def draw(self,win,outline=None):
        """Methode zeichnet einen

        Args:
            win (display): Window
            outline (boolean, optional): Umrandung. Defaults to None.
        """
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.breite+4,self.hoehe+4),0)
            
        pygame.draw.rect(win, self.farbe, (self.x,self.y,self.breite,self.hoehe),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.breite/2 - text.get_breite()/2), self.y + (self.hoehe/2 - text.get_hoehe()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.breite:
            if pos[1] > self.y and pos[1] < self.y + self.hoehe:
                Sound.klick.play()
                return True
            
        return False 