import pygame
import Vektor
import random
from GBall_Normal import GBall_Normal
from Farben import Farbe


class GBall_Shoot(GBall_Normal):

    def __init__(self, geschwindigkeit, window, hindernisse, spieler, shoot=0.01):

        super().__init__(geschwindigkeit, window, hindernisse)
        self.shoot = shoot
        self.farbe = Farbe.beige
        self.spieler = spieler

    def move(self, liste):
        """Alternative Methode für die Shoot Bälle. Optional können sie mit einer Wahrscheinlichkeit bei jeder Bewegung schießen

        Args:
            liste (Hindernisse Liste): Liste mit den Hindernissen in einem Level

        Returns:
            [vektor]: Normierter Vektor in Richtung Spieler.
        """
        super().move(liste)
        if random.random() < self.shoot:
            return self.vektor_spieler()

    def vektor_spieler(self):
        """Errechnet normierten Vektor in richtung Spieler

        Returns:
            [Vektor]: Vektor richtung Spieler
        """
        vektor_spieler = [self.spieler.xpos, self.spieler.ypos]
        vektor_gegner = [self.xpos, self.ypos]
        return Vektor.vektornomieren(Vektor.vektsub(vektor_spieler, vektor_gegner))

    def malen(self):
        """Methode malt Kugel und die Waffe
        """

        # Waffe malen
        vek = Vektor.vektadd((self.xpos, self.ypos), Vektor.vektormult(
            self.vektor_spieler(), self.radius+10))
        pygame.draw.line(self.window, (0, 0, 0),
                         (self.xpos, self.ypos), vek, 5)
        super().malen()

#kliene Testfunktion
def shootballtest():
    from Spiel import Test_Spiel
    level_data = {
        "level": 1,
        "hindernisse": 2,
        "GBall_Normal": {
            "Anzahl": 10,
            "geschwindigkeit": 5
        },
        "GBall_Shoot": {
            "Anzahl": 2,
            "geschwindigkeit": 5
        }
    }
    game = Test_Spiel(level_data)
    game.schleife_haupt()


if __name__ == "__main__":
    shootballtest()
