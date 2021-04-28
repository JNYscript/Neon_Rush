import random
from GegnerBall import GegnerBall
from Farben import Farbe

class GBall_Normal(GegnerBall):

    def __init__(self,geschwindigkeit,window,hindernisse):

        super().__init__(random.randint(25,40),Farbe.cyan,random.randint(int(geschwindigkeit*0.75),geschwindigkeit),window,hindernisse)




def testgball():
    import Spiel
    level_data = {
            "level": 1,
            "hindernisse": 2,
            "GBall_Normal": {
                "Anzahl": 2,
                "geschwindigkeit": 5
            }
            }
    game = Spiel.Test_Spiel(level_data)
    game.schleife_haupt()

if __name__ == "__main__":
    testgball()