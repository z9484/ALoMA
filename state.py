import pygame, sys
from pygame.locals import *
import constants


class State(object):
    def __init__(self, screen, content):
        self.screen = screen
        self.content = content
        self.dt = 0
        self.keys = []
        self.cooltime = constants.COOLTIME
        self.keysDown = []
        self.events = []

    def update(self, clock):
        self.keysDown = []
        self.events = []
        self.dt = clock.get_time()
    
        for event in pygame.event.get():
            if hasattr(event, 'key'):
                if event.type == KEYDOWN:
                    self.keysDown.append(event.key)
                    self.keys.append([event.key, constants.ICOOLTIME])
                elif event.type == KEYUP:
                    self.keyreleased(event.key)

            elif event.type == USEREVENT+1:
                self.events.append(event)

    def draw(self):
        # for i in xrange(len(self.keys)):
        #     if self.keys[i][0] == key:
        #         self.keys.pop(i)
        #         break
        pass
    
    def keyreleased(self, key):
        for i in xrange(len(self.keys)):
            if self.keys[i][0] == key:
                self.keys.pop(i)
                break
                
    def check_cool(self, index):
        cool = self.cooltime
        if index >= len(self.keys):
            return False
        
        if self.keys[index][0] == K_BACKSPACE:
            cool = 25
            
        if self.keys[index][1] <= 0:
            self.keys[index][1] = cool
            return True
        else:
            self.keys[index][1] -= self.dt
            return False
