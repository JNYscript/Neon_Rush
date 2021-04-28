#########################################
# main.py

#Die benötigten Module,Klassen importieren
import operator,csv,Sound,pygame,os,ai
from Button import button
from Run import Run
from Spiel import Survival_Spiel,Test_Spiel

def main():
    """Die Methode startet das Programm und Initalisiert Pygame 
    """

    os.environ['SDL_VIDEO_CENTERED'] = '1' #Versuchen das Fenster zu zentrieren
    pygame.init()   #Pygame Initialisieren
    pygame.mixer.init() #Pygames Sound Mixer initalisieren
    WIN_WIDTH = 1500 #Fensterbreite
    WIN_HEIGHT = 1000 #Fensterhöhe
    main.font = pygame.font.SysFont("Comic Sans", 60) #Initalisieren der Schriftart Comic Sans
    main.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) #Das Ausgabe Fenster definieren
    main.godmode = False #Variable für den Godmode des Spielers
    
    menu() #Menu methode aufrufen
    
    


def menu():
    """Diese Methode realisiert das Hauptmenu. Sie überprüft ob ein button geklickt wurde und führt die entsprechende Methode aus
    """
    #Hintergrund Bild von Datei laden
    hintergrund = pygame.image.load(
        os.path.join(sourceFileDir, "Bilder", "menu.png"))
    #Eine Pygame Clock erstellen
    clock = pygame.time.Clock()

    menu_init() # Menu initialisieren

    main.buttonlist = [] #Liste für alle Buttons
    buttons() #benötigte Buttons erstellen
    
    menu.RUN = True #ob die Hauptschleife weiter laufen soll

    
    pygame.display.update() # Display updaten um Veräderungen anzuzeigen


    #In dieser Schleife wird auf user Input gewartet und dann die entsprechende Aktion ausgeführt
    while menu.RUN:


        clock.tick(30)# Für besseres Frametiming

        for event in pygame.event.get():
            #Falls beendet wird
            if event.type == pygame.QUIT:
                return

        #falls Mouseklick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousepos = pygame.mouse.get_pos()
            if main.buttonlist[0].isOver(mousepos):

                Sound.volume_inc()

            elif main.buttonlist[1].isOver(mousepos):

                Sound.volume_dec()

            elif main.buttonlist[2].isOver(mousepos):

                start()
                menu_init()

            elif main.buttonlist[3].isOver(mousepos):
                AI()
                menu_init()
            elif main.buttonlist[4].isOver(mousepos):

                survival()
                menu_init()
                clock.tick()
                clock.tick(5)
            elif main.buttonlist[5].isOver(mousepos):

                highscore()
                main.win.blit(hintergrund, (0, 0))
                pygame.display.update()

            elif main.buttonlist[6].isOver(mousepos):
                main.godmode = True

                print(6)
            elif main.buttonlist[7].isOver(mousepos):
                lvl()
                menu_init()


def menu_init():
    """initalisiert das Hauptmenu(Musik,Hintergrundbild...)
    """
    #Mousecurser ädnern
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pygame.mixer.music.stop() #Musik Stoppen
    pygame.mixer.music.load(os.path.join(
        sourceFileDir, "Musik", "menumusik.wav")) #Musik Laden

    
    hintergrund = pygame.image.load(
        os.path.join(sourceFileDir, "Bilder", "menu.png"))
    main.win.blit(hintergrund, (0, 0)) #Hintergrundbild auf das Fenster zeichnen
    pygame.mixer.music.play(-1) #Musik im Endlosmodus spielen
    pygame.display.update()

def buttons():
    """Erstellt alle Buttons für das Hauptmenu
    """
    #Buttons hinzufügen
    main.buttonlist.append(button((0, 0, 0), 40, 480, 200, 150))
    main.buttonlist.append(button((0, 0, 0), 40, 750, 200, 150))
    main.buttonlist.append(button((0, 0, 0), 450, 380, 370, 150))
    main.buttonlist.append(button((0, 0, 0), 400, 720, 270, 150))
    main.buttonlist.append(button((0, 0, 0), 1000, 400, 350, 230))
    main.buttonlist.append(button((0, 0, 0), 1000, 720, 350, 230))
    main.buttonlist.append(button((0, 0, 0), 0, 0, 100, 100))
    main.buttonlist.append(button((0, 0, 0), 750, 600, 240, 150))

def start():
    """Startet ein normales Spiel
    """

    run = Run(main.win, godmode=main.godmode) #Erstelle ein Run Objekt
    
    erglvl, ergkills = run.run() #Spiel starten
    normal_submit(str(erglvl), str(ergkills)) #Highscore eingabe 

