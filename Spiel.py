#Module und Klassen importieren


import os,pygame,random,Sound,threading,Vektor

from Waffen import Bullets,Bullets_Gegner
from Spieler import Spieler

from Hindernisse import Hindernisse
from Blood import Blood
from Farben import Farbe

class Test_Spiel():

    
    
    def __init__(self, data):
        """Kosntruktor Test_Spiel

        Args:
            data (dic): Ein dictionary mit den Level Parametern
        """
        self.sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.WIN_WIDTH = 1500
        self.WIN_HEIGHT = 1000
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))

        
        self.clock = pygame.time.Clock()
        
        self.hintergrund = pygame.image.load(os.path.join(self.sourceFileDir,"Bilder",'Hintergrund_Spiel.png'))
        
        self.gegner = []    #in dieser Liste werden die gegner gespeichert
        
        #Bulletklassen für Spieler und Gegner erstellen
        self.bullets_spieler = Bullets(self.win)
        self.bullets_gegner = Bullets_Gegner(self.win)
        
        #Hindernisse erstellen
        self.hindernisse = Hindernisse(data["hindernisse"], 400, 200, spiel=self)
        self.spieler = Spieler(100, 500, 20, Farbe.white, self.win)
        
        #Fonts initialisieren
        self.font = pygame.font.SysFont("Arial", 50)

        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        pygame.key.set_repeat(10)
        
        
        self.data = data
        
        self.gegner_hinzufuegen()
        self.gewonnen = False
        self.RUN = True
        self.kills = 0
        self.level = 0

    def gegner_hinzufuegen(self):
        """Funktion fügt dem Spiel gegner hinzu. Ausgelesen aus dictionary.
        """
        from GBall_Normal import GBall_Normal
        from GBall_Two import GBall_Two
        from GBall_RNG import GBall_RNG
        from GBall__Verdoppler import GBall_Verdoppler
        from GBall_Shoot import GBall_Shoot

        #Im dic nach den Einträgen für gegner suchen und ins Level packen
        if "GBall_Normal" in self.data:
            for i in range(self.data["GBall_Normal"]["Anzahl"]):
                self.gegner += [GBall_Normal(self.data["GBall_Normal"]["geschwindigkeit"],self.win,self.hindernisse.hliste)]
        
        if "GBall_Two" in self.data:
            for i in range(self.data["GBall_Two"]["Anzahl"]):
                self.gegner += [GBall_Two(self.data["GBall_Two"]["geschwindigkeit"],self.win,self.hindernisse.hliste)]

        if "GBall_RNG" in self.data:
            for i in range(self.data["GBall_RNG"]["Anzahl"]):
                self.gegner += [GBall_RNG(self.data["GBall_RNG"]["geschwindigkeit"],self.win,self.hindernisse.hliste)]
        
        if "GBall_Verdoppler" in self.data:
            for i in range(self.data["GBall_Verdoppler"]["Anzahl"]):
                self.gegner += [GBall_Verdoppler(self.data["GBall_Verdoppler"]["geschwindigkeit"],self.win,self.hindernisse.hliste)]
        
        if "GBall_Shoot" in self.data:
            for i in range(self.data["GBall_Shoot"]["Anzahl"]):
                self.gegner += [GBall_Shoot(self.data["GBall_Shoot"]["geschwindigkeit"],self.win,self.hindernisse.hliste,self.spieler)]
        
    


  
    def schleife_bullets(self):
        """bewegt alle Kugeln
        """
        self.bullets_spieler.move(self.hindernisse.hliste)#
        self.bullets_gegner.move(self.hindernisse.hliste)

    def schleife_haupt(self):
        """Hauptschleife realisiert das Einzelspiel
        """
        
        self.start_sequenz()
        while self.RUN:
            self.schleife_malen()
            self.clock.tick(80)
            #Abläufe auf Threats verteilen und starten
            th1 = threading.Thread(target=self.schleife_bullets())
            th2 = threading.Thread(target=self.schleife_gegner())
            
            th1.start()
            th2.start()
            
            self.schleife_spieler()
            self.siegbedingung()

    def schleife_malen(self):
        """In dieser Methode werden alle Malvorgänge realisiert
        """
        self.win.blit(self.hintergrund,(0,0))
        self.hindernisse.malen()
        self.bullets_spieler.malen()
        self.bullets_gegner.malen()
        self.gegner_malen()
        self.spieler.malen()
        self.show_fps()
        self.show_level()
        self.show_kills()
        pygame.display.update()
        

    def gegner_alive(self):
        """Hier wird getestet ob die Gegnerischen Kugeln noch am Leben sind oder ob sie aus der Liste entfernt werden müssen
        """
        for i in self.gegner:
            i.trefferDetection(self.bullets_spieler.BulletList)

        for i in self.gegner:
            if not i.alive:
                self.kills += 1
                self.gegner.remove(i)


    



    def gegner_move(self):
        """In dieser Methode werden die gegnerischen Kugeln bewegt, und eventuell neue Kugeln der Liste hinzugefügt oder Schuesse abgefeuert
        """
        #Alle gegner Durchgehen
        for i in self.gegner:

            a = i.move(self.hindernisse.hliste)

            #Wenn Objekt zurückgegeben wird
            if a != None:

                if isinstance(a,list):
                    self.bullets_gegner.schiessen(i.xpos,i.ypos,a)
                else:
                    self.gegner +=[a]

    def gegner_malen(self):
        """in dieser Methode werden alle gegnerischen Kugeln gemalt
        """
        for i in self.gegner:
            i.malen()
    def schleife_gegner(self):
        """In dieser Methode werden alle Aktionen der gegnerischen Kugeln ausgeführt
        """
        self.gegner_alive()
        self.gegner_move()


    def schleife_spieler(self):
        """In dieser Methode werden alle Vorgänge für die Spieler_Kugel realisiert. 

        
        """
        self.keyinput()
        self.spieler_move()
        self.spieler_alive()



    def spieler_alive(self):
        """Methode überprüft ob die Spielerkugel noch am Leben ist

        Returns:
            boolean: ist der Spieler noch am Leben?
        """

        
        todesBall = self.spieler.trefferDetection(self.gegner+self.bullets_gegner.BulletList)
        
        if not self.spieler.alive and not self.spieler.godmode:
            self.spieler_sterben(todesBall)
            self.niederlagenachricht()
            self.RUN = False
        
    def spieler_sterben(self,todesBall):
        """Methode implementiert die Todes-Animation der Spieler Kugel

        Args:
            todesBall (Ball): Ball der für den Tod der Spielerkugel verantwortlich ist
        """
        
        #Blut erstellen. Richtungsvektor des Todesball verwenden
        blut = Blood(self.spieler.xpos,self.spieler.ypos,self.spieler.farbe,todesBall.richtung,50,self.win)
        #Sound abspielen
        Sound.smash.play()
        pygame.mixer.music.stop()

        #Schleife für die Blutanimation
        for i in range(50):
            self.clock.tick(60)
            self.win.blit(self.hintergrund,(0,0))
            blut.move()
            blut.malen()
            self.hindernisse.malen()
            self.gegner_malen()
            self.gegner_move()
            self.schleife_bullets()
            self.bullets_spieler.malen()
            pygame.display.update()
    

    def spieler_shoot(self):
        """Methode implementiert das Schießen des Spielers
        """
        self.bullets_spieler.schiessen(
                    self.spieler.xpos, self.spieler.ypos, self.spieler.richtung)
    
    
    def keyinput(self):
        """Methode implementiert die Steuerung der Spielerfigur
        """

        #Das event Array von Pygame durchgehen
        for event in pygame.event.get():
            #Wenn Fenster geschlossen wird
            if event.type == pygame.QUIT:
                main.Run=exit()

            #Wenn geschossen wird
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                self.spieler_shoot()

            #schauen welche Tasten gedrückt wurden
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.spieler.keys['left']=True
                elif event.key == pygame.K_RIGHT:
                    self.spieler.keys['right']=True
                elif event.key == pygame.K_UP:
                    self.spieler.keys['up']=True
                elif event.key == pygame.K_DOWN:
                    self.spieler.keys['down']=True
            
            #schauen welche Tasten losgelassen wurden
            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_RIGHT:
                    self.spieler.keys['right']=False
                elif event.key == pygame.K_UP:
                    self.spieler.keys['up']=False
                elif event.key == pygame.K_DOWN:
                    self.spieler.keys['down']=False
                elif event.key == pygame.K_LEFT:
                    self.spieler.keys['left']=False


    def spieler_move(self):
        """Methode realisiert die Spieler_Kugel Bewegung
        """
        alt_xpos=self.spieler.xpos
        alt_ypos=self.spieler.ypos

        #Spieler Bewegungsarray auslesen
        if self.spieler.keys['right']:
            self.spieler.xpos += 5
        if self.spieler.keys['up']:
            self.spieler.ypos -= 5
        if self.spieler.keys['down']:
            self.spieler.ypos += 5
        if self.spieler.keys['left']:
            self.spieler.xpos -= 5

        #Kollisionen abfragen
        xbool, ybool=self.spieler.collision_wand()

        if xbool:
            self.spieler.xpos=alt_xpos
        if ybool:
            self.spieler.ypos=alt_ypos

        collision=self.spieler.collision_gegensteande(self.hindernisse.hliste)

        if collision != None:

            if collision >= 3:
                self.spieler.xpos, self.spieler.ypos=alt_xpos, alt_ypos
            elif collision == 1:
                self.spieler.ypos=alt_ypos
            else:
                self.spieler.xpos=alt_xpos



    def show_fps(self):
        """Methode gibt die aktuellen Frames per Second aus

        
        """

        fps=str(int(self.clock.get_fps()))
        fps_text=self.font.render(fps, 1, pygame.Color("grey"))
        self.win.blit(fps_text, (50, 50))

    def show_kills(self):
        """Methode gibt die aktuellen kills aus

        
        """

        
        kills_text=self.font.render("Kills:  "+str(self.kills), 1, pygame.Color("white"))
        self.win.blit(kills_text, (600, 50))    

    def show_level(self):
        """Methode gibt das aktuelle lvl aus

        
        """

        
        lvl_text=self.font.render("lvl:  "+str(self.level), 1, pygame.Color("white"))
        self.win.blit(lvl_text, (1000, 50))    


    def start_sequenz(self):
        """Methode implementiert eine Startsequenz vor jedem Spiel
        """
        Uhr=pygame.time.Clock()
        
        #Zahlen als Bilder einlesen und ausgeben
        Zahlen = []
        Zahlen.append(pygame.image.load(os.path.join(self.sourceFileDir,"Bilder",'1.png')))
        Zahlen.append(pygame.image.load(os.path.join(self.sourceFileDir,"Bilder",'2.png')))
        Zahlen.append(pygame.image.load(os.path.join(self.sourceFileDir,"Bilder",'3.png')))

        #Zahlen nacheinander auf den Bilschirm blitten.
        for i in reversed(Zahlen):
            Sound.countdown.play()
            self.win.blit(self.hintergrund,(0,0))
            for j in self.gegner:
                j.malen()
            self.spieler.malen()
            self.hindernisse.malen()
            self.show_level()
            self.show_kills()
            self.win.blit(i,(500,400))
            pygame.display.update()
            Uhr.tick(1)

    def siegbedingung(self):
        """Methode gibt zurück ob das aktuelle Spiel gewonnen ist

        Returns:
            booelan: gewonnen?
        """
        if not self.gegner:
            self.siegnachricht()
            self.gewonnen = True
            self.RUN = False

    def siegnachricht(self):
        """Methode implementiert eine Siegesnachricht nach gewonnenem Spiel
        """
        gewonnen =pygame.image.load(os.path.join(self.sourceFileDir,"Bilder",'win.png'))
        Uhr=pygame.time.Clock()
        self.win.blit(self.hintergrund,(0,0))
        self.spieler.malen()
        self.hindernisse.malen()
        self.gegner_malen()
        self.show_level()
        self.show_kills()
        self.win.blit(gewonnen,(0,0))
        Sound.victory.play()
        Uhr.tick()
        pygame.display.update()
        Uhr.tick(1)

    def niederlagenachricht(self):
        """Methode implementiert eine Niederlage-Nachricht 
        """
        Uhr=pygame.time.Clock()
        verloren =pygame.image.load(os.path.join(self.sourceFileDir,"Bilder",'lost.png'))
        self.win.blit(self.hintergrund,(0,0))
        
        self.gegner_malen()
        self.hindernisse.malen()
        self.win.blit(verloren,(0,0))
        Sound.defeat.play()
        Uhr.tick()
        pygame.display.update()
        Uhr.tick(1)

    

    def randomcolor(self) -> tuple:
        """Methode gibt eine Zufallsfarbe zurück

        Returns:
            tuple: Farbe
        """
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Spiel(Test_Spiel):
    def __init__(self,run,data,win,godmode = False):
        """Konstruktor Spiel

        Args:
            run (run): das run Objekt
            data (dic): Level Daten
            win (ypgame.window): das Fenster
            godmode (bool, optional): Godmode. Defaults to False.
        """
        self.sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        self.data = data
        self.win = win
        self.clock = pygame.time.Clock()
        self.gegner = []
        self.bullets_spieler = Bullets(self.win)
        self.bullets_gegner = Bullets_Gegner(self.win)
        self.hindernisse = Hindernisse(data["hindernisse"], 400, 200, spiel=self)
        self.spieler = Spieler(100, 500, 20, Farbe.white, self.win)
        self.gegner_hinzufuegen()
        self.gewonnen = False
        self.aktrun = run
        self.RUN = True
        self.hintergrund = pygame.image.load(os.path.join(self.sourceFileDir,"Bilder",'Hintergrund_Spiel.png'))
        self.spieler.godmode = godmode
        self.font = pygame.font.SysFont("Arial", 50)
        self.kills = run.kills
        self.level = run.level
    
    def schleife_haupt(self):
        """Hauptschleife realisiert das Einzelspiel
        """
        
        self.start_sequenz()
        while self.RUN:
            self.schleife_malen()
            self.clock.tick(80)
            
            self.schleife_bullets()
            self.schleife_gegner()
            self.schleife_spieler()
            self.siegbedingung()
        return self.gewonnen
    def gegner_alive(self):
        """Hier wird getestest ob die Gegnerischen Kugeln noch am Leben sind oder ob sie aus der Liste entfernt werden müssen
        """
        for i in self.gegner:
            i.trefferDetection(self.bullets_spieler.BulletList)

        for i in self.gegner:
            if not i.alive:
                self.aktrun.kills += 1
                self.gegner.remove(i)
    def show_kills(self):
        """Methode gibt die aktuellen kills aus

        
        """

        
        kills_text=self.font.render("Kills:  "+str(self.aktrun.kills), 1, pygame.Color("white"))
        self.win.blit(kills_text, (600, 50)) 

