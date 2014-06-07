# import pygame
import constants
from AnimEvents import *


class Battler(object):
    def __init__(self, content, character, side, isPlayer=False):
        self.character = character
        self.isPlayer = isPlayer
        self.isMyTurn = False
        self.isTargeted = False
        self.anim_state = ''
        self.events = {}  # Current animation events currently affecting the battler

        if isPlayer:
            rate = constants.random.randrange(45, 95) * .01
        else:
            rate = constants.random.randrange(0, 95) * .01

        self.waitTime = int(self.__getMaxWait() * rate)
        self.active = False
        self.side = side

        self.isBackRow = character.isBackRow
        self.rect = self.character.images[0].get_rect()

        self.rect.x = 32
        if self.isBackRow:
            self.rect.x += 40

        if self.side == 1:
            self.rect.x += 200

        self.rect.y = 60 + self.character.partyPosition * 32

        if self.isPlayer:
            self.spdBarBack = constants.pygame.Surface((32, 6))
            self.spdBarBack.fill((0, 0, 255))

        self.commandText = ['Attack', 'Defend', 'Item', 'Run']
        if 'Magus' in self.character.feats or 'Mage' in self.character.feats:
            self.commandText.insert(1, 'Magic')

        if 'Summoner' in self.character.feats:
            self.commandText.insert(1, 'Summon')

        self.commands = [content["font1"].render(text, True, constants.WHITE) for text in self.commandText]

    def attack(self, target, content):
        dmg, dCrit = self.character.attack(target.character)
        dmgString = str(abs(dmg))
        if dmg == -1:
            print 'Missed'
            dmgString = 'Miss'

        event = TextEvent(content, dmgString, (target.rect.x, target.rect.y - 5), constants.RED if dmg >= 0 else constants.WHITE)
        self.events['attacking'] = event
        target.isTargeted = False

        self.didAction(1)
        self.anim_state = 'attacking'
        self.character.animcount = self.character.ANIM_BATTLE_TIME

        return dmg, dCrit

    def __getMaxWait(self):
        if self.isPlayer:
            return 250 - (self.character.AGI + self.character.modAGI)
        else:
            return 50 - (self.character.AGI + self.character.modAGI)

    def update(self):
        if self.character.hp <= 0:
            return

        if self.anim_state:
            self.character.animcount -= 1
            if self.character.animcount % 4 == 0:
                self.character.frame = 1
            else:
                self.character.frame = 0

            if self.character.animcount == 0:
                if self.anim_state in self.events:
                    event = constants.pygame.event.Event(constants.USEREVENT_EVENT_TO_ADD, payload=self.events[self.anim_state])
                    constants.pygame.event.post(event)
                    del self.events[self.anim_state]

                self.anim_state = ''
                self.character.frame = 0

        if self.waitTime < self.__getMaxWait() - 1:
            self.waitTime += 1
        elif self.waitTime == self.__getMaxWait() - 1:
            self.waitTime += 1
            self.active = True

    def draw(self, screen, content):
        # if self.anim_state == 'attacking':
        screen.blit(self.character.images[self.character.frame], (self.rect.x, self.rect.y))
        self.__blitLabels(screen, content)

    def drawCommands(self, screen, content, cursorPos):
        cursor = content["font1"].render('*', True, constants.WHITE)

        for i in range(len(self.commands)):
            screen.blit(self.commands[i], (500, 220 + i * 16))

        screen.blit(cursor, (490, 220 + cursorPos * 16))

    def __blitLabels(self, screen, content):
        if self.isPlayer:
            xCoord = 460
            yCoord = 400 + self.character.partyPosition * 18

            text = content["font1"].render(self.character.name, True, constants.YELLOW if self.isMyTurn else constants.WHITE)
            screen.blit(text, (xCoord, yCoord))

            # yCoord += 16
            xCoord += 80
            # text = content["font1"].render("HP: {0:3d}/{1:3d}".format(self.character.hp, self.character.maxHp), True, WHITE)
            text = content["font1"].render("{0:3d}".format(self.character.hp, self.character.maxHp), True, constants.WHITE)
            screen.blit(text, (xCoord, yCoord))

            # yCoord += 16
            # text = content["font1"].render("Mana: +{0}".format(0), True, WHITE)
            # screen.blit(text, (xCoord, yCoord))


            coord = (xCoord + 40, yCoord + self.spdBarBack.get_height()-1)
            # coord = (xCoord, 390)
            screen.blit(self.spdBarBack, coord)
            spdBar = self.__calcSpdBar()
            if spdBar:
                screen.blit(spdBar, (coord[0], coord[1]+1))

        if self.isTargeted:
            screen.blit(constants.targetCursor, (self.rect.x, self.rect.y))

    def __calcSpdBar(self):
        maxWait = self.__getMaxWait()
        spdBarRatio = self.waitTime / float(maxWait)
        hpBarSize = int(spdBarRatio * 30)
        hpBar = constants.pygame.Surface((hpBarSize, 4))
        hpBar.fill((120, 120, 255))

        return hpBar

        # print self.waitTime, maxWait, spdBarRatio
        # hpBarSize = int(spdBarRatio * 30)
        # hpBar = pygame.Surface((hpBarSize, 4))
        # if spdBarRatio > 0.70:
        #     hpBar.fill((0, 100, 0))
        # elif spdBarRatio > 0.30:
        #     hpBar.fill((255, 255, 0))
        # else:
        #     hpBar.fill((255, 0, 0))

    def didAction(self, percent):
        percent = 1 - percent
        self.active = False
        self.waitTime = int(percent * self.__getMaxWait())
        self.isMyTurn = False