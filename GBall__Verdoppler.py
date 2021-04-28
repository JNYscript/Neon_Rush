import pygame,Vektor,random,Spiel
from GBall_Normal import GBall_Normal
from Farben import Farbe
class GBall_Verdoppler(GBall_Normal):

    def __init__(self, geschwindigkeit, window, hindernisse, xpos = None , ypos = None , richtung = None, ausgewachsen = False):

        super().__init__(geschwindigkeit, window, hindernisse)
        self.farbe = Farbe.darkgreen
        self.verdopp_Pause = 200
        self.verdopp_erzeugen = 40 #Dieser Zähler verhindert, dass zu nahe an der Wand verdoppelt wird. Dies kann zu Bugs führen.
        self.verdopp_bool = False
        self.ausgewachsen = ausgewachsen
        self.radius = 5
        
        #Die Schleife wird nur angesteuert, wenn das Objekt ein Profukt einer Verdopplung ist. 
        if xpos != None:
            self.xpos = xpos
            self.ypos = ypos
            self.richtung = richtung
            
            

    
    def verdoppeln(self):
        """Methode realisiert das Verdoppeln

        Returns:
            GBall_Verdoppler: gibt neues Verdoppler Objekt zurück
        """

        #wenn noch nicht ausgewachsen
        if not self.ausgewachsen:
            self.radius += 1

            if self.radius > 40 : self.ausgewachsen = True


        #Reduziere die Verdopplungspausen Zähler
        self.verdopp_Pause -= 1

        if self.verdopp_Pause < 0 : 
            self.verdopp_Pause = 0
            self.farbe = Farbe.green

        #Wenn bereit erzeuge neues Verdopplungsobjekt
        if self.verdopp_bool:
            self.verdopp_erzeugen -= 1
            if self.verdopp_erzeugen < 0:
                self.verdopp_Pause = 200
                self.verdopp_erzeugen = 40
                self.verdopp_bool = False
                self.ausgewachsen = False
                self.radius = 5
                self.farbe = Farbe.darkgreen
                return  GBall_Verdoppler(self.geschwindigkeit,self.window,[],self.xpos,self.ypos,Vektor.vektrotation(self.richtung,random.choice([-30,-20,20,30])),False)

    

    def verdoppeln_test(self):
        """Methode schaut, ob der Ball bereit zum verdoppeln ist
        """
        if self.verdopp_Pause <= 0:
            self.verdopp_bool = True

    def move(self,liste):
        """alternative move Methode in welcher beim Abprallen eine neues BBall_verdoppler Objekt erzeugt wird.

        Args:
            liste (Hindernisse): Liste mit Hindernissen
        """
        

        alt_ypos = self.ypos
        alt_xpos = self.xpos

        self.xpos += int(self.richtung[0]*self.geschwindigkeit)
        self.ypos += int(self.richtung[1]*self.geschwindigkeit)

        bx,by = self.collision_wand()
        
        if bx :
            self.richtung[0] = (-1 )*self.richtung[0] 
            self.xpos,self.ypos=alt_xpos, alt_ypos
            self.verdoppeln_test()
        if by:
            self.richtung[1] = (-1 )*self.richtung[1] 
            self.xpos,self.ypos=alt_xpos, alt_ypos 
            self.verdoppeln_test()
        
        
            

        obj_coll = self.collision_gegensteande(liste)

        if obj_coll != None:
            self.verdoppeln_test()
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

        return self.verdoppeln()
            




#Testfunktion
def testverdoppler():
    
    level_data = {
            "level": 1,
            "hindernisse": 2,
            
            "GBall_Verdoppler": {
                "Anzahl":1,
                "geschwindigkeit":5
            }
            }
    game = Spiel.Test_Spiel(level_data)
    game.schleife_haupt()

if __name__ == "__main__":
    testverdoppler()