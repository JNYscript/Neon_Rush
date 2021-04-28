#Module importieren
from GBall_Normal import GBall_Normal
from Farben import Farbe
import pygame,Vektor,Spiel

class GBall_Two(GBall_Normal):

    def __init__(self, geschwindigkeit, window, hindernisse,leben = 1):

        self.leben = 1
        super().__init__(geschwindigkeit, window, hindernisse)
        self.farbe = Farbe.yellow
        


    def trefferDetection(self, liste):
        """Funktion schaut ob Kollision vorliegt zieht eventuell ein Leben ab und ändert die Farbe. Sollte die Kugel nur noch ein Leben haben wird sie auf Tod gestellt.

        Args:
            liste (list[Hindernisse]): Lsite mit Hindernissen

        Returns:
            [Ball]: Der Ball mit dem eine Kollision vorliegt
        """
        

        for b in liste:
            abstand = Vektor.vektorleange(Vektor.vektsub(
                (self.xpos, self.ypos), (b.xpos, b.ypos)))
            if abstand <= b.radius + self.radius:
                
                if self.leben <= 0:
                    self.alive = False
                    b.alive = False
                    return 
                else:
                    self.leben -= 1
                    self.farbe = Farbe.cyan
                    b.alive = False
                    return b

def testgballtwo():
    level_data = {
            "level": 1,
            "hindernisse": 2,
            "GBall_Normal": {
                "Anzahl": 2,
                "geschwindigkeit": 5
            },
            "GBall_Two": {
                "Anzahl":5,
                "geschwindigkeit":5
            }
            }
    game = Spiel.Test_Spiel(level_data)
    game.schleife_haupt()

if __name__ == "__main__":
    testgballtwo()