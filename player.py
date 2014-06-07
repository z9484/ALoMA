import constants
import random
import sys
from math import sqrt
import pygame


class Party(object):
    MAX_PARTY_SIZE = 4

    def __init__(self):
        self.members = []
        self.gold = 0

    def add(self, character):
        if len(self.members) < Party.MAX_PARTY_SIZE:
            availableSlots = range(Party.MAX_PARTY_SIZE)
            for member in self.members:
                if member.partyPosition in availableSlots:
                    availableSlots.remove(member.partyPosition)

            if len(availableSlots) > 0:
                character.partyPosition = availableSlots[0]
                self.members.append(character)

    def remove(self, character):
        self.members.remove(character)


class Character(object):
    ANIM_TIME = 15
    ANIM_BATTLE_TIME = 12

    def __init__(self, name, gender, race, image, x, y, skill, naturalArmor, ste, agi, vit, mag):
        self.name = name
        self.gender = gender
        self.race = race
        self.isBackRow = False
        self.partyPosition = 0
        self.skill = skill
        self.STR = ste
        self.AGI = agi
        self.VIT = vit
        self.MAG = mag
        #Add bonus values from equipment and buffs
        
        self.calcMods()
        
        self.gold = 0
        self.maxHp = self.VIT * 2
        self.hp = self.maxHp  

        self.posX = x
        self.posY = y
        self.animcount = Character.ANIM_TIME
        #self.load(image)

        # self.inBattle = True
        # self.isTargeted = False
    
        self.weapon = constants.WEAPONS['fists']
        
        self.armor = 0
        self.naturalArmor = naturalArmor
        self.items = [] 
        self.steps = 0
        self.pathToGo = []
        # self.canAttack = True
        self.feats = []
        self.frame = 0
        self.images = []
        
    def setNumSteps(self):
        steps = 1 + self.AGI / 4
        #~ if steps < 0: steps = 1        
        self.steps = steps
    
    def draw(self, screen, coord):
        screen.blit(self.images[self.frame], coord)

    def moveLeft(self):
        self.posX -= 1
        self.steps -=1
        
    def moveRight(self):
        self.posX += 1
        self.steps -=1

    def moveUp(self):
        self.posY -= 1
        self.steps -=1

    def moveDown(self):
        self.posY += 1
        self.steps -=1
        
    def save(self):
        self.images = []
        self.hpBarBack = []
        
    def load(self, images):
        self.images = images
            
        # self.hpBarBack = pygame.Surface((32, 4))
        # self.hpBarBack.fill(constants.BLACK)
        
    def printStats(self):
        print 'Name', self.name
        print 'Race', self.race
        print 'HP', self.hp, '/', self.maxHp
        print 'STR', self.STR
        print 'AGI', self.AGI
        print 'VIT', self.VIT
        print 'Mag', self.MAG
        print 'Gold', self.gold
        print

    def calcMods(self):
        self.modSkill = 0
        self.modSTR = self.getMod(self.STR)
        self.modAGI = self.getMod(self.AGI)
        self.modVIT = self.getMod(self.VIT)
        self.modMAG = self.getMod(self.MAG)
        
    def getMod(self, skill):
        return (skill - 8) / 2
    
    def takeDamage(self, dmg):
        self.hp -= dmg
        if self.hp < 0: self.hp = 0
        
    # def canAttackPos(self, x, y):
    #     #if self.ranged:
    #     if self.melee:
    #         if self.posX == x+1 and self.posY == y:
    #             return True
    #         elif self.posX == x-1 and self.posY == y:
    #             return True
    #         elif self.posX == x and self.posY == y+1:
    #             return True
    #         elif self.posX == x and self.posY == y-1:
    #             return True
                
    def attack(self, defender, no_front_row):
        aSkill, aCrit = constants.rollDice(1, self.skill, self.modSkill, -1)
        #Return on critical failure
        if aCrit == -1:
            print 'Critical Failure'
            return 0, -1
            
        if aCrit > 0: print 'Crit'
        
        #dSkill, dCrit = constants.rollDice(1,defender.skill,defender.modSkill,-1)
        dSkill = defender.naturalArmor + defender.armor + defender.getMod(defender.AGI)
        
        print 'skill', aSkill, dSkill
        
        if aSkill > dSkill:
            # if isMelee:
            # else:
            #     weapon = self.ranged
            
            die, sides, mod, crits = self.weapon.damage
            
            if self.weapon.type == 'STR':
                mod += self.modSTR
            elif self.weapon.type == 'AGI':
                mod += self.modAGI
            elif self.weapon.type == 'MAG':
                mod += self.modMAG

            dmg, dcrit = constants.rollDice(die, sides, mod, crits)

            if not no_front_row and defender.isBackRow and self.weapon.range == 1:
                dmg /= 2

            return dmg, dcrit
            
        else:
            return 0, -1


