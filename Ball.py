
# Module importieren
import pygame
import random
import Vektor


class Ball():
    """Die Klasse Ball ist eine abstrakte Klasse von der alle anderen Bälle/Kugeln abgeleiter werden
    """

    def __init__(self, xpos, ypos, radius, farbe, window):
        """Abstrakte Klasse Ball Konstruktor

        Args:
            xpos (int): Die Xpos
            ypos (int): Die Ypos
            radius (int): Der Radius des Balls
            farbe (tuple): Farbe des Balls
            window (window): das Fenster in dem gespielt wird
        """
        self.radius = radius
        self.xpos = xpos
        self.ypos = ypos

        self.window = window
        self.farbe = farbe
        self.alive = True

    def collision_wand(self) -> tuple:
        """ Überprüft ob das Objekt mit einer Wand kollidiert. Gibt zurück um welche Wand es sich handelt.


        Returns:
            tuple: (bool:kollision mit rechter/linker Wand, bool: kollision mit oberer/unterer Wand)
        """

        # Abstand zur Wand mit Tupel vergleichen
        w = self.window.get_width()
        h = self.window.get_height()

        x = self.xpos
        y = self.ypos

        xbool = True

        ybool = True

        # Links/ Rechts und Oben/Unten schauen
        if x + self.radius/2 < w and x-self.radius/2 > 0:
            xbool = False
        if y+self.radius/2 < h and y-self.radius/2 > 0:
            ybool = False

        return xbool, ybool

    def trefferDetection(self, liste):
        """ Überprüft, ob eine Kollision mit einem Objekt aus der übergebenden Liste existiert

        Args:
            liste ([Ball]): Liste mit zu überprüfenden Bällen


        """

        for b in liste:
            abstand = Vektor.vektorleange(Vektor.vektsub(
                (self.xpos, self.ypos), (b.xpos, b.ypos)))
            if abstand <= b.radius + self.radius:
                self.alive = False
                b.alive = False
                return b

    def collision_gegensteande(self, liste) -> int:
        """Methode überprüft, ob eine Kollision zwischen dem Ball und einem Rechteck vorliegt. Gibt die Art der Kollision zurück


        Returns:
            [int]: Art der Kollision

            None : keine kollision
            1: Links/Rechts
            2: Oben/Unten
            3: Ecke Links Oben
            4: Ecke Links Unten
            5: Ecke Rechts Unten
            6: Ecke Rechts Oben

        """

        # alle gegenstände in der Liste durchgehen
        for g in liste:

            # Abstand errechnen
            abstand_x = abs(self.xpos - g.xm)
            abstand_y = abs(self.ypos - g.ym)

            # Einfache Fälle ausschließen
            if abstand_x > (g.b/2 + self.radius):
                continue

            # X und Y werte vergleichen
            if abstand_y > (g.h/2 + self.radius):
                continue

            if abstand_x <= g.b/2:

                return 1

            if abstand_y <= g.h/2:

                return 2

            # Abstand zu den Ecken ermitteln
            eckabstand = (abstand_x - g.b/2)**2 + (abstand_y - g.h/2)**2

            # jetzt wird noch bestimmt wo sich die Kugel relativ zum Objekt aufhält, anhand dessen kann man dann die Ecke bestimmen
            if (eckabstand <= (self.radius**2)):
                if self.xpos < g.xm:
                    if self.ypos < g.ym:
                        return 3
                    else:
                        return 4
                else:
                    if self.ypos < g.ym:
                        return 6
                    else:
                        return 5

        return None

    def move(self):
        """Abstrakte Methode. Soll Bewegung realisieren

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError("Please Implement this method")

    def malen(self):
        """Methode malt die Kugel mit Pygames
        """
        pygame.draw.circle(self.window, self.farbe,
                           (self.xpos, self.ypos), self.radius)
