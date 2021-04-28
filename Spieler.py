#Module importieren
import pygame
import math
import Vektor,Waffen
from Ball import Ball



class Spieler(Ball):

    def __init__(self, xpos, ypos, radius, farbe,window):
        """Klasse spieler

        Args:
            xpos (int): X Position spieler
            ypos (int): Y Position spieler
            radius (int): Radius der Spieler Kugel
            farbe (Farbe): Farbe der Spieler Kugel
            window (pygame.window): Fenster in welchem gemalt werden soll
        """

        super().__init__(xpos, ypos, radius, farbe,window)
        self.keys = {'right': False, 'up': False, 'left': False, 'down': False}
        
        self.godmode = False


    
    def malen(self):
        """Methode malt die Spieler Kugel + Waffe
        """

        self.waffe_malen()
        super().malen()

    
    def move(self):
        """Methode ist in der Klasse Spiel implementiert
        """
        return
        
    

    def waffe_malen(self):
        """Methode malt die Waffe des Spielers und errechnet dazu einen Einheitsvektor in Richtung Spieler
        """
        mx, my = pygame.mouse.get_pos()

        #Vekor zur Mausposition
        self.richtung = Vektor.vektornomieren(
            Vektor.vektsub((mx, my), (self.xpos, self.ypos)))

        vek = Vektor.vektadd((self.xpos, self.ypos),Vektor.vektormult(self.richtung, 30))

        pygame.draw.line(self.window, (100, 100, 100),(self.xpos, self.ypos), vek, 5)
       

#Kleine Testfunktion
def testgball():
    import Spiel
    level_data = {
            "level": 1,
            "hindernisse": 2,
            "GBall_Normal": {
                "Anzahl": 1,
                "geschwindigkeit": 0
            }
            }
    game = Spiel.Test_Spiel(level_data)
    game.schleife_haupt()

if __name__ == "__main__":
    testgball()
