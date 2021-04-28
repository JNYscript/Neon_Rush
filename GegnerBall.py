import pygame,random,math,Vektor
from Ball import Ball
class GegnerBall(Ball):

    def __init__(self,radius,farbe,geschwindigkeit,window,hindernisse):
        """ Constructor

        Args:
            radius (int): Radius
            farbe (list): Farbe des Balls
            geschwindigkeit (int): Geschwindigkeit des Balls        
            window (window): 
            hindernisse (Hindernisse Liste): Liste mit Hidernissen. Wird zur Erstellung benötigt.
        """

        self.radius = radius
        self.xpos = random.randint(2*radius+400,window.get_width()-2*radius)
        self.ypos = random.randint(2*radius,window.get_height()-2*radius)
        
        while self.collision_gegensteande(hindernisse) != None:
            self.xpos = random.randint(2*radius+400,window.get_width()-2*radius)
            self.ypos = random.randint(2*radius,window.get_height()-2*radius)
       
        
        super().__init__(self.xpos, self.ypos, radius,farbe,window)

        self.richtung = Vektor.randomnormiertvekt()
        
        self.geschwindigkeit = geschwindigkeit
        
    
    def move(self,liste):
        """Bewegt den Ball. Berechnet das Abprallen

        Args:
            liste (list[Hindernisse]): [description]
        """

        #Alte Position speichern
        alt_xpos = self.xpos
        alt_ypos = self.ypos

        #Bewegen
        self.xpos += int(self.richtung[0]*self.geschwindigkeit)
        self.ypos += int(self.richtung[1]*self.geschwindigkeit)

        #Kollisionsabfrage Wand
        bx,by = self.collision_wand()
        
        #Richtung ändern
        if bx :
            self.richtung[0] = (-1 )*self.richtung[0] 
            self.xpos,self.ypos=alt_xpos, alt_ypos  
            return
        if by:
            self.richtung[1] = (-1 )*self.richtung[1] 
            self.xpos,self.ypos=alt_xpos, alt_ypos
            return  
        

        #Kollision mit Hindernissen
        obj_coll = self.collision_gegensteande(liste)

        #Richtung ändern
        if obj_coll != None:

            if obj_coll == 2:
                self.richtung[0] = (-1 )*self.richtung[0] 
                self.xpos,self.ypos=alt_xpos, alt_ypos  
            elif obj_coll ==1:
                self.richtung[1] = (-1 )*self.richtung[1] 
                self.xpos,self.ypos=alt_xpos, alt_ypos  
            elif obj_coll == 3:
                self.richtung = [-0.707106,-0.707106]
                self.xpos,self.ypos=alt_xpos, alt_ypos
            elif obj_coll == 4:
                self.richtung = [-0.707106,0.707106]
                self.xpos,self.ypos=alt_xpos, alt_ypos        
            elif obj_coll == 5:
                self.richtung = [0.707106,0.707106]
                self.xpos,self.ypos=alt_xpos, alt_ypos  
            else :
                self.richtung = [0.707106,-0.707106]
                self.xpos,self.ypos=alt_xpos, alt_ypos  
        
    

    
    




#kleine Testfunktion 
def GegnerBalltest():
    
    WIN_WIDTH = 1680
    WIN_HEIGHT = 1000

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    pygame.key.set_repeat(10)
    clock = pygame.time.Clock()
    Run = True
    P1 = GegnerBall(20,(255,0,0),5,win,[])
    win.fill((255, 255, 255))
    pygame.draw.circle(win, (0, 0, 255), (400, 400), 10)
    beallearray = []
    for i in range(10000):
        beallearray += [GegnerBall(random.randint(10,30),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),random.randint(2,15),win,[])]

    while Run:
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                    Run = False
        clock.tick(60)
        win.fill((255, 255, 255))
        P1.move([])
        P1.malen()
        for b in beallearray:
            b.move([])
            b.malen()
        pygame.display.update()

if __name__ == "__main__":
    GegnerBalltest()