class Player(Character):
    def __init__(self, name, gender, race, image):
        self.map = 'battle'
        
        race1 = constants.RACES[race]
        super(Player, self).__init__(name, gender, race, image, 5, 6, 20, race1.naturalArmor, race1.STR, race1.AGI, race1.VIT, race1.MAG)
        self.gold = 20

        self.weapon = constants.WEAPONS['short bow']
        # self.weapon = constants.WEAPONS['short sword']
        self.offhand = None

        self.isMelee = False
        
        self.hair = 'boromir.bmp'
        self.beard = ''
        self.equipCloak = ''
        self.equipHead = ''
        self.equipBody = 'leather_jacket.bmp'
        self.equipLegs = 'leg/pants_darkgreen.bmp'
        self.equipFeet = 'short_brown2.bmp'

        self.load(image)

        blinkImage = self.images[0].copy()
        blinkImage.lock()
        pxArray = pygame.PixelArray(blinkImage)
        pxArray.replace(constants.BLACK, constants.WHITE)
        blinkImage.unlock()
        self.images.append(blinkImage)

        self.printStats()

        self.isPlayer = True
        self.isMeleeMode = True
        
    def draw(self, screen):
        Character.draw(self, screen, (7*constants.TILESIZE, 7*constants.TILESIZE))

    def load(self, image):
        # Character.load(self, image)
        self.createImage()
        
    def createImage(self):
        if self.gender:
            gender = 'm'
        else:
            gender = 'f'
        
        if self.equipCloak:
            image = pygame.image.load('gfx/player/cloak/' + 'black.bmp')
            image.set_colorkey(constants.COLORKEY)
            
            temp = pygame.image.load('gfx/player/base/shadow.bmp')
            temp.set_colorkey(constants.COLORKEY)
            image.blit(temp, (0,0))
        else:
            image = pygame.image.load('gfx/player/base/shadow.bmp')
            image.set_colorkey(constants.COLORKEY)
        
        temp = pygame.image.load('gfx/player/base/{0}_{1}.bmp'.format(self.race, gender))
        temp.set_colorkey(constants.COLORKEY)
        image.blit(temp, (0,0))

        if self.equipFeet:
            temp = pygame.image.load('gfx/player/boot/'+ self.equipFeet)
            temp.set_colorkey(constants.COLORKEY)
            image.blit(temp, (0,0))
        
        if self.equipLegs:
            temp = pygame.image.load('gfx/player/' + self.equipLegs)
            temp.set_colorkey(constants.COLORKEY)
            image.blit(temp, (0,0))
        
        if self.equipBody:
            temp = pygame.image.load('gfx/player/body/' + self.equipBody)
            temp.set_colorkey(constants.COLORKEY)
            image.blit(temp, (0,0))
        
        if self.hair:
            temp = pygame.image.load('gfx/player/hair/' + self.hair)
            temp.set_colorkey(constants.COLORKEY)
            image.blit(temp, (0,0))
        
        if self.beard:
            temp = pygame.image.load('gfx/player/beard/' + self.beard)
            temp.set_colorkey(constants.COLORKEY)
            image.blit(temp, (0,0))
        
        if self.equipHead:
            temp = pygame.image.load('gfx/player/head/' + self.equipHead)
            temp.set_colorkey(constants.COLORKEY)
            image.blit(temp, (0,0))
        
        if self.isMelee:
            if self.weapon.range == 1:
                temp = pygame.image.load('gfx/player/' + self.weapon.imgName)
                temp.set_colorkey(constants.COLORKEY)
                image.blit(temp, (0,0))
        else:
           if self.weapon.range > 1:
                temp = pygame.image.load('gfx/player/' + self.weapon.imgName)
                temp.set_colorkey(constants.COLORKEY)
                image.blit(temp, (0,0))

        self.images.append(image)


class Monster(Character):
    def __init__(self, name, x, y):
        if name in constants.MONSTERS:
            #MONSTERS['rat'] = ('gfx/monsters/animals/gray_rat.bmp', None, BLADES['claws'], 8, (1, 1, 4, 0))
            monStats = constants.MONSTERS[name]
            image = pygame.image.load(monStats[0])
            # image.fill((250, 250, 250))

            skill = monStats[3]
            stats = monStats[4]
            
        else:
            print 'No', name, 'monster exists defaulting to rat'
            monStats = constants.MONSTERS['rat']
            image = pygame.image.load(monStats[0])
            skill = monStats[3]
            stats = monStats[4]
            
        image.set_colorkey(constants.COLORKEY)
        super(Monster, self).__init__(name, 1, 'Monster', image, x, y, skill, 4, *stats)
        self.load(image)


        blinkImage = self.images[0].copy()
        blinkImage.lock()
        pxArray = pygame.PixelArray(blinkImage)
        pxArray.replace(constants.BLACK, constants.WHITE)
        blinkImage.unlock()
        self.images.append(blinkImage)

        self.ranged = monStats[1]
        self.melee = monStats[2]
        self.printStats()
        self.isPlayer = False
        
    def draw(self, screen, x, y):
        isValid, deltaX, deltaY = self.inView(x, y)
        if isValid:
            Character.draw(self, screen, ((7 - deltaX)*constants.TILESIZE, (7 - deltaY)*constants.TILESIZE))
            
    def load(self, image):
        self.images.append(image)
        # Character.load(self, image)

    def inView(self, x, y):
        isValid = False
        deltaX = (x - self.posX)
        deltaY = (y - self.posY)
        
        if abs(deltaX) <= 7:
            if abs(deltaY) <= 7:
                isValid = True

        return isValid, deltaX, deltaY

