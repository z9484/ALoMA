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
        self.range = 1
        super(weapon, self).__init__(name, imgName, value, dmg)


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
BLADES = {
    'short sword': weapon('short sword', 'handR/short_sword_slant.bmp', 5, [1,6,-1,1], 'STR', 0),
    'claws': weapon('claws', '', 0, [1, 6, -1, 1], 'STR', 1),
    'dagger': weapon('dagger', '', 0, [1, 4, 0, 3], 'STR', 0),
    'sword': weapon('sword', '', 0, [1, 6, 0, 2], 'STR', 2),
    'axe': weapon('axe', '', 0, [1, 8, 0, 2], 'STR', 2),
    'rapier': weapon('rapier', '', 0, [1, 6, 0, 2], 'STR', 2),
    'broadsword': weapon('broadsword', '', 0, [1, 8, 0, 3], 'STR', 1),
    'katana': weapon('katana', '', 0, [1, 10, 0, 3], 'STR', 2),
    'magic claws': weapon('magic claws', '', 0, [1, 10, 0, 3], 'STR', 1),
    'great sword': weapon('great sword', '', 0, [1, 12, 0, 3], 'STR', 1),
    'battleaxe': weapon('battleaxe', '', 0, [2, 10, 0, -1], 'STR', 1),
    'ulsaera': weapon('ulsaera', '', 0, [2, 6, 0, -1], 'STR', 1),
}

IMPACT = {
    'fists': weapon('fists', '', 0, [1, 4, -1, 0], 'STR', 1),
    'staff': weapon('staff', '', 0, [1, 6, 0, 1], 'STR', 0),
    'club': weapon('club', '', 0, [1, 6, 0, 1], 'STR', 0),
    'mace': weapon('mace', '', 0, [1, 8, 0, 1], 'STR', 0),
    'morning star': weapon('morning star', '', 0, [1, 8, 0, 2], 'STR', 0),
    'war hammer': weapon('war hammer', '', 0, [1, 12, 0, 3], 'STR', 1),
}

PIERCE = {
    'half spear': weapon('half spear', '', 0, [1, 8, 0, 2], 'AGI', 1),
    'spear': weapon('spear', '', 0, [1, 10, 0, -1], 'AGI', 1),
    'halberd': weapon('halberd', '', 0, [1, 12, 0, -1], 'AGI', 1),
    'naginata': weapon('naginata', '', 0, [1, 12, 0, -1], 'AGI', 1),
}

RANGED = {
    'throwing knife': weapon('throwing knife', '', 5, [1, 4, 0, -1], 'AGI', 0),
    'sling': weapon('sling', '', 5, [1, 4, 0, 1], 'AGI', 0),
    'throwing stars': weapon('throwing stars', '', 5, [1, 10, 0, -1], 'AGI', 0),
    'short bow': weapon('short bow', 'handR/bow2.bmp', 5, [1, 6, 0, 1], 'AGI', 0),
    'bow': weapon('bow', '', 5, [1, 6, 0, 2], 'AGI', 0),
    'crossbow': weapon('crossbow', '', 5, [1, 6, 0, 2], 'AGI', 0),
    'heavy crossbow': weapon('heavy crossbow', '', 5, [1, 8, 0, -1], 'AGI', 0),
    'long bow': weapon('long bow', '', 5, [1, 8, 0, -1], 'AGI', 0),
}

#spells
SPELLS = {
    'flame': weapon('flame', 'effect/bolt04.bmp', 100, [1,6,-1,1], 'MAG', 0),
}

MONSTERS = {
    'rat': ('gfx/monsters/animals/gray_rat.bmp', None, BLADES['claws'], 20, (14, 10, 4, 0)),
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
