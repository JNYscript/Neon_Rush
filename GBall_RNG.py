import pygame
import random
import Vektor
import Spiel
from GBall_Normal import GBall_Normal
from Farben import Farbe


class GBall_RNG(GBall_Normal):

    def __init__(self, geschwindigkeit, window, hindernisse):
        super().__init__(geschwindigkeit, window, hindernisse)
        self.rng = 0.02
        self.farbe = Farbe.purple

    def move(self, liste):
        """Wie bei Oberklasse. Zusätzlich kommt noch die Möglichkeit hinzu den Richtungsvektor zufällig zu ändern.

        Args:
            liste (list[Hindernisse]): Liste mit Hindernissen
        """

        #

        if random.random() < self.rng:
            grad = random.choice([-90, 90, 180])
            self.richtung = Vektor.vektrotation(self.richtung, grad)
        super().move(liste)


# kleine Testfunktion
def testgballrng():
    level_data = {
        "level": 1,
        "hindernisse": 2,
        "GBall_Normal": {
            "Anzahl": 2,
            "geschwindigkeit": 5
        },
        "GBall_RNG": {
            "Anzahl": 5,
            "geschwindigkeit": 10
        }
    }
    game = Spiel.Test_Spiel(level_data)
    game.schleife_haupt()


if __name__ == "__main__":
    testgballrng()
