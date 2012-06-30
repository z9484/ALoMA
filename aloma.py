import pygame, sys
from pygame.locals import *
from player import *
import random
from states.gamestate import *
#from states.combatstate import *
import constants

class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))#, pygame.FULLSCREEN)
        pygame.display.set_caption("ALoMA")
        self.clock = pygame.time.Clock()

        ## Load Content ## try static
        pygame.font.init()
        font = pygame.font.Font(None, 20)

        self.tiles = {}
        self.tiles["monsters"] = [pygame.image.load('gfx/monsters/animals/black_snake.bmp'),
            pygame.image.load('gfx/monsters/animals/gray_rat.bmp')]
        
        for i in xrange(len(self.tiles["monsters"])):
            self.tiles["monsters"][i].set_colorkey((71,108,108))
            
            
        chars = pygame.image.load('gfx/Joram_bow.png')
        
        self.tiles["targetCursor"] = pygame.image.load('gfx/cursor_red.png')
        #self.tiles["moveTile"] = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        #self.tiles["moveTile"].fill((0,0,0))    
        #self.tiles["moveTile"].set_alpha(15)
        self.tiles["font1"] = font
        
  
        try:
            with open("player.dat", 'r') as file: 
                storage = pickle.load(file)
                player1 = storage
                player1.load(chars)
        except:
            print "Creating new player"
            player1 = Player("Joram", MALE, 'human', chars)

        
        self.currentState = 0
        self.gamestate = []
        self.gamestate.append(GameState(self.screen, self.tiles, player1, self.gamestate))
        #CombatState(self.screen, self.tiles, player1,self.gamestate )]
        
        #self.gamestate = GameState(self.screen, self.tiles, player1)
        #self.gamestate = CombatState(self.screen, self.tiles)


    def update(self):
        # USER INPUT
        self.clock.tick(FRAMES_PER_SECOND)
        self.gamestate[-1].update(self.clock)    
        
    def draw(self):
        self.gamestate[-1].draw()
        pygame.display.flip()


    def run(self):
        while 1:
            self.update()
            self.draw()


game = Game()
game.run()