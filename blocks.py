#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os
import pyganim
from pygame.locals import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "black"
ICON_DIR = os.path.dirname(__file__)

ANIMATION_MONSTERHORYSONTAL = [('%s/monsters/mushroom1.png' % ICON_DIR),
                      ('%s/monsters/fire2.png' % ICON_DIR )]

ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal2.png' % ICON_DIR),
            ('%s/blocks/portal1.png' % ICON_DIR)]
            
ANIMATION_PRINCESS = [
            ('%s/blocks/princess_l.png' % ICON_DIR),
            ('%s/blocks/princess_r.png' % ICON_DIR)]

ANIMATION_INBLOCKTELEPORT = [
            ('%s/blocks/invisiblePortal.png' % ICON_DIR),
            ('%s/blocks/invisiblePortal2.png' % ICON_DIR)]

 
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.5))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()


    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


class InvisibleBlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        self.image = image.load("%s/blocks/invisiblePortal.png" % ICON_DIR)

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))


class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 0.8))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


class Saw(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.original = image.load("%s/blocks/saw.png" % ICON_DIR)
        self.image = self.original
        self.angle = 0

    def update(self):
        rotated_image = pygame.transform.rotate(self.original, self.angle)
        rotated_image.fill(Color(PLATFORM_COLOR))
        self.angle += 3
        pygame.display.update()
