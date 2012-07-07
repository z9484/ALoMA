from state import *
import pygame, sys
from pygame.locals import *
from constants import *
import cPickle as pickle
from Map import Map

from player import *
#from bmpfont import *
#from combatstate import CombatState
 
class GameState(State):
    def __init__(self, screen, content, player, gamestate):
        super(GameState, self).__init__(screen, content)

        self.player1 = player

        self.map1 = Map(self.player1.map)
        self.gamestate = gamestate
                
        self.cooltime = COOLTIME
        
        self.dt  = 0
        self.view = self.findView(self.player1.posX, self.player1.posY)
        self.buffer = ""
        self.history = ["","",""]
        #self.font =  BmpFont()
        
        self.chatMode = False
        self.targetMode = False
        self.currentTarget = 0
        '''
        self.textBoxImage = pygame.image.load('gfx/gui/textBox.png')
        self.textBoxImageInner = pygame.image.load('gfx/gui/textboxInner.png')
        self.textBox = pygame.Surface((236, 36))
        '''
        self.sideBar = pygame.Surface((160, 480))
        self.sideBar.fill((135, 206, 250))        
        
        self.cheat = 0

    def isNpcBlocking(self, x, y):
        isBlocked = False
        for i in range(len(self.map1.monsters)):
            if self.map1.monsters[i].posX == x and self.map1.monsters[i].posY == y:
                isBlocked = True
                break
                
        return isBlocked
    
    def draw(self):
        self.screen.fill(BLACK)
        for y in xrange(15):
            for x in xrange(15):
                for i in range(2):
                    try:        
                        if isinstance(self.view[y][x][i], pygame.Surface):
                            self.view[y][x][i].set_colorkey(constants.COLORKEY)
                            self.screen.blit(self.view[y][x][i], (x*TILESIZE, y*TILESIZE) )
                            
                    except:
                        pass    

        self.player1.draw(self.screen)
        
        for i in range(len(self.map1.monsters)):
            self.map1.monsters[i].draw(self.screen, self.player1.posX, self.player1.posY)
        
        #self.screen.blit(self.content['moveTile'], (7*TILESIZE, 6*TILESIZE) )
        """
        for y in xrange(15):
            for x in xrange(15):
                try:
                    if isinstance(self.view[y][x][1], pygame.Surface):
                         self.screen.blit(pygame.transform.scale(self.view[y][x][1], (32, 32)), (x*TILESIZE, y*TILESIZE) )
                except:
                    pass    
        """         
        text = self.content["font1"].render("X:" + str(self.player1.posX) + " Y:" + str(self.player1.posY), True, WHITE)   
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery))
        
        text = self.content["font1"].render("name: {0}".format(self.player1.name), True, WHITE)   
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+15))
        
        text = self.content["font1"].render("Gold: {0}".format(self.player1.gold), True, WHITE)   
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+30))
        
        text = self.content["font1"].render(self.buffer, True, WHITE)  
        self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+150))
        
        for i in xrange(len(self.history)):
            text = self.content["font1"].render(self.history[i], True, GRAY)  
            self.screen.blit(text, (self.screen.get_rect().centerx, self.screen.get_rect().centery+90+20*i))

        #self.font.blit('0123', self.screen, (32, 2))
        
        '''
        #self.textBox.blit((0,0))
        self.screen.blit(self.textBoxImage, (0,0))
        self.textBox.blit(self.textBoxImageInner, (0,0))
        self.font.blit('BAD TO THE BONE CHARMANDER EAT PIZZA ice cold', self.textBox, (0, 0))
        '''
        #self.screen.blit(self.textBox, (8,5))
        self.screen.blit(self.sideBar, (480,0))

       
    
    def player_left(self):
        if self.cheat:
            self.player1.moveLeft()
        else:
            if not isinstance(self.view[7][6][2], pygame.Surface) and not self.isNpcBlocking(self.player1.posX - 1, self.player1.posY):
                self.player1.moveLeft()

    def player_right(self):
        if self.cheat:
            self.player1.moveRight()
        else:
            if not isinstance(self.view[7][8][2], pygame.Surface) and not self.isNpcBlocking(self.player1.posX + 1, self.player1.posY):
                self.player1.moveRight()
        
    def player_up(self):
        if self.cheat:
            self.player1.moveUp()
        else:
            if not isinstance(self.view[6][7][2], pygame.Surface) and not self.isNpcBlocking(self.player1.posX, self.player1.posY - 1):
                self.player1.moveUp()
        
    def player_down(self):
        if self.cheat:
            self.player1.moveDown()
        else:
            if not isinstance(self.view[8][7][2], pygame.Surface) and not self.isNpcBlocking(self.player1.posX, self.player1.posY + 1):
            #if not isinstance(self.view[8][7][7], pygame.Surface) and not isinstance(self.view[8][7][8], pygame.Surface):
                self.player1.moveDown()
        
    def keyreleased(self, key):
        super(GameState, self).keyreleased(key) 

    def move(self, direction):
        if direction == "up":
            self.player_up()
        elif direction == "down":
            self.player_down()
        elif direction == "left":
            self.player_left()
        elif direction == "right":
            self.player_right()

        self.view = self.findView(self.player1.posX, self.player1.posY)
        #if (self.player1.posX, self.player1.posY) in self.map1.events:
            #if self.map1.events[(self.player1.posX, self.player1.posY)][0] == 0:
                #self.changemap(self.map1.events[(self.player1.posX, self.player1.posY)][2], self.map1.events[(self.player1.posX, self.player1.posY)][1])

        #Check for events
        if self.map1.events[self.player1.posY][self.player1.posX] != 0:
            event = self.map1.events[self.player1.posY][self.player1.posX]
            if event.type == 'warp':
                self.changemap(event.map, (int(event.destX), int(event.destY)))

    def changemap(self, newMap, position):
        #if self.player1.
        self.player1.posX = position[0]
        self.player1.posY = position[1]
        if newMap != '':
            self.player1.map = newMap
            self.map1 = Map(newMap)
        self.move('Nowhere')
        
    def letter(self, key):
        #if self.currentCommand != -1:
        shift = False
        for i in xrange(len(self.keys)):
            if self.keys[i][0] == K_LSHIFT or self.keys[i][0] == K_RSHIFT or self.keys[i][0] == K_CAPSLOCK:
                shift = True
                break
        #if its a alpha numeric character    
        if (key > 31 and key < 47) or (key > 60 and key < 128) and len(self.buffer) < MAXTEXT:
            if shift:        
                self.buffer += chr(key).upper()
            else:
                self.buffer += chr(key)
       
        elif key > 46 and key < 60:
            if not shift:
                self.buffer += chr(key)
            else:
                if key == K_1:
                    character = chr(K_EXCLAIM) 
                elif key == K_2:
                    character = chr(K_AT)
                elif key == K_3:
                    character = chr(K_HASH)
                elif key == K_4:
                    character = chr(K_DOLLAR)
                elif key == K_5:
                    character = chr(37)
                elif key == K_6:
                    character = chr(K_CARET)
                elif key == K_7:
                    character = chr(K_AMPERSAND)
                elif key == K_8:
                    character = chr(K_ASTERISK)
                elif key == K_9:
                    character = chr(K_LEFTPAREN)
                elif key == K_0:
                    character = chr(K_RIGHTPAREN)
                elif key == K_SLASH:
                    character = chr(K_QUESTION)
                elif key == K_SEMICOLON:
                    character = chr(K_COLON)
                else:
                    character = chr(key)
                    
                self.buffer += character
                
                
    def backspace(self):
        self.buffer = self.buffer[:-1]
        
    def enter(self):
        raw = self.buffer.strip()
        if raw == "":
            self.chatMode = False
            return
            
        self.dispMessage(self.buffer)
        if raw == 'p':
            for poke in self.player1.party:
                print poke.name, poke.level, poke.ability
        elif raw == 'pc':
            self.player1.visitPokecenter()
            
        self.buffer = ""    
    
    def dispMessage(self, msg):
        self.history.append(msg)
        self.history.pop(0)
        
    def update(self, clock):
        super(GameState, self).update(clock) 
        
        for key in self.keysDown:
            self.keyHandler(key)

        for i in xrange(len(self.keys)):
            if self.check_cool(i):
                self.keyHandler(self.keys[i][0])
            
        
    def keyHandler(self, key):
        if key == K_ESCAPE: self.exit()
        
        if self.targetMode:
            if key == K_LEFT: 
                self.map1.monsters[self.currentTarget].isTargeted = False
                self.currentTarget -= 1
                if self.currentTarget == -1:
                    self.currentTarget = len(self.map1.monsters) - 1
                    
                self.map1.monsters[self.currentTarget].isTargeted = True
                                
            elif key == K_RIGHT:
                self.map1.monsters[self.currentTarget].isTargeted = False
                self.currentTarget += 1
                if self.currentTarget == len(self.map1.monsters):
                    self.currentTarget = 0
                    
                self.map1.monsters[self.currentTarget].isTargeted = True
                
            elif key == K_LCTRL:
                self.targetMode = False
                self.map1.monsters[self.currentTarget].isTargeted = False
                dmg, dCrit = self.player1.attack(self.map1.monsters[self.currentTarget], self.player1.isMelee)
                if dmg == -1:
                    print 'Missed'
                
                if self.map1.monsters[self.currentTarget].hp == 0:
                    print 'Monster defeated!'
                    self.map1.monsters.remove(self.map1.monsters[self.currentTarget])
                    
            #Switch from monsters to players or npcs?
            #elif key == K_UP: self.move("up")
            #elif key == K_DOWN: self.move("down")
        else:
            if key == K_LEFT: self.move("left")
            elif key == K_RIGHT: self.move("right")
            elif key == K_UP: self.move("up")
            elif key == K_DOWN: self.move("down")
            #elif key == K_g: self.cmd_g()
            elif key == K_TAB:
                self.targetMode = True
                self.map1.monsters[self.currentTarget].isTargeted = True
                
        
        if self.chatMode:
            if key == K_KP0: self.letter(K_0)
            elif key == K_KP1: self.letter(K_1)
            elif key == K_KP2: self.letter(K_2)
            elif key == K_KP3: self.letter(K_3)
            elif key == K_KP4: self.letter(K_4)
            elif key == K_KP5: self.letter(K_5)
            elif key == K_KP6: self.letter(K_6)
            elif key == K_KP7: self.letter(K_7)
            elif key == K_KP8: self.letter(K_8)
            elif key == K_KP9: self.letter(K_9)
            elif key == K_RETURN or key == K_KP_ENTER: self.enter()
            elif key == K_BACKSPACE: self.backspace()
            elif key == K_SPACE: self.letter(key)
            else: self.letter(key)
        elif key == K_RETURN or key == K_KP_ENTER:
            self.chatMode = True
            
         
    def findView(self, x,y):
        view = []
        for q in xrange(-7,8):
            row = []
            for r in xrange(-7,8):
                if y+q >= self.map1.tiled.height or x+r >= self.map1.tiled.width or y+q < 0 or x+r < 0:
                    row.append('^')
                else:
                    #try:
                        #row.append(self.map[y+q][x+r])
                    layers = [self.map1.tiled.getTileImage(x+r, y+q, i) for i in range(3)]
                    row.append(layers)
                        
                    #except:
                    #    row.append("v")
                        #print 'bad terrain', y+q, x+r
            view.append(row)  

        return view        
        
        
    def exit(self):
        self.player1.save()
        storage = self.player1
        with open("player.dat", 'w') as file: 
            pickle.dump(storage, file)
        sys.exit(0)

