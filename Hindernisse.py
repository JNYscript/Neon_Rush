
import pygame,random
from Farben import Farbe
from Spieler import Spieler


class Hindernisse():

    def __init__(self, anzahl, _max, _min, spiel=None, win=None):
        """Konstruktor für die Hindernisse im level

        Args:
            anzahl (int): Anzahl der Hindernisse
            _max (int): Max größe der Hindernisse
            _min (int): Min größe der Hindernisse
            spiel (Spiel, optional):  Das Level in welchem die Hidnernisse dargestellt werden sollen. Defaults to None.
            win (pygame.win, optional): Das Fenster in dem gemalt werden soll. Defaults to None.
        """
        self.hliste = []
        self.spiel = spiel
        self.max = _max
        self.min = _min
        if spiel == None:
            self.win = win
        else:
            self.win = spiel.win

        #Hinsernisse erstellen
        for i in range(anzahl):
            self.hliste += [self.Rechteck(random.randint(100,1400),random.randint(100,900),random.randint(_min,_max),random.randint(_min,_max),self.win)]

    def malen(self):
        """Methode malt alle Hindernisse
        """
        for h in self.hliste:
            h.malen()

    class Rechteck():

        def __init__(self, xpos, ypos, b, h, win):
            self.b = b
            self.h = h
            self.xpos = xpos
            self.ypos = ypos
            
            self.win = win
            self.xm = int(xpos+b/2)
            self.ym = int(ypos+h/2)
            

        def malen(self):
            """Methode malt das Rechteck
            """
            pygame.draw.rect(self.win, Farbe.grey,
                             (self.xpos, self.ypos, self.b, self.h))

            pygame.draw.rect(self.win, Farbe.black,
                             (self.xpos, self.ypos, self.b-10, self.h-15))


        
#kleine Testfunktion
def hindernissetest():
    WIN_WIDTH = 1680
    WIN_HEIGHT = 1000
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    hindernisse = Hindernisse(1,500,100,win = win)
    pygame.key.set_repeat(10)
    clock = pygame.time.Clock()
    Run = True
    
    win.fill((255, 255, 255))
    pygame.draw.circle(win, (0, 0, 255), (400, 400), 10)
    while Run:
        clock.tick(60)
    

        win.fill((255, 255, 255))
        
        
        hindernisse.malen()
        pygame.display.update()

        # print(f'{P1.xpos},{P1.ypos}')


if __name__ == "__main__":
    hindernissetest()