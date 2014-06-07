from Being import *
import random
import pygame

USEREVENT_EVENT_TO_ADD = 25


class Item(object):
    def __init__(self, name, imgName, value, dmg):
        self.name = name
        self.imgName = imgName
        self.value = value
        self.damage = dmg


class Weapon(Item):
    def __init__(self, name, imgName, value, dmg, wType, cat, hand, range=1):
        self.type = wType
        self.hand = hand
        self.range = range
        self.cat = cat
        super(Weapon, self).__init__(name, imgName, value, dmg)


def rollDice(die, sides, mod, crits):
    critical = 0
    if crits == -1:
        crits = 1000
        
    total = 0
    for i in xrange(die):
        val = random.randint(1, sides)
        total += val
        while val == sides and crits > 0:
            val = random.randint(1, sides)
            total += val
            crits -= 1
            critical = 1

    if total == die:  # critical failure
        critical = -1

    # Dice can not go negative
    subTotal = total + mod
    if subTotal < 0:
        subTotal = 0

    return subTotal, critical
    
#Races
RACES = {
    'human':     Being('human',          8,  8,  8,  8,  8, [1, 1, 1, 1]),
    'areeam':    Being('areeam',         6,  8,  9,  9,  9, [0.75, 1.25, 1, 1]),
    'wrenonunh': Being('wrenonun Hand', 10,  9,  9,  4, 10, [1.25, 1, 1.25, 0.5]),
    'wrenonunp': Being('wrenonun Paw',  11,  9, 10,  2, 11, [1.5, 1, 1.25, 0.25]),
    'druid':     Being('druid',          5, 10,  6, 11,  7, [0.5, 1, 1, 1.5]),
    'gargoyle':  Being('gargoyle',      14,  6, 12,  4, 12, [2, 0.5, 1.25, 0.25]),
    'fae':       Being('fae',            6,  9,  7, 14,  7, [0.25, 0.25, 0.25, 2])
}

#weapons
WEAPONS = {
    'short sword': Weapon('short sword', 'handR/short_sword_slant.bmp', 5, [1,6,-1,1], 'STR', 'BLADE', 0),
    'claws': Weapon('claws', '', 0, [1, 6, -1, 1], 'STR', 'BLADE', 1),
    'dagger': Weapon('dagger', '', 0, [1, 4, 0, 3], 'STR', 'BLADE', 0),
    'sword': Weapon('sword', '', 0, [1, 6, 0, 2], 'STR', 'BLADE', 2),
    'axe': Weapon('axe', '', 0, [1, 8, 0, 2], 'STR', 'BLADE', 2),
    'rapier': Weapon('rapier', '', 0, [1, 6, 0, 2], 'STR', 'BLADE', 2),
    'broadsword': Weapon('broadsword', '', 0, [1, 8, 0, 3], 'STR', 'BLADE', 1),
    'katana': Weapon('katana', '', 0, [1, 10, 0, 3], 'STR', 'BLADE', 2),
    'magic claws': Weapon('magic claws', '', 0, [1, 10, 0, 3], 'STR', 'BLADE', 1),
    'great sword': Weapon('great sword', '', 0, [1, 12, 0, 3], 'STR', 'BLADE', 1),
    'battleaxe': Weapon('battleaxe', '', 0, [2, 10, 0, -1], 'STR', 'BLADE', 1),
    'ulsaera': Weapon('ulsaera', '', 0, [2, 6, 0, -1], 'STR', 'BLADE', 1),

    'fists': Weapon('fists', '', 0, [1, 4, -1, 0], 'STR', 'IMPACT', 1),
    'staff': Weapon('staff', '', 0, [1, 6, 0, 1], 'STR', 'IMPACT', 0),
    'club': Weapon('club', '', 0, [1, 6, 0, 1], 'STR', 'IMPACT', 0),
    'mace': Weapon('mace', '', 0, [1, 8, 0, 1], 'STR', 'IMPACT', 0),
    'morning star': Weapon('morning star', '', 0, [1, 8, 0, 2], 'STR', 'IMPACT', 0),
    'war hammer': Weapon('war hammer', '', 0, [1, 12, 0, 3], 'STR', 'IMPACT', 1),

    'half spear': Weapon('half spear', '', 0, [1, 8, 0, 2], 'AGI', 'PIERCE', 1),
    'spear': Weapon('spear', '', 0, [1, 10, 0, -1], 'AGI', 'PIERCE', 1),
    'halberd': Weapon('halberd', '', 0, [1, 12, 0, -1], 'AGI', 'PIERCE', 1, range=2),
    'naginata': Weapon('naginata', '', 0, [1, 12, 0, -1], 'AGI', 'PIERCE', 1, range=2),

    'throwing knife': Weapon('throwing knife', '', 5, [1, 4, 0, -1], 'AGI', 'PIERCE', 0, range=2),
    'sling': Weapon('sling', '', 5, [1, 4, 0, 1], 'AGI', 'IMPACT', 0, range=2),
    'throwing stars': Weapon('throwing stars', '', 5, [1, 10, 0, -1], 'AGI', 'PIERCE', 0, range=2),
    'short bow': Weapon('short bow', 'handR/bow2.bmp', 5, [1, 6, 0, 1], 'AGI', 'PIERCE', 0, range=2),
    'bow': Weapon('bow', '', 5, [1, 6, 0, 2], 'AGI', 'PIERCE', 0, range=2),
    'crossbow': Weapon('crossbow', '', 5, [1, 6, 0, 2], 'AGI', 'PIERCE', 0, range=2),
    'heavy crossbow': Weapon('heavy crossbow', '', 5, [1, 8, 0, -1], 'AGI', 'PIERCE', 0, range=2),
    'long bow': Weapon('long bow', '', 5, [1, 8, 0, -1], 'AGI', 'PIERCE', 0, range=2),
}

#spells
SPELLS = {
    'flame': Weapon('flame', 'effect/bolt04.bmp', 100, [1,6,-1,1], 'MAG', 'FIRE', 0),
}

MONSTERS = {
    'rat': ('gfx/monsters/animals/gray_rat.bmp', None, WEAPONS['claws'], 20, (14, 10, 4, 0)),
    'black_snake': 'gfx/monsters/animals/black_snake.bmp'
}

targetCursor = pygame.image.load('gfx/cursor_red.png')

FEMALE = 0
MALE = 1

FRAMES_PER_SECOND = 30
COOLTIME = 100
ICOOLTIME = 500
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
YELLOW = (215, 232, 58)
TILESIZE = 32
OBSTACLES = ["#", '~', '^', '#h', '#v']
MAXTEXT = 30
STATE = 0

COLORKEY = (71,108,108)
