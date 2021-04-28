#Module importieren

import json,pygame,os,Sound
from Spiel import Spiel
class Run:

    def __init__(self,win,maxlvl = 14,godmode = False):
        """Konstruktor Run Objekt

        Args:
            win (pygame.window): Das Fenster
            maxlvl (int, optional): Maximales Level. Defaults to 14.
            godmode (bool, optional): Soll der Godmode aktiviert sein. Defaults to False.
        """

        self.win = win
        self.data = {}
        #Level Daten aus Datei einlesen
        with open("level.json","r") as _input:
            self.data = json.load(_input)
        self.level = 0
        self.kills = 0
        self.maxlvl = maxlvl
        self.sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        self.godmode = godmode
        

    def run(self):
        """Diese Methode implementiert den ganzen Spielablauf. Dazu werden die Leveldaten aus die ersten 25 Level aus der level.json Datei eingelesen. 
        Ab level 26 wird  dann das Level 25 immer schwerer gemacht.
          

        Returns:
            [Tuple]: erreichtes Level, Kills
        """
        #Level Musik starten
        pygame.mixer.music.stop()
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        pygame.key.set_repeat(10)
        pygame.mixer.music.load(os.path.join(self.sourceFileDir,"Musik","Decktonic - Night Drive (Strong Suit Remix).wav"))
        
        pygame.mixer.music.play(-1)
        
        #Level Daten aus Datei einlesen
        for i in range(25):
            
            self.level += 1 
            spiel = Spiel(self,self.data["levels"][self.level-1],self.win,godmode= self.godmode)
            #Wenn der Spieler das Level nicht geschafft haben sollte
            if not spiel.schleife_haupt():
                return self.level, self.kills
        
        geschwindigkeit = 10

        #Grundlevel erstellen
        lvl_data = {
        
            "level": self.level,
            "hindernisse": 2,
            
            "GBall_Shoot": {
                "Anzahl": 2,
                "geschwindigkeit": geschwindigkeit
            },
            "GBall_Normal": {
                "Anzahl": 2,
                "geschwindigkeit": geschwindigkeit
            },
            "GBall_Verdoppler": {
                "Anzahl": 3,
                "geschwindigkeit": geschwindigkeit
            },
            "GBall_RNG": {
                "Anzahl": 4,
                "geschwindigkeit": geschwindigkeit
            },
            "GBall_Two": {
                "Anzahl": 3,
                "geschwindigkeit": geschwindigkeit
            }
            
        }
        #Level immer schwerer machen
        for k in range(self.maxlvl):


            self.level += 1
            geschwindigkeit += 1
            spiel = Spiel(self,lvl_data,self.win,godmode= self.godmode)
            if not spiel.schleife_haupt():
                return self.level, self.kills
            
    



#Kleine Testfunktion
def testrun():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    WIN_WIDTH = 1500
    WIN_HEIGHT = 1000
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    run = Run(win)
    run.run()

if __name__ =="__main__":
    testrun()