class Survival_Spiel(Test_Spiel):

    def __init__(self):
        #Level Daten Erstellen
        data = {
            "level": 1,
            "hindernisse": 0,
            "GBall_Verdoppler": {
                "Anzahl": 1,
                "geschwindigkeit": 8
            }}
        self.time = 0
        super().__init__(data)

    def show_kills(self):
        """Methode verhindert das im Survival Modus kills angezeigt werden
        """
        
        pass
    
    def spieler_shoot(self):
        """Methode verhindert, dass der Spieler im Survival Modus schießen kann
        """
        pass
    
    def show_level(self):
        lvl_text=self.font.render("Sekunden überlebt:   %8.2f" %(self.time), 1, pygame.Color("white"))
        self.win.blit(lvl_text, (900, 50))   
    def schleife_haupt(self):
        """Hauptschleife realisiert das Survivalspiel
        """
        #Start Ticks
        start_ticks=pygame.time.get_ticks()
        self.start_sequenz()
        while self.RUN:
            #Anhand der Startticks vergangene Zeit berechnen
            self.time=(pygame.time.get_ticks()-start_ticks)/1000
            self.schleife_malen()
            self.clock.tick(80)
            
            self.schleife_gegner()
            
            
            
            
            self.schleife_spieler()
        return "%8.2f"%(self.time)
    def schleife_malen(self):
        """In dieser Methode werden alle Malvorgänge realisiert
        """
        self.win.blit(self.hintergrund,(0,0))
        self.hindernisse.malen()
        
        self.gegner_malen()
        self.spieler.malen()
        self.show_fps()
        self.show_level()
        
        pygame.display.update()       


#Kleine Testfunktion
def Spieltest():
    level_data = {
            "level": 1,
            "hindernisse": 2,
            "GBall_Normal": {
                "Anzahl": 10,
                "geschwindigkeit": 15
            }}

    spiel = Test_Spiel(level_data)
    spiel.schleife_haupt()




if __name__ == "__main__":
    Spieltest()
