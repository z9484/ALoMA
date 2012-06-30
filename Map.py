import os
from pytmx import tmxloader

class Map(object):
    def __init__(self, filename):
        
        print 'loading', filename
        self.tiled = tmxloader.load_pygame('maps/' + filename + '.tmx') 
        #print dir(self.tiled)
        #obj = self.tiled.getObjects()
        #o = obj.next()
        #o2 = obj.next()
        #print o2.type
        
        if os.path.exists(os.path.abspath(os.curdir + '/maps/'  + filename + '.py')):
            exec('from maps.{0} import {0} as mapObject'.format(filename))
            self.mapScript = mapObject()
        try: 
            self.name = self.tiled.name
        except:
            self.name = ''
        
    def loadScript(self, filename):
        fileHandler = open('mapScripts/' + filename + '.txt', 'r')
        self.events = {}
        while True:
            temp = fileHandler.readline().strip()
            if temp == '[npc]':
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                fileHandler.readline().strip()
            elif temp == '[warp]':
                x = int(fileHandler.readline().strip())
                y = int(fileHandler.readline().strip())
                x2 = int(fileHandler.readline().strip())
                y2 = int(fileHandler.readline().strip())
                mapX = fileHandler.readline().strip()
                mapY = fileHandler.readline().strip()
                tt = fileHandler.readline().strip()
                fileHandler.readline().strip()
                self.events[(x,y)] = (0, (x2,y2), "{0}.{1}".format(mapX, mapY))
            elif temp == '':
                break
        fileHandler.close()
