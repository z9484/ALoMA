from Being import *
import random
import pygame

class item(object):
    def __init__(self, name, imgName, value, dmg):
        self.name = name
        self.imgName = imgName
        self.value = value
        self.damage = dmg
        
class weapon(item):
    def __init__(self, name, imgName, value, dmg, wType, hand):
        self.type = wType
        self.hand = hand
        super(weapon, self).__init__(name, imgName, value, dmg)


def rollDice(die, sides, mod, crits):
    critical = 0
    if crits == -1:
        crits = 1000
        
    total = 0;
    for i in xrange(die):
        val = random.randint(1,sides)
        total += val
        while val == sides and crits > 0:
            val = random.randint(1,sides)
            total += val
            crits -= 1
            critical = 1

    if total == die: #critical failure
        critical = -1
		
    return total + mod, critical
    
#Races
RACES = {}
RACES['human']    = Being('human',      8,  8,  8,  8, [1, 1, 1, 1])
RACES['areeam']   = Being('areeam',     6,  8,  9,  9, [0.75, 1.25, 1, 1])
RACES['notsonah'] = Being('notsonaH',  10,  9,  9,  4, [1.25, 1, 1.25, 0.5])
RACES['notsonaw'] = Being('notsonaw',  11,  9, 10,  2, [1.5, 1, 1.25, 0.25])
RACES['druid']    = Being('druid',      5, 10,  6, 11, [0.5, 1, 1, 1.5])
RACES['gargoyle'] = Being('gargoyle',  14,  6, 12,  4, [2, 0.5, 1.25, 0.25])
RACES['fae']      = Being('fae',        6,  9,  7, 14, [0.25, 0.25, 0.25, 2])


#weapons
BLADES = {}
BLADES['short sword'] = weapon('short sword', 'handR/short_sword_slant.bmp', 5, [1,6,-1,1], 'STR', 0)
BLADES['claws'] = weapon('claws', '', 0, [1,6,-1,1], 'STR', 0)


IMPACT = {}
IMPACT['fists'] = weapon('fists', '', 0, [1,4,-1,0], 'STR', 0)

RANGED = {}
RANGED['short bow'] = weapon('short bow', 'handR/bow2.bmp', 5, [1,6,0,1], 'AGI', 0)

#spells
SPELLS = {}
SPELLS['flame'] = weapon('flame', 'effect/bolt04.bmp', 100, [1,6,-1,1], 'MAG', 0)


MONSTERS = {}
MONSTERS['rat'] = ('gfx/monsters/animals/gray_rat.bmp', None, BLADES['claws'], 8, (1, 1, 4, 0))
MONSTERS['black_snake'] = 'gfx/monsters/animals/black_snake.bmp'

targetCursor = pygame.image.load('gfx/cursor_red.png')


FEMALE = 0
MALE = 1

FRAMES_PER_SECOND = 30
COOLTIME = 100
ICOOLTIME = 500
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
TILESIZE = 32
OBSTACLES = ["#", '~', '^', '#h', '#v']
MAXTEXT = 30
STATE = 0

COLORKEY = (71,108,108)