import pygame, sys
import numpy as np
from math import pi, sin, cos, sqrt

screen_width = 1000
screen_height = 1000
N_players = 50

# pink -> yellow -> blue
colours = {0: [255, 255, 100], 1: [255, 100, 255], 2: [100, 255, 255]}


class player:
    def __init__(self, x, y, type, speed, r):
        self.pos = np.array((x, y))
        assert type in range(2)
        self.type = type
        self.maxSpeed = speed
        self.v = np.zeros(2)
        self.r = r

    def __init__(self):
        self.pos = screen_width / 2 * (1 / 2 + np.random.rand(2))
        self.type = np.random.choice([0, 1, 2])
        self.maxSpeed = 2
        self.v = np.zeros(2)
        self.r = 20

    def update_random(self):
        a = 2 * pi * np.random.rand()
        self.pos += self.maxSpeed * np.array((sin(a), cos(a)))

    def update_random_acc(self):
        a = 2 * pi * np.random.rand()
        self.a = np.array((sin(a), cos(a)))
        self.v += self.a
        self.pos += self.v

    def draw(self, screen):
        pygame.draw.circle(screen, colours[self.type], self.pos, self.r)


def update(players):
    for p in players:
        p.update_random()
    np.random.shuffle(players)
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            if players[i].type != players[j].type:
                dx = (players[i].pos[0] - players[j].pos[0]) ** 2
                dy = (players[i].pos[1] - players[j].pos[1]) ** 2
                dr = players[i].r + players[j].r
                if sqrt(dx + dy) < dr:
                    if players[i].type == 0:
                        if players[j].type == 1:
                            players[j].type = 0
                        elif players[j].type == 2:
                            players[i].type = 2
                        else:
                            print("Ah1")
                    elif players[i].type == 1:
                        if players[j].type == 2:
                            players[j].type = 1
                        elif players[j].type == 0:
                            players[i].type = 0
                        else:
                            print("Ah2")
                    elif players[i].type == 2:
                        if players[j].type == 0:
                            players[j].type = 2
                        elif players[j].type == 1:
                            players[i].type = 1
                        else:
                            print("Ah3")
                    else:
                        print("Ah4")


def draw(screen, players):
    screen.fill(0)
    for p in players:
        p.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    players = np.array([player() for _ in range(N_players)])
    while True:
        update(players)
        draw(screen, players)


main()
