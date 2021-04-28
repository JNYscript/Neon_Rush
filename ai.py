import neat
import os
import pygame
import Vektor
import random
import Button

from Spiel import Survival_Spiel
from Farben import Farbe
from Spieler import Spieler
from Hindernisse import Hindernisse
from GegnerBall import GegnerBall


class AI(Spieler):

    def __init__(self, xpos, ypos, radius, farbe, window):


        super().__init__(xpos, ypos, radius, farbe, window)
        self.fitness = 0
        self.geschwindigkeit = 10
        self.wand_beruehrt = False
        self.next_enemy = None
        self.gegessen = False
        self.gegessen_besser = False
        self.next_enemy_besser = None

    def move_up(self):
        """Methode Bewegt KI nach oben schaut ob die Wand berührt wurde und setzt Position entsprechen zurück 
        """

        alt_ypos = self.ypos

        self.ypos -= self.geschwindigkeit
        if self.ypos - self.radius-10 < 0:
            self.ypos = alt_ypos
            self.wand_beruehrt = True

    def move_down(self):

        alt_ypos = self.ypos

        self.ypos += self.geschwindigkeit
        if self.ypos + self.radius+10 > 1000:
            self.ypos = alt_ypos
            self.wand_beruehrt = True

    def move_left(self):

        alt_xpos = self.xpos

        self.xpos -= self.geschwindigkeit
        if self.xpos - self.radius-10 < 0:
            self.xpos = alt_xpos
            self.wand_beruehrt = True

    def move_right(self):

        alt_xpos = self.xpos

        self.xpos += self.geschwindigkeit
        if self.xpos + self.radius + 10 > 1500:
            self.xpos = alt_xpos
            self.wand_beruehrt = True

    def abstand_wand(self):
        """Berechnet Bastand zur Wand

        Returns:
            int: Abstand zur Wand 
        """
        return [self.ypos, abs(self.ypos - 1000), self.xpos, abs(self.xpos - 1500)]

    def abstand_next(self, liste, besser):
        """Methode berechnet Abstand zum nächsten Objekt aus Liste

        Args:
            liste (list): liste mit Objekten
            besser (boolean): handelt es sich um besseres Essen?

        Returns:
            int: Abstand zum nächsten Essen
        """
        abstand_min = 3000
        #Alle Objekte durchprobieren und nächstes abspeichern
        for i in liste:
            abstand = Vektor.vektorleange(Vektor.vektsub(
                [self.xpos, self.ypos], [i.xpos, i.ypos]))
            if abstand < abstand_min:
                abstand_min = abstand
                if besser:
                    self.next_enemy_besser = i
                else:
                    self.next_enemy = i

        return (self.xpos-self.next_enemy.xpos, self.ypos-self.next_enemy.ypos)

    def malen(self):
        """Methode stellt das KI Objekt dar und malt Linien repräsentativ für den Abstand zum nächsten Essen.
        """

        pygame.draw.line(self.window, (0, 0, 0), (self.xpos, self.ypos),
                         (self.next_enemy.xpos, self.next_enemy.ypos))
        pygame.draw.line(self.window, (0, 0, 255), (self.xpos, self.ypos),
                         (self.next_enemy_besser.xpos, self.next_enemy_besser.ypos))
        pygame.draw.circle(self.window, self.farbe,
                           (self.xpos, self.ypos), self.radius)


