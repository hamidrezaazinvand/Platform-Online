import pygame as pg
import sys

from network import Network

pg.init()

screen = pg.display.set_mode((800, 600), 0, 32)
clock = pg.time.Clock()

class Player:
    def __init__(self, pos, size, color):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.color = color
        self.speed = 2

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.rect.y -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        if keys[pg.K_d]:
            self.rect.x += self.speed

    def update(self):
        self.input()

    def render(self, surf):
        a = pg.Surface(self.rect.size)
        a.fill(self.color)
        surf.blit(a, self.rect)

net = Network()

player = Player((100, 100), (32, 32), (255, 187, 90))
player_2 = Player((150, 100), (32, 32), (0, 0, 0))

def parse_data(data):
    try:
        d = data.split(":")[1].split(",")
        return int(d[0]), int(d[1])
    except:
        return 0, 0

def send_data():
    data = str(net.id) + ":" + str(player.rect.x) + "," + str(player.rect.y)
    reply = net.send(data)
    return reply

while True:
    screen.fill((255, 255, 255))

    player.update()
    player.render(screen)

    player_2.rect.x, player_2.rect.y = parse_data(send_data())

    player_2.update()
    player_2.render(screen)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(60)