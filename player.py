import constants
import random
import sys
from math import sqrt
import pygame

class Character(object):
    def __init__(self, name, gender, race, image, x, y, skill, ste, agi, vit, mag):
        self.name = name
        self.gender = gender
        self.race = race
    
        self.skill = skill
        self.STR = ste
        self.AGI = agi
        self.VIT = vit
        self.MAG = mag

        self.calcMods()

        
        self.gold = 0
        self.maxHp = self.VIT * 2
        self.hp = self.maxHp  

        self.posX = x
        self.posY = y
        #self.load(image)

        self.inBattle = True
        self.isTargeted = False
    
        self.melee = []
        self.ranged = []
        
        self.items = [] 
    

    def draw(self, screen, coord):
        screen.blit(self.image, coord)
        
        if self.inBattle:
            screen.blit(self.hpBarBack,  coord)
            screen.blit(self.calcHpBar(),  (coord[0]+1, coord[1]+1))            

        if self.isTargeted:
            screen.blit(constants.targetCursor, coord)
        
        
    def calcHpBar(self):
        hpBarRatio = self.hp / float(self.maxHp)
        hpBarSize = int(hpBarRatio * 30)
        hpBar = pygame.Surface((hpBarSize, 2))
        if hpBarRatio > 0.70:
            hpBar.fill((0, 100, 0))
        elif hpBarRatio > 0.30:
            hpBar.fill((255, 255, 0))
        else:
            hpBar.fill((255, 0, 0))
        return hpBar
        
    def moveLeft(self):
        self.posX -= 1

    def moveRight(self):
        self.posX += 1

    def moveUp(self):
        self.posY -= 1

    def moveDown(self):
        self.posY += 1
        
    def save(self):
        self.image = []
        self.hpBarBack  = []
        
    def load(self, image):
        self.image = image
            
        self.hpBarBack = pygame.Surface((32, 4))
        self.hpBarBack.fill((0,0,0))    
        
        
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
        
    def attack(self, defender, isMelee):

        aSkill, aCrit = constants.rollDice(1,self.skill,self.modSkill,-1)
        #Return on critical failure
        if aCrit == -1: 
            return  -1, -1
            
        dSkill, dCrit = constants.rollDice(1,defender.skill,defender.modSkill,-1)
        
        if aSkill > dSkill:
            if isMelee:
                weapon = self.melee
            else:
                weapon = self.ranged
            
            die, sides, mod, crits = weapon.damage
            
            if   weapon.type == 'STR': 
                mod += self.modSTR
            elif weapon.type == 'AGI': 
                mod += self.modAGI
            elif weapon.type == 'MAG': 
                mod += self.modMAG
            
            dmg, dCrit = constants.rollDice(die,sides,mod,crits)
            defender.takeDamage(dmg)
            return dmg, dCrit
            
        else:
            return  -1, -1
            
