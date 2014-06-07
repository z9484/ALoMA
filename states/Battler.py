# import pygame
# import random
import constants


class Battler(object):
    def __init__(self, content, character, side, isPlayer=False):
        self.character = character
        self.isPlayer = isPlayer
        self.isMyTurn = False
        self.isTargeted = False

        if isPlayer:
            rate = constants.random.randrange(45, 95) * .01
        else:
            rate = constants.random.randrange(0, 95) * .01

        self.waitTime = int(self.__getMaxWait() * rate)
        self.active = False
        self.side = side

        self.isBackRow = character.isBackRow
        self.rect = self.character.image.get_rect()

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

    def attack(self, target):
        dmg, dCrit = self.character.attack(target)
        self.didAction(1)

        return dmg, dCrit

    def __getMaxWait(self):
        if self.isPlayer:
            return 250 - (self.character.AGI + self.character.modAGI)
        else:
            return 50 - (self.character.AGI + self.character.modAGI)

    def update(self):
        if self.character.hp <= 0:
            return

        if self.waitTime < self.__getMaxWait() - 1:
            self.waitTime += 1
        elif self.waitTime == self.__getMaxWait() - 1:
            self.waitTime += 1
            self.active = True
            # event = pygame.event.Event(, char=self)
            # pygame.event.post(event)

    def draw(self, screen, content):
        screen.blit(self.character.image, (self.rect.x, self.rect.y))
        self.__blitLabels(screen, content)

    def drawCommands(self, screen, content, cursorPos):
        cursor = content["font1"].render('*', True, constants.WHITE)

        for i in range(len(self.commands)):
            screen.blit(self.commands[i], (500, 220 + i * 16))

        screen.blit(cursor, (490, 220 + cursorPos * 16))

    def __blitLabels(self, screen, content):
        if self.isPlayer:
            # xCoord = screen.get_rect().centerx - 160 + self.character.partyPosition * 120
            # yCoord = 400
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