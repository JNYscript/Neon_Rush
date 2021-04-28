import pygame
import random
import Vektor


class Blood:
    """Klasse für Bluteffekte
    """

    def __init__(self, x, y, color, richtung, anzahl, window):
        """Konstruktor

        Args:
            x (int): X position
            y (int): y position
            color (Farbe): Farbe color
            richtung (Tuple): Richtung der Animation   
            anzahl (int): Anzahl der Blutpartikel
            window (pygame.window): Fenster der Darstellung
        """
        self.x = x
        self.y = y
        self.color = color
        self.win = window
        self.blood = []
        self.clock = pygame.time.Clock()

        for i in range(anzahl):
            self.blood.append(self.BloodPartikel(
                x, y, 7, self.color, richtung, self.win))

    def move(self):
        """Methode implementiert die Bewegung aller Blutpartikel
        """
        for i in self.blood:
            i.move()

    def malen(self):
        """Methode implementiert die Dartstellung aller Blutpartikel
        """
        for i in self.blood:
            i.malen()

    def run(self):
        """Methode implementiert einen Testcase 
        """
        clock = pygame.time.Clock()
        for i in range(10000):
            clock.tick(60)
            self.win.fill((255, 255, 255))
            self.move()
            self.malen()
            pygame.display.update()

    class BloodPartikel:
        """Klasse für Blutpartikel
        """

        def __init__(self, x, y, groesse, farbe, richtung, window):
            """Konstruktor Blutpartikel

            Args:
                x (int): X Position
                y (int): Y Position
                groesse (int): Größe des Blutpartikels
                farbe (Farbe): Farbe des Blutpartikels
                richtung (Tuple): Bewegungsrichtung des Blutpartikels
                window (pygame.window): Das Window
            """
            self.xpos = x
            self.ypos = y
            self.farbe = farbe
            self.groesse = random.randint(int(groesse/2), groesse)
            self.richtung = Vektor.vektrotation(
                richtung, random.randint(-20, 20))
            self.window = window
            self.geschwindigkeit = random.randint(2, 10)

        def move(self):
            """Methode implementiert die Bewegung eines Blutpartikels. Diese startet mit einer bestimmten Geschwindigkeit welche abnimmt und einer Richtung
            """
            self.xpos += self.geschwindigkeit * self.richtung[0]
            self.ypos += self.geschwindigkeit * self.richtung[1]
            # Geschwindigkeit nimmt langsam ab
            self.geschwindigkeit -= random.randint(0, 1)
            if self.geschwindigkeit < 0:
                self.geschwindigkeit = 0

        def malen(self):
            pygame.draw.rect(self.window, self.farbe,
                             (self.xpos, self.ypos, self.groesse, self.groesse))


# kleine Testfunktion
def test():

    WIN_WIDTH = 1000
    WIN_HEIGHT = 1000

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    Blut = Blood(500, 500, pygame.Color("Red"), [1, 0], 30, win)
    Blut.run()


if __name__ == "__main__":
    test()
