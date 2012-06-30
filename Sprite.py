class Sprite(object):
    def __init__(self, images):
        self.images = images
        self.frame = 0
        self.delay = 1500 / 30
        self.last_update = 0
        self.shouldPlay = False
        
    def update(self, ticks):
        if self.shouldPlay and ticks - self.last_update > self.delay:
            self.frame += 1
            self.last_update = ticks
            if self.frame == 7:
                self.frame = 0
                self.shouldPlay = False

    def play(self):
        self.shouldPlay = True
        
    def draw(self, screen, position):
        screen.blit(self.images[self.frame], position)
