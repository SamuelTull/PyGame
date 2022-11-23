import pygame, sys
import numpy as np
from math import pi, sin, cos, sqrt

width = 1000
height = 1000
N_players = 50

# pink -> yellow -> blue
colours = {0: [255, 255, 100], 1: [255, 100, 255], 2: [100, 255, 255]}


class player:
    def __init__(self):
        self.position = width * np.random.rand(2)
        self.velocity = np.random.rand(2)  #
        self.acceleration = np.zeros(2)
        self.type = np.random.choice([0, 1, 2])
        self.maxSpeed = 5
        self.maxForce = 0.01
        self.r = 10
        self.perception = 100

    def update_random(self):
        a = 2 * pi * np.random.rand()
        self.position += self.maxSpeed * np.array((sin(a), cos(a)))

    def draw(self, screen):
        pygame.draw.circle(screen, colours[self.type], self.position, self.r)

    def distance(self, other):
        return sqrt(
            (self.position[0] - other.position[0]) ** 2
            + (self.position[1] - other.position[1]) ** 2
        )

    def intersect(self, other):
        return self.distance(other) <= self.r + other.r

    def canSee(self, other):
        return self.distance(other) <= self.perception

    def align(self, players):
        desired = np.zeros(2)
        for player in players:
            if self.canSee(player):  # dont think it matters this includes self
                desired += player.velocity
                # total += 1
        desired = setMag(desired, self.maxSpeed)
        return clamp(desired - self.velocity, self.maxForce)

    def cohesion(self, players):
        desired = np.zeros(2)
        total = 0
        # dont think it matters this includes self/ difference is aims to speed up to max speed rather than slow to 0 if only boid
        # if dont want self remember to check total > 0
        for player in players:
            if self.canSee(player):
                desired += player.position
                total += 1
        desired /= max(total, 1)
        desired -= self.position
        return setMag(desired, self.maxForce)

    def seperation(self, players):
        desired = np.zeros(2)
        for player in players:
            if self.canSee(player) and player != self:
                diff = self.position - player.position
                desired += setMag(diff, 1 / self.distance(player))
        return setMag(desired, self.maxForce)

    def flock(self, players):
        self.acceleration = self.align(players)
        self.acceleration += self.cohesion(players)
        self.acceleration += self.seperation(players)

    def screenLoop(self):
        if self.position[0] > width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = width
        if self.position[1] > height:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = height

    def update(self):
        self.velocity += self.acceleration
        self.velocity = clamp(self.velocity, self.maxSpeed)
        self.position += self.velocity
        self.screenLoop()


def clamp(v, maxM):
    length = sqrt(v[0] ** 2 + v[1] ** 2)
    if length == 0:
        return v
    return v * min(maxM / length, 1)


def setMag(v, mag):
    length = sqrt(v[0] ** 2 + v[1] ** 2)
    if length == 0:
        return v
    return v * mag / length


def update(players):
    for p in players:
        p.flock(players)
        p.update()


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
    screen = pygame.display.set_mode((width, height))
    players = np.array([player() for _ in range(N_players)])
    i = 0
    while True:
        i += 1
        if i == 1000:
            continue
        update(players)
        draw(screen, players)


main()
