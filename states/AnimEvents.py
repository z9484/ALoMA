class AnimBaseEvent(object):
    def __init__(self, image, coord):
        self.coord = coord
        self.count = 15
        self.image = image
        self.func = None
        self.args = None

    def update(self):
        self.count -= 1
        if self.count == 0:
            self.call()

    def draw(self, screen):
        screen.blit(self.image, self.coord)

    def loadFunc(self, func, *args):
        self.func = func
        self.args = args

    def call(self):
        if self.func is not None:
            if self.args:
                self.func(*self.args)
            else:
                self.func()


class TextEvent(AnimBaseEvent):
    def __init__(self, content, text, coord, color):
        super(TextEvent, self).__init__(content["font1"].render(text, True, color), coord)


class AnimEvent(AnimBaseEvent):
    def __init__(self, content, spriteSheet, coord):
        super(AnimEvent, self).__init__(spriteSheet, coord)
