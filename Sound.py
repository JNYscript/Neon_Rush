import pygame,os

#Den Musik Mixer initalisieren
pygame.mixer.init()

soundlist = []
sourceFileDir = os.path.dirname(os.path.abspath(__file__))



#Sounds Laden und abspeichern
pygame.mixer.music.load(os.path.join(sourceFileDir,"Musik","menumusik.wav"))
klick = pygame.mixer.Sound(os.path.join(sourceFileDir,"Sound","klick.wav"))
smash = pygame.mixer.Sound(os.path.join(sourceFileDir,"Sound","smash.wav"))
laser = pygame.mixer.Sound(os.path.join(sourceFileDir,"Sound","laser.wav"))
victory = pygame.mixer.Sound(os.path.join(sourceFileDir,"Sound","victory.wav"))
defeat = pygame.mixer.Sound(os.path.join(sourceFileDir,"Sound","defeat.wav"))
countdown = pygame.mixer.Sound(os.path.join(sourceFileDir,"Sound","countdown.wav"))
soundlist.append(klick)
soundlist.append(smash)
soundlist.append(laser)
soundlist.append(victory)
soundlist.append(defeat)
#Grundlautstärke setzten
pygame.mixer.music.set_volume(0.3)
klick.set_volume(0.4)
smash.set_volume(1)
laser.set_volume(0.8)
victory.set_volume(1)


def volume_dec():
    """Methode verringert das Sound Volumen
    """
    clock = pygame.time.Clock()
    clock.tick()
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.1)
    for s in soundlist:
        s.set_volume(s.get_volume()-0.1)
    clock.tick(2)

def volume_inc():
    """Methode erhöht das Sound Volumen
    """
    clock = pygame.time.Clock()
    clock.tick()
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.1)
    for s in soundlist:
        s.set_volume(s.get_volume()+0.1)
    clock.tick(2)