def normal_submit(level, kills):
    """In dieser Methode wird die Highscore Eingabe für das normale Spiel realisiert

    Args:
        level (string): Anzahl der Level
        kills (string): Anzahl der Kills
    """

    #kurz warten
    pygame.time.wait(200)
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    clock = pygame.time.Clock()

    hintergrund = pygame.image.load(os.path.join(
        sourceFileDir, "Bilder", "submit_normal.png"))
    
    #Buttons erstellen
    back_button = button((255, 255, 255), 1330, 20, 120, 120)
    submit_button = button((255, 255, 255), 500, 300, 450, 180)
    #Text erstellen
    text = "..Name.."
    text_level = main.font.render(level, 12, (0, 0, 0))
    text_kills = main.font.render(kills, 12, (0, 0, 0))

    run = True
    clock.tick()
    #Diese schleife ermöglicht Userinput in ein Feld indem gecheckt wird welche Tasten gedrückt werden
    for event in pygame.event.get():
        pass
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                #zum Abschicken
                if back_button.isOver(mousepos):

                    return
                elif submit_button.isOver(mousepos):
                    #in Tabellen Datei laden
                    tabelle_schreiben("highscore_normal.csv",
                                      ""+"\n"+text+","+level+","+kills)
                    return
            elif event.type == pygame.KEYDOWN:
                
                #für Text löschen
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            #Elemente darstellen
            main.win.blit(hintergrund, (0, 0))
            text_surf = main.font.render(text, 12, (0, 0, 0))
            main.win.blit(text_surf, (300, 700))
            main.win.blit(text_level, (650, 700))
            main.win.blit(text_kills, (1000, 700))
            pygame.display.update()


def tabelle_schreiben(tabelle, inhalt):
    """Methode schreibt Daten ans Ende einer Datei

    Args:
        tabelle (string): Pfad zu Datei
        inhalt (string): Inhalt der geschrieben werden soll
    """
    with open(tabelle, 'a') as file:
        file.write(inhalt)
def AI():
    """Startet die AI Funktion
    """

    #Schauen ob das Modul NEAT-python vorhanden ist
    try:
        import neat
    except ModuleNotFoundError :
        return


    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(
        sourceFileDir, "Musik", "MelloC-Numesy.wav"))
    pygame.mixer.music.play(-1)
    #AI Starten
    ai.run(os.path.join(sourceFileDir, "config-feedforward.txt"),main.win)



def tabelle_malen(x, y, datei,type):
    """malt eine Tabelle auf das Fenster

    Args:
        x (int): x Koordinate 
        y (int): y Koordinate
        datei (str): Pfad  
        type (type): Datentyp nach dem sortiert werden soll
    """
    tabelle = []

    #Datei öffnen
    with open(datei, "r") as datei:

        csv1 = list(csv.reader(datei))

        for row in csv1:
            row[1] = type(row[1])

        #Sortieren
        sortcsv = sorted(csv1, key=lambda r: r[1], reverse=True)
        i = 1
        #DAten in Zeile einlesen
        for row in sortcsv:
            tabelle += [str(i)+"     "+row[0]+"  "*(10-len(row[0])) +
                        str(row[1])+"  "*(5-len(str(row[1])))+str(row[2])]
            i += 1
            if i >= 7:
                break

    rendert = []
    #Als Text rendern
    for row in tabelle:
        rendert += [main.font.render(row, 40, pygame.Color("black"))]

    k = y
    #Auf Fenster malen
    for row in rendert:
        main.win.blit(row, (x, k))
        k += 70


def highscore():
    """Realisiert das Highscore Fenster mit den zwei Tabellen
    """
    #Hintergrund Laden
    hintergrund = pygame.image.load(os.path.join(
        sourceFileDir, "Bilder", "highscore.png"))
    main.win.blit(hintergrund, (0, 0))

    back_button = button((255, 255, 255), 1330, 20, 120, 120)
    #Tabellen Malen
    tabelle_malen(160, 480, "highscore_normal.csv",int)
    tabelle_malen(1000, 480, "highscore_survival.csv",float)
    pygame.display.update()
    #Schauen ob der USer zurück möchte
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                if back_button.isOver(mousepos):

                    return


