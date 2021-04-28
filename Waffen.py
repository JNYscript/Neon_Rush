import pygame,Vektor,Spieler,Sound,Farben
from Ball import Ball
from GegnerBall import GegnerBall
class Bullets():
    
    def __init__(self,window):
        """Konstruktor Waffe

        Args:
            window (pygame.window): Das Fenster
        """
        
        self.BulletList = []
        self.window = window
        self.bereit = True
        
        self.geschw = 10
        self.zeahler = self.geschw
    def schiessen(self,x,y,m):
        """Methode realisiert das Abschießen einer Kugel

        Args:
            x (int): x Koordinate
            y (int): y Koordinate
            m (touple): Richtungsvektor
        """

        #Schauen ob die Waffe bereit zum Schießen ist
        if self.bereit:
            Sound.laser.play()
            self.BulletList += [self.Bullet(x,y,m,self.window)]
            self.bereit = False

    def move(self,hindernisse):
        """Methode bewegt alle Kugeln

        Args:
            hindernisse (Hindernisse Liste): Liste mit Hindernissen
        """

        #bereit zähler verringern
        if not self.bereit:
            self.zeahler -= 1
            if self.zeahler < 0:
                self.bereit = True
                self.zeahler = self.geschw
        #Alle Kugeln bewegen
        for b in self.BulletList:
            if b.collision_gegensteande(hindernisse) != None:
                b.alive = False
            if not b.alive:
                self.BulletList.remove(b)
            else:    
                b.move()
    def malen(self):
        """Methode malt alle Kugeln der Waffe
        """
        for b in self.BulletList:
            b.malen()
    
  
        
        
    class Bullet(Ball):

        def __init__(self,xpos,ypos,richtung,window):

            self.richtung = richtung
            super().__init__(xpos,ypos,2,(0,255,0),window)
            


            
        
        
        def move(self):
            """Methode bewegt die Kugel. Schaut, ob sie mit der Wand kollidiert ist und löscht sie eventuell.
            """

            self.xpos += int(15*self.richtung[0])
            self.ypos += int(15*self.richtung[1])
            
            xc , yc = self.collision_wand()
            if xc or yc:
                self.alive = False
                
            
class Bullets_Gegner(Bullets):

    def __init__(self, window):
        super().__init__(window)
        self.geschw = 2

        

#kleine Testfunktion
def Waffentest():
    import os
    from Run import Run
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    WIN_WIDTH = 1500
    WIN_HEIGHT = 1000
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    run = Run(win)
    run.run()

if __name__ == "__main__":
    Waffentest()