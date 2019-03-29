import os
import pygame
from pygame import *
import pyganim

WIN_WIDTH = 900
WIN_HEIGHT = 740
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "black"
FPS = 50
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "blue"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "black"
MOVE_SPEED = 7
MOVE_EXTRA_SPEED = 2.5 # ускорение
WIDTH = 22
HEIGHT = 32
COLOR = "gray"
JUMP_POWER = 10
JUMP_EXTRA_POWER = 1  # дополнительная сила прыжка
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.1 # скорость смены кадров
ANIMATION_SUPER_SPEED_DELAY = 0.13 # скорость смены кадров при ускорении
pygame.init()

ANIMATION_MONSTERHORYSONTAL = ['mushroom1.png', 'fire1.png']
ANIMATION_BLOCKTELEPORT = ['portal2.png', 'portal1.png']
ANIMATION_PRINCESS = ['princess_l.png', 'princess_r.png']
ANIMATION_INBLOCKTELEPORT = ['invisiblePortal.png', 'invisiblePortal2.png']
ANIMATION_RIGHT = ['r1.png', 'r2.png', 'r3.png', 'r4.png', 'r5.png']
ANIMATION_LEFT = ['l1.png', 'l2.png', 'l3.png', 'l4.png', 'l5.png']
ANIMATION_JUMP_LEFT = [('jl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('jr.png', 0.1)]
ANIMATION_JUMP = [('j.png', 0.1)]
ANIMATION_STAY = [('0.png', 0.1)]


def music():
    pygame.mixer.music.load('muzon.mid')
    pygame.mixer.music.play(-1, 0.0)


def terminate():
    pygame.quit()
    sys.exit()


def pre_start_screen():
    intro_text = ["Zstudio presents...",
                  "mini-MAR.io",
                  "(mario mini-remake)"]
    fon = pygame.transform.scale(pygame.image.load('Zstudio.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font1 = pygame.font.Font(None, 30)
    text_coord = 70
    for line in intro_text:
        string_rendered = font1.render(line, 1, pygame.Color('Snow 4'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    pre_start_screen()
    intro_text = ["ДОБРО ПОЖАЛОВАТЬ!",
                  "Правила игры:",
                  "управление стрелками,",
                  "не попадайся в ловушки(совет)",
                  "Задача: ",
                  "спаси принцессу)",
                  "(для продолжения нажмиите любую кнопку)"]

    fon = pygame.transform.scale(pygame.image.load('fon4.jpg'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font1 = pygame.font.Font(None, 30)
    text_coord = 10
    for line in intro_text:
        string_rendered = font1.render(line, 1, pygame.Color('Snow 4'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    intro_text = ["У тебя получилось!",
                  "Невероятно!",
                  "Спасибо за игру",
                  "Ждите MAR.io 2 REMASTED на Zstation в 2030 году"]

    fon = pygame.transform.scale(pygame.image.load('fon1.jpg'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 60
    pygame.mixer.music.load('muzon1.mid')
    pygame.mixer.music.play(-1, 0.0)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('Snow 4'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

            if event.type == QUIT:
                raise SystemExit("QUIT")
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                raise SystemExit("ESCAPE")
        pygame.display.flip()
        clock.tick(FPS)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width-WIN_WIDTH), l)
    t = max(-(camera.height-WIN_HEIGHT), t)
    t = min(0, t)
    return Rect(l, t, w, h) 


def loadLevel1():
    global playerX, playerY

    levelFile = open('1.txt')
    line = " "
    commands = []
    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":
            while line[0] != "]":
                line = levelFile.readline()
                if line[0] != "]":
                    endLine = line.find("|")
                    level.append(line[0: endLine])
                    
        if line[0] != "":
         commands = line.split()
         if len(commands) > 1:
            if commands[0] == "player":
                playerX = int(commands[1])
                playerY = int(commands[2])
            if commands[0] == "portal":
                tp = BlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                entities.add(tp)
                platforms.append(tp)
                animatedEntities.add(tp)
            if commands[0] == "inportal":
                itp = InvisibleBlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                entities.add(itp)
                platforms.append(itp)
                animatedEntities.add(itp)
            if commands[0] == "monster":
                mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                             int(commands[5]), int(commands[6]))
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = left
        self.yvel = up
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms):

        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("platform.png")
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("dieBlock.png")


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX
        self.goY = goY
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
        self.goX = goX
        self.goY = goY
        self.image = image.load("invisiblePortal.png")

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
        self.original = image.load("saw.png")
        self.image = self.original
        self.angle = 0

    def update(self):
        rotated_image = pygame.transform.rotate(self.original, self.angle)
        rotated_image.fill(Color(PLATFORM_COLOR))
        self.angle += 3
        pygame.display.update()


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        self.winner = False

    def update(self, left, right, up, running, platforms):

        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
                if running and (left or right):
                    self.yvel -= JUMP_EXTRA_POWER
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.xvel -= MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, BlockDie) or isinstance(p, Monster) \
                        or isinstance(p, Saw):
                    self.die()
                elif isinstance(p, BlockTeleport) or isinstance(p, InvisibleBlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, Princess):
                    self.winner = True
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        time.wait(500)
        if 2100 > self.rect.x > 1000:
            self.rect.x = 1150
            c = self.rect.x
        elif self.rect.x > 2100:
            self.rect.x = 2255
            c = self.rect.x
        else:
            c = self.startX
        self.teleporting(c, self.startY)


def main():
    start_screen()
    music()
    loadLevel1()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("MAR.io")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))
        
    left = right = False
    up = False
    running = False
    hero = Player(playerX, playerY)
    entities.add(hero)
    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "s":
                s = Saw(x, y)
                entities.add(s)
                platforms.append(s)
            if col == "P":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    
    total_level_width = len(level[0])*PLATFORM_WIDTH
    total_level_height = len(level)*PLATFORM_HEIGHT
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    
    while not hero.winner:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit("ESCAPE")

        pressed = pygame.key.get_pressed()
        up, left, right = [pressed[key] for key in (K_UP, K_LEFT, K_RIGHT)]

        screen.blit(bg, (0, 0))

        animatedEntities.update()
        monsters.update(platforms)
        camera.update(hero)
        hero.update(left, right, up, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()

    if hero.winner:
        print('U ARE WINNER! CONGRATULATIONS!!')
        end_screen()
        pygame.display.update()


level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
platforms = []
if __name__ == "__main__":
    main()