def survival():
    """Startet das Survival Spiel
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(
        sourceFileDir, "Musik", "Wake-Steppin.wav"))
    pygame.mixer.music.play(-1)
    game = Survival_Spiel() #Survival Spiel Objekt erstellen


    survival_submit(game.schleife_haupt()) #Spielstart und Highscore Eingabe


def survival_submit(zeit):
    """Realisiert die Highscore Eingabe für das Survival Spiel

    Args:
        zeit (str): überlebte Zeit
    """


    #ist ähnlich wie die normal_submit Methode aber anderer Hintergrund und Aktionen und darzustellender Text
    pygame.time.wait(200)
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    clock = pygame.time.Clock()

    hintergrund = pygame.image.load(os.path.join(
        sourceFileDir, "Bilder", "submit_survival.png"))
    back_button = button((255, 255, 255), 1330, 20, 120, 120)
    submit_button = button((255, 255, 255), 500, 300, 450, 180)
    text = "Name.."
    text_zeit = main.font.render(zeit+"  Sekunden", 12, (0, 0, 0))

    run = True
    clock.tick()
    clock.tick(5)
    for event in pygame.event.get():
        pass
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                if back_button.isOver(mousepos):

                    return
                elif submit_button.isOver(mousepos):
                    tabelle_schreiben("highscore_survival.csv",
                                      ""+"\n"+text+","+zeit+", ")
                    return
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            main.win.blit(hintergrund, (0, 0))
            text_surf = main.font.render(text, 12, (0, 0, 0))
            main.win.blit(text_surf, (300, 700))
            main.win.blit(text_zeit, (600, 700))

            pygame.display.update()

def lvl_menu(buttonlist, werte, hintergrund):
    """Hier wird das LVL Editor Menu dargestellt und die Usereingaben erfasst

    Args:
        buttonlist ([button]): die zu darstellenden Buttons
        werte (int[]): Array mit werten die verändert werden sollen
        hintergrund (picture): Bild das im Hintergrund angezeigt werden soll

    Returns:
        [bool]: ob der spieler weiter gedrückt hat oder zurück
    """
    hintergrund = pygame.image.load(
        os.path.join(sourceFileDir, "Bilder", hintergrund))
    back_button = button((255, 255, 255), 1330, 20, 120, 120)
    weiter_button = button((0, 0, 0), 888, 90, 312, 130)
    xwerte = [190, 525, 757, 1050, 1310]
    clock = pygame.time.Clock()

    #In dieser Schleife wird überprüft, ob der Spieler auf einen der Plus oder Minus Buttons gedrück hat und der entsprechende Wert im Array geändert
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousepos = pygame.mouse.get_pos()
                if weiter_button.isOver(mousepos):
                    return True

                if back_button.isOver(mousepos):

                    return False
                #Checken welcher Button gedrückt wurde
                for i in range(len(buttonlist)):
                    if buttonlist[i][0].isOver(mousepos):
                        werte[i] += 1
                        if werte[i] > 20:
                            werte[i] = 20
                    elif buttonlist[i][1].isOver(mousepos):
                        werte[i] -= 1
                        if werte[i] < 0:
                            werte[i] = 0
        main.win.blit(hintergrund, (0, 0))

        #Die aktuellen Werte darstellen
        for i in range(len(werte)):
            text = main.font.render(str(werte[i]), 30, (0, 0, 0))
            main.win.blit(text, (xwerte[i], 370))
        pygame.display.update()




def lvl():
    """Realisiert die Level_Editor Funktion. 
    """

    #Benötigte Buttons
    Buttons = []
    werte_anzahl = []
    werte_geschwindigkeit = []
    x = 160
    #Buttons erstellen
    for i in range(5):
        b = []

        y = 570
        for i in range(2):
            b += [button((0, 0, 0), x, y, 100, 100)]
            y += 170

        Buttons += [b]
        x += 295
    for i in range(5):
        werte_anzahl += [0]
        werte_geschwindigkeit += [0]
    #Feintuning mancher Buttons
    Buttons[4][0].x -= 60
    Buttons[4][1].x -= 60
    Buttons[3][0].x -= 20
    Buttons[3][1].x -= 20

    #Usereingabe in Dic umwandeln um dann ein LVL mit den Spezifikationen erstellen zu können
    if lvl_menu(Buttons, werte_anzahl, "lvl_anzahl.png") and lvl_menu(Buttons, werte_geschwindigkeit, "lvl_geschwindigkeit.png"):

        data = {
            "level": 0,
            "hindernisse": 3,

            "GBall_Normal": {
                "Anzahl": werte_anzahl[0],
                "geschwindigkeit": werte_geschwindigkeit[0]
            },
            "GBall_Two": {
                "Anzahl": werte_anzahl[1],
                "geschwindigkeit": werte_geschwindigkeit[1]
            },
            "GBall_RNG": {
                "Anzahl": werte_anzahl[2],
                "geschwindigkeit": werte_geschwindigkeit[2]
            },
            "GBall_Verdoppler": {
                "Anzahl": werte_anzahl[3],
                "geschwindigkeit": werte_geschwindigkeit[3]
            },
            "GBall_Shoot": {
                "Anzahl": werte_anzahl[4],
                "geschwindigkeit": werte_geschwindigkeit[4]
            }

        }

        #Spiel starten
        game = Test_Spiel(data)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(sourceFileDir,"Musik","Decktonic - Night Drive (Strong Suit Remix).wav"))
        
        pygame.mixer.music.play(-1)
        game.schleife_haupt()







if __name__ == "__main__":
    sourceFileDir = os.path.dirname(os.path.abspath(__file__)) #Pfad in welchem das Spiel ausgeführt wird

    main()