def main(genomes, config):
    """Methode implementiert den Ablauf einer einzelnen Generation

    Args:
        genomes (Tuple): Genome Nr, Genome Object
        config (str): Pfad zur Config Datei
    """

    # Variablen defnieren
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    win = run.win
    font = pygame.font.SysFont("Arial", 50)
    clock = pygame.time.Clock()
    hintergrund = pygame.image.load(os.path.join(
        sourceFileDir, "Bilder", 'Hintergrund_Ki.png'))
    essen = []
    essen_besser = []

    # Gegner Erstellen
    for i in range(10):
        essen += [GegnerBall(30, Farbe.green, 0, win, [])]

    for i in range(4):
        essen_besser += [GegnerBall(30, Farbe.darkgreen, 0, win, [])]


    zeit = 0

    
    nets = []   #hier werden die neuronalen netze gespeichert
    ge = []     #hier werden die Genome gespeichert 
    ais = []    #Hier werden die KIs gespeichert

    #AIs, Gnome, Netze erstellen und speichern
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets += [net]
        ais += [AI(random.randint(100, 1400),
                   random.randint(100, 900), 20, (255, 255, 255), win)]
        g.fitness = 0
        ge += [g]

        RUN = True


    back_button = Button.button((0, 0, 0), 50, 50, 130, 130)
    start_ticks = pygame.time.get_ticks() #Ticks zählen
    ende = 0
    #Haptschleife
    while RUN:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                if back_button.isOver(mousepos):
                    ge[0].fitness = 10000

        #Durchläufe zählen
        ende += 1
        zeit = (pygame.time.get_ticks()-start_ticks)/1000

        #Fürs Essen Belohnen
        for x, ai in enumerate(ais):

            if ai.gegessen:

                ge[x].fitness += 1

                ai.gegessen = False

            if ai.gegessen_besser:

                ge[x].fitness += 6

                ai.gegessen_besser = False

            #hier wird dem Netzt input gegeben. Der Abstand zum Essen
            abstand_essen = ai.abstand_next(essen, False)
            abstand_essen_besser = ai.abstand_next(essen_besser, True)
            #Neuronales Netz gibt output zurück
            output = nets[x].activate(
                (abstand_essen[0], abstand_essen[1], abstand_essen_besser[0], abstand_essen_besser[1]))

            #Der output des Netzt wird in Aktionen umgewandelt
            if output[0] > 0.5:
                ai.move_up()

            if output[1] > 0.5:
                ai.move_down()

            if output[2] > 0.5:
                ai.move_left()

            if output[3] > 0.5:
                ai.move_right()


        #schauen ob Essen gegessen wurde
        for x, g in enumerate(essen):
            esser = g.trefferDetection(ais)
            if esser != None:
                esser.gegessen = True
                essen.pop(x)

        for x, g in enumerate(essen_besser):
            esser = g.trefferDetection(ais)
            if esser != None:
                esser.gegessen_besser = True
                essen_besser.pop(x)

        #Schauen ob man die schleife beenden kann
        if ende > 200:
            RUN = False
            break
        
        #Alles darstellen
        if run.gen % 1 == 0:

            win.blit(hintergrund, (0, 0))

            for ai in ais:
                ai.malen()

            for g in essen:

                g.malen()

            for g in essen_besser:
                g.malen()

            show_generation(font, win)
            show_time(font, zeit, win)

            pygame.display.update()

    #Generationenzähler hochsetzen
    run.gen += 1


def show_time(font, zeit, win):
    """Methode gibt die abgelaufene Zeit aus

    Args:
        font (pygame.Font): Schriftart
        zeit (float): abgelaufene zeit
        win (pygame.Window): das window
    """
    time_text = font.render("Sekunden:%8.2f" %
                            (zeit), 1, pygame.Color("white"))
    win.blit(time_text, (800, 50))


def show_generation(font, win):
    """Methode gibt die aktuelle Generationsnummer aus

    Args:
        font ([type]): [description]
        win ([type]): [description]
    """
    time_text = font.render(f"Generation: {run.gen}", 1, pygame.Color("white"))
    win.blit(time_text, (400, 50))


def run(config_file, win):
    """Diese Methode implementiert den Ablauf des NEAT Algorithmus

    Args:
        config_file (string): Pfad zur Config Datei
        win (pygame.window): Window
    """
    run.win = win
    run.gen = 1

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    winner = p.run(main, 500)




#Testfunktion
if __name__ == "__main__":
    pygame.init()
    WIN_WIDTH = 1500
    WIN_HEIGHT = 1000
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path, win)