class Player(Character):
    def __init__(self, name, gender, race, image):
        self.map = 'battle'

        race1 = constants.RACES[race]
        super(Player, self).__init__(name, gender, race, image, 5, 6, 10, race1.STR, race1.AGI, race1.VIT, race1.MAG)
        self.gold = 20
            
        self.melee = constants.BLADES['short sword']
        self.ranged = constants.RANGED['short bow']
        self.isMelee = False
        
        self.hair = 'boromir.bmp'
        self.beard = []
        self.equipCloak = []
        self.equipHead = []
        self.equipBody = 'leather_jacket.bmp'
        self.equipLegs = 'leg/pants_darkgreen.bmp'
        self.equipFeet = 'short_brown2.bmp'
        
        self.load(image)
        self.printStats()

    def draw(self, screen):
        Character.draw(self, screen, (7*constants.TILESIZE, 7*constants.TILESIZE))

    def load(self, image):
        Character.load(self, image)
        self.createImage()
        
    def createImage(self):
        if self.gender:
            gender = 'm'
        else:
            gender = 'f'
        
        if self.equipCloak != []:   
            self.image = pygame.image.load('gfx/player/cloak/' + 'black.bmp')
            self.image.set_colorkey(constants.COLORKEY)
            
            temp = pygame.image.load('gfx/player/base/shadow.bmp')
            temp.set_colorkey(constants.COLORKEY)
            self.image.blit(temp, (0,0))
        else:
            self.image = pygame.image.load('gfx/player/base/shadow.bmp')
            self.image.set_colorkey(constants.COLORKEY)
        
        temp = pygame.image.load('gfx/player/base/{0}_{1}.bmp'.format(self.race, gender))
        temp.set_colorkey(constants.COLORKEY)
        self.image.blit(temp, (0,0))

        if self.equipFeet != []:        
            temp = pygame.image.load('gfx/player/boot/'+ self.equipFeet)
            temp.set_colorkey(constants.COLORKEY)
            self.image.blit(temp, (0,0))
        
        if self.equipLegs != []:
            temp = pygame.image.load('gfx/player/' + self.equipLegs)
            temp.set_colorkey(constants.COLORKEY)
            self.image.blit(temp, (0,0))
        
        if self.equipBody != []:
            temp = pygame.image.load('gfx/player/body/' + self.equipBody)
            temp.set_colorkey(constants.COLORKEY)
            self.image.blit(temp, (0,0))
        
        if self.hair != []:
            temp = pygame.image.load('gfx/player/hair/' + self.hair)
            temp.set_colorkey(constants.COLORKEY)
            self.image.blit(temp, (0,0))
        
        if self.beard != []:
            temp = pygame.image.load('gfx/player/beard/' + self.beard)
            temp.set_colorkey(constants.COLORKEY)
            self.image.blit(temp, (0,0))
        
        if self.equipHead != []:
            temp = pygame.image.load('gfx/player/head/' + self.equipHead)
            temp.set_colorkey(constants.COLORKEY)
            self.image.blit(temp, (0,0))
        
        if self.isMelee:
            if self.melee != []:
                temp = pygame.image.load('gfx/player/' + self.melee.imgName)
                temp.set_colorkey(constants.COLORKEY)
                self.image.blit(temp, (0,0))
        else:
            if self.ranged != []:
                temp = pygame.image.load('gfx/player/' + self.ranged.imgName)
                temp.set_colorkey(constants.COLORKEY)
                self.image.blit(temp, (0,0))
        
class Monster(Character):
    def __init__(self, name, x, y):
    
        #print dir(constants.MONSTERS)
        if name in constants.MONSTERS:
            #MONSTERS['rat'] = ('gfx/monsters/animals/gray_rat.bmp', None, BLADES['claws'], 8, (1, 1, 4, 0))
            monStats = constants.MONSTERS[name]
            image = pygame.image.load(monStats[0])
            skill = monStats[3]
            stats = monStats[4]
            
        else:
            print 'No', name, 'monster exists defaulting to rat'
            monStats = constants.MONSTERS['rat']
            image = pygame.image.load(monStats[0])
            skill = monStats[3]
            stats = monStats[4]
            
        image.set_colorkey(constants.COLORKEY)
        super(Monster, self).__init__(name, 1, 'Monster', image, x, y, skill, *stats)
        self.load(image)
        
        self.ranged = monStats[1]
        self.melee = monStats[2]
        self.printStats()
        
    def draw(self, screen, x, y):
        isValid, deltaX, deltaY = self.inView(x, y)
        if isValid:
            Character.draw(self, screen, ( (7 - deltaX)*constants.TILESIZE, (7 - deltaY)*constants.TILESIZE) )
            



    def load(self, image):
        Character.load(self, image)
        #self.createImage()
        
        
    def inView(self, x, y):
        isValid = False
        deltaX = (x - self.posX)
        deltaY = (y - self.posY)
        
        if abs(deltaX) <= 7:
            if abs(deltaY) <= 7:
                isValid = True

        return isValid, deltaX, deltaY

