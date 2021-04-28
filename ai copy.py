import neat,os,pygame,Vektor,random,Button

from Spiel import Survival_Spiel
from Farben import Farbe
from Spieler import Spieler
from Hindernisse import Hindernisse
from GegnerBall import  GegnerBall

class AI(Spieler):
    
    def __init__(self, xpos, ypos, radius, farbe, window):


        super().__init__(xpos, ypos, radius, farbe, window)
        self.fitness = 0
        self.geschwindigkeit = 30
        self.wand_beruehrt = False
        self.next_enemy = None
        self.gegessen = False
        self.gegessen_besser = False
        self.next_enemy_besser =None
        self.fitness = 0
    
    def move_up(self):
        
        alt_ypos = self.ypos
        
        self.ypos -= self.geschwindigkeit
        if self.ypos - self.radius-10 < 0:
            self.ypos = alt_ypos 
            self.wand_beruehrt = True
    def move_down(self):
        
        alt_ypos = self.ypos
        
        self.ypos += self.geschwindigkeit
        if self.ypos + self.radius+10> 1000: 
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
        if self.xpos + self.radius +10 > 1500:
            self.xpos = alt_xpos 
            self.wand_beruehrt = True
    def abstand_wand(self):
        return [self.ypos,abs(self.ypos - 1000),self.xpos,abs(self.xpos - 1500)]

    def abstand_next(self,liste,besser):
        abstand_min = 3000
        for i in liste:
            abstand = Vektor.vektorleange(Vektor.vektsub([self.xpos,self.ypos],[i.xpos,i.ypos]))
            if abstand < abstand_min:
                abstand_min = abstand
                if besser:
                    self.next_enemy_besser = i
                else:
                    self.next_enemy = i
        
        return (self.xpos-self.next_enemy.xpos,self.ypos-self.next_enemy.ypos)
    
    def malen(self):

        pygame.draw.line(self.window,(0,0,0),(self.xpos,self.ypos),(self.next_enemy.xpos,self.next_enemy.ypos))
        pygame.draw.line(self.window,(0,0,255),(self.xpos,self.ypos),(self.next_enemy_besser.xpos,self.next_enemy_besser.ypos))
        pygame.draw.circle(self.window,self.farbe,(self.xpos,self.ypos),self.radius)

        
        
def main(genomes,config):
    
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    win = run.win
    font = pygame.font.SysFont("Arial", 50)
    clock = pygame.time.Clock()
    hintergrund = pygame.image.load(os.path.join(sourceFileDir,"Bilder",'Hintergrund_Ki.png'))
    
    
    
    
    
    
    
    
    
    pygame.key.set_repeat(10)
    
    
    



    
    
    zeit = 0


    max_fitness = 0
    
    for _,genome in genomes:
        net = neat.nn.RecurrentNetwork.create(genome, config)
        
        ai =  AI(random.randint(100,1400),random.randint(100,900),20,(255,255,255),win)
        genome.fitness = 0
        
        essen = []
        essen_besser = []

        RUN = True

        for i in range(10):
            essen += [GegnerBall(30,Farbe.green,0,win,[])]
    
        for i in range(4):
            essen_besser += [GegnerBall(30,Farbe.darkgreen,0,win,[])]

        ##################################################################################################################
     
        back_button = Button.button((0,0,0),50,50,130,130)
        start_ticks = pygame.time.get_ticks()
        ende = 0
        while RUN:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousepos = pygame.mouse.get_pos()
                    if back_button.isOver(mousepos):
                        ge[0].fitness = 10000


            ende += 1
            zeit =(pygame.time.get_ticks()-start_ticks)/1000

            

            if ai.gegessen:

                genome.fitness  += 1

                ai.gegessen = False

            if ai.gegessen_besser:

                genome.fitness  += 2

                ai.gegessen_besser = False
            
            #abstand_essen = ai.abstand_next(essen,False)
            #abstand_essen_besser = ai.abstand_next(essen_besser,True)
            #output = net.activate((abstand_essen[0],abstand_essen[1],abstand_essen_besser[0],abstand_essen_besser[1]))

            abstand_essen = ai.abstand_next(essen,False)
            abstand_essen_besser = ai.abstand_next(essen_besser,True)
            output = net.activate((ai.xpos,ai.ypos,ai.next_enemy.xpos,ai.next_enemy.ypos,ai.next_enemy_besser.xpos,ai.next_enemy_besser.ypos))

            if output[0] > 0.5:
                ai.move_up()
                
            if output[1] > 0.5:
                ai.move_down()
                
            if output[2] > 0.5:
                ai.move_left()
                
            if output[3] > 0.5:
                ai.move_right()
                    
                    
                


            for x,g in enumerate(essen):
                esser = g.trefferDetection([ai])
                if esser != None:
                    esser.gegessen = True
                    essen.pop(x)
            
            for x,g in enumerate(essen_besser):
                esser = g.trefferDetection([ai])
                if esser != None:
                    esser.gegessen_besser = True
                    essen_besser.pop(x)



                    
                
            
            if ende> 200:
                RUN = False
                break

            

            if max_fitness > 16 :
                
                

                win.blit(hintergrund,(0,0))

                ai.malen()

                for g in essen:
                
                    g.malen()
                
                for g in essen_besser:
                    g.malen()
                
                show_generation(font,win)
                show_time(font,zeit,win)
                
                pygame.display.update()
        
        
        if genome.fitness > max_fitness:
            max_fitness = genome.fitness
            print(f"max_fitness:{max_fitness}")
    
    run.gen += 1
    print(f"Generation:run.gen")
def show_time(font,zeit,win):
        time_text=font.render("Sekunden:%8.2f" % (zeit), 1, pygame.Color("white"))
        win.blit(time_text, (800, 50))   

def show_generation(font,win):
        time_text=font.render(f"Generation: {run.gen}", 1, pygame.Color("white"))
        win.blit(time_text, (400, 50))   
def run(config_file,win):
    run.win = win
    run.gen = 2
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    

    winner = p.run(main,500)
    

    





if __name__ == "__main__":
    pygame.init()
    WIN_WIDTH = 1500
    WIN_HEIGHT = 1000
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path,win)

    