from state import *
from Battler import Battler
from constants import *
#from player import *
import pygame, sys
from AnimEvents import *
#from pygame.locals import *
#import math
#import random
import pdb
 
MOVE_MAX = 15
# USEREVENT_PLAYERREADY = USEREVENT+1


class Message(object):
    def __init__(self, message, func, *args):
        self.message = message
        self.func = func
        self.args = args

    def call(self):
        if self.func is not None:
            if self.args:
                self.func(*self.args)
            else:
                self.func()


class CombatState(State):
    def __init__(self, screen, content, party, grounds, mobs, gamestate):
        super(CombatState, self).__init__(screen, content)

        self.party = party
        self.gamestate = gamestate

        self.cooltime = COOLTIME
        self.dt = 0

        self.textBox = pygame.Surface((236, 120))
        self.textBox.fill((0, 0, 255))

        self.portImage = pygame.image.load('gfx/player/portrait/joram.png')
        self.targetImage = pygame.image.load('gfx/cursor_red.png')
        self.cursorImage = pygame.image.load('gfx/cursor_white.png')
        self.isFinished = False
        '''
        self.textBoxImage = pygame.image.load('gfx/gui/textBox.png')
        self.textBoxImageInner = pygame.image.load('gfx/gui/textboxInner.png')
        self.textBox = pygame.Surface((236, 36))
        '''

        self.chatMode = False
        self.buffer = ""
        self.history = ["","",""]

        self.optionText = ['Attack', 'Magic', 'Defend', 'Item', 'Run']
        self.options = [self.content["font1"].render(text, True, WHITE) for text in self.optionText]
        self.current = 0
        self.currentAction = None
        self.animEvents = []
        self.messages = []
        # self.sideBar = pygame.Surface((160, 480))
        # self.sideBar.fill((135, 206, 250))

        #CHEAT
        self.cheat = 0
        for player in self.party.members:
            player.hp = player.maxHp

        self.playersToGo = []
        self.targetCoord = None
        self.mode = 0  # 0 menu, 1 waiting on event

        self.lhsPlayers = [Battler(self.content, mob, 1) for mob in mobs]
        self.rhsPlayers = [Battler(self.content, player, 0, True) for player in party.members]
        self.currentPlayer = -1
        self.currentTarget = 0

    def endTurn(self, char):
        self.playersToGo.remove(char)        
        print 'Finished with {0}\'s turn'.format(char.name)
                        
    # def initCombatRound(self):
        # print 'Starting new round'
        # self.playersToGo = self.findTurnOrder()
        # #~ print 'order for this round', self.playersToGo
        #
        # isPlayersLeft = False
        # for char in self.playersToGo:
        #     char.character.calcMods()
        #     char.active = True
        #     if not char.isPlayer: isPlayersLeft = True
        #
        # if not isPlayersLeft:
        #     print 'Battle over!'
        #     self.endCombat()
        
    def findTurnOrder(self):        
        chars = [char for char in self.lhsPlayers + self.rhsPlayers]
        chars = sorted(chars, key=lambda char: char.character.AGI + char.character.modAGI)
        
        return chars

    def endCombat(self):
        self.gamestate.pop()

    def draw(self):
        self.screen.fill(BLACK)

        for char in self.rhsPlayers + self.lhsPlayers:
            char.draw(self.screen, self.content)

            if char.isMyTurn:
                self.screen.blit(self.cursorImage, (char.rect.x, char.rect.y - 4))

                # if char.isPlayer and self.currentPlayer != -1 and self.mode == 0:
                if self.mode == 0:
                    char.drawCommands(self.screen, self.content, self.current)

        for event in self.animEvents:
            event.draw(self.screen)

        if self.mode == 2 and len(self.animEvents) == 0:  # Messages
            self.screen.blit(self.textBox, (self.screen.get_rect().centerx - 8, self.screen.get_rect().centery - 8))
            mesg = self.content["font1"].render(self.messages[0].message, True, WHITE)
            self.screen.blit(mesg, (self.screen.get_rect().centerx, self.screen.get_rect().centery))

    def keyreleased(self, key):
        super(CombatState, self).keyreleased(key)

    def letter(self, key):
        shift = False
        for i in xrange(len(self.keys)):
            if self.keys[i][0] == K_LSHIFT or self.keys[i][0] == K_RSHIFT or self.keys[i][0] == K_CAPSLOCK:
                shift = True
                break
        #if its a alpha numeric character    
        if (31 < key < 47) or (60 < key < 128) and len(self.buffer) < MAXTEXT:
            if shift:        
                self.buffer += chr(key).upper()
            else:
                self.buffer += chr(key)
       
        elif 46 < key < 60:
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
        if raw == '/hl':
            for player in self.party.members:
                player.hp = player.maxHp

        self.buffer = ""    
    
    def dispMessage(self, msg):
        self.history.append(msg)
        self.history.pop(0)

    def update(self, clock):
        super(CombatState, self).update(clock)

        if len(self.messages) == 0:
            # Update PCs
            for char in self.rhsPlayers:
                char.update()
                if char.active and self.currentPlayer == -1:
                    self.currentPlayer = self.rhsPlayers.index(char)
                    char.isMyTurn = True

            # Update enemies
            for char in self.lhsPlayers:
                char.update()
                if char.active:
                    choices = [player for player in self.rhsPlayers if player.character.hp > 0]
                    target = random.choice(choices)
                    print target.character.name

                    # target = self.rhsPlayers[0]
                    dmg, dCrit = char.attack(target, self.content)
                    char.events['attacking'].loadFunc(self.doDamage, dmg, target)
                    # dmgString = str(abs(dmg))
                    # if dmg == 0:
                    #     print 'Missed'
                    #     dmgString = 'Miss'
                    #
                    # char.didAction(1)
                    # if dmg > 0:
                    #     color = RED
                    # elif dmg == 0:
                    #     color = WHITE
                    # else:
                    #     color = GREEN

                    # event = TextEvent(self.content, dmgString, (target.rect.x, target.rect.y - 5), color)


                    # self.animEvents.append(event)

        for key in self.keysDown:
            self.keyHandler(key)

        for i in xrange(len(self.keys)):
            if self.check_cool(i):
                self.keyHandler(self.keys[i][0])

        for event in self.events:
            # print event.category + '!!!!!!!!!!!'
            if event.type == constants.USEREVENT_EVENT_TO_ADD:
                self.animEvents.append(event.payload)

        for event in self.animEvents:
            event.update()
            if event.count <= 0:
                self.animEvents.remove(event)

        # if self.mode == 1 and len(self.textEvents) == 0:
        #     self.mode = 0

        if len(self.lhsPlayers) == 0:
            self.beginFinish()

    def keyHandler(self, key):
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

        else:
            if key == K_ESCAPE or key == K_x:
                if self.mode == 1:
                    self.mode = 0
                    self.currentTarget = 0
                    self.currentAction = None
                    for char in self.lhsPlayers + self.rhsPlayers:
                        char.isTargeted = False
                else:
                    print self.mode
                    self.exit()

            elif key == K_z: self.doAction()
            elif key == K_LEFT: self.left()
            elif key == K_RIGHT: self.right()
            elif key == K_UP: self.up()
            elif key == K_DOWN: self.down()
            elif key == K_z: self.doAction()
            elif key == K_RETURN or key == K_KP_ENTER:
                self.chatMode = True

    def left(self):
        if self.mode == 0 and self.currentPlayer != -1:
            index = self.currentPlayer
            while 1:
                index -= 1
                if index == self.currentPlayer:
                    break
                elif index < 0:
                    index = len(self.rhsPlayers)
                else:
                    if self.rhsPlayers[index].active:
                        self.rhsPlayers[self.currentPlayer].isMyTurn = False
                        self.currentPlayer = index
                        self.rhsPlayers[index].isMyTurn = True
                        break

    def right(self):
        if self.mode == 0 and self.currentPlayer != -1:
            index = self.currentPlayer
            while 1:
                index += 1
                if index == self.currentPlayer:
                    break
                elif index >= len(self.rhsPlayers):
                    index = -1
                else:
                    if self.rhsPlayers[index].active:
                        self.rhsPlayers[self.currentPlayer].isMyTurn = False
                        self.currentPlayer = index
                        self.rhsPlayers[index].isMyTurn = True
                        break

    def down(self):
        if self.mode == 0 and self.currentPlayer != -1:
            self.current += 1
            if self.current >= len(self.rhsPlayers[self.currentPlayer].commands):
                self.current = 0

    def up(self):
        if self.mode == 0 and self.currentPlayer != -1:
            self.current -= 1
            if self.current < 0:
                self.current = len(self.rhsPlayers[self.currentPlayer].commands) - 1

    def doDamage(self, dmg, target):
        if target is not None:
            target.character.takeDamage(dmg)
            if target.character.hp <= 0:
                print target.character.name, 'defeated!'
                if not target.isPlayer:
                    self.lhsPlayers.remove(target)
                else:
                    target.waitTime = 0
                    target.active = False
                    target.isMyTurn = False
                    # if self.currentPlayer
                    if self.rhsPlayers[self.currentPlayer] is target:
                        self.mode = 0
                        self.currentPlayer = -1

                    isDefeated = True
                    for char in self.rhsPlayers:
                        if char.character.hp > 0:
                            isDefeated = False
                            break

                    if isDefeated:
                        mesg = 'Defeated!'
                        print(mesg)
                        self.mode = 2
                        self.messages.append(Message(mesg, self.finish))

    def doAction(self):
        if self.mode == 0 and self.currentPlayer != -1:
            if not self.currentAction:
                if self.current == 0:  # Attack
                    self.mode = 1
                    self.currentAction = 'attack'
                    self.lhsPlayers[self.current].isTargeted = True

        elif self.mode == 1:
            if self.currentAction == 'attack':
                target = self.lhsPlayers[self.current]
                dmg, dCrit = self.rhsPlayers[self.currentPlayer].attack(target, self.content)
                self.rhsPlayers[self.currentPlayer].events['attacking'].loadFunc(self.doDamage, dmg, target)
                # self.animEvents.append(event)
                self.currentPlayer = -1
                self.currentAction = None
                self.mode = 0

        elif self.mode == 2 and len(self.animEvents) == 0:
            if self.messages[0]:
                self.messages[0].call()

            self.messages.remove(self.messages[0])
            if len(self.messages) == 0:
                self.mode = 0

    def beginFinish(self):
        self.mode = 2
        # Do XP
        mesg = 'Victory!'
        self.messages.append(Message(mesg, self.finish))

    def finish(self):
        self.keys = []
        self.gamestate.pop()