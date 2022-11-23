import pygame, sys
import numpy as np
from math import pi, sin, cos, sqrt

args = {
    "N": 3,
    "N_players": 50,
    "width": 1000,
    "height": 1000,
    "maxSpeed": 2,
    "maxForce": 0.1,
    "r": 18,
    "perception": 50,
}
args = {
    "N": 3,
    "N_players": 500,
    "width": 1000,
    "height": 1000,
    "maxSpeed": 2,
    "maxForce": 0.1,
    "r": 10,
    "perception": 50,
}

width = args["width"]
height = args["height"]
N_players = args["N_players"]
N = args["N"]

types = np.arange(N)
targets, enemies, colours = {}, {}, {}
for i in types:
    colours[i] = 255 * np.array(
        [sin(pi * i / N), 0.5 * sin((i / N + 1) * pi / 2), 0.5 * sin(i / N + 1)]
    )
    targets[i] = (i + 1) % N
    enemies[i] = (i - 1) % N
if N == 3:
    colours = {0: [100, 255, 255], 1: [255, 100, 255], 2: [255, 255, 100]}


class player:
    def __init__(self):
        self.position = width * np.random.rand(2)
        self.velocity = np.random.normal(0, 1, 2)
        self.acceleration = np.zeros(2)
        self.type = np.random.choice(types)
        self.maxSpeed = args["maxSpeed"]
        self.maxForce = args["maxForce"]
        self.r = args["r"]
        self.perception = args["perception"]

    def update_random(self):
        a = 2 * pi * np.random.rand()
        self.position += self.maxSpeed * np.array((sin(a), cos(a)))

    def draw(self, screen):
        pygame.draw.circle(screen, colours[self.type], self.position, self.r)

    def distance(self, v):
        return sqrt((self.position[0] - v[0]) ** 2 + (self.position[1] - v[1]) ** 2)

    def intersect(self, other):
        return self.distance(other.position) <= self.r + other.r

    def canSee(self, v):
        return self.distance(v) <= self.perception

    def align(self, players):
        desired = np.zeros(2)
        for player in players:
            if self.canSee(player.position):  # dont think it matters this includes self
                desired += player.velocity
        desired = setMag(desired, self.maxSpeed)
        return clamp(desired - self.velocity, self.maxForce)

    def cohesion(self, players):
        desired = np.zeros(2)
        total = 0
        # dont think it matters this includes self/ difference is aims to speed up to max speed rather than slow to 0 if only boid
        # if dont want self remember to check total > 0
        for player in players:
            if self.canSee(player.position):
                desired += player.position
                total += 1
        if total > 0:
            desired /= total
            desired -= self.position
            return setMag(desired, self.maxForce)
        return desired

    def seperation(self, players):
        desired = np.zeros(2)
        for player in players:
            if self.canSee(player.position) and player != self:
                diff = self.position - player.position
                desired += diff / self.distance(player.position)
        return setMag(desired, self.maxForce)

    def target(self, pos):
        return setMag(pos - self.position, self.maxForce)

    def avoidWalls(self):
        desired = np.zeros(2)
        for wall in [
            np.array((0, self.position[1])),
            np.array((width, self.position[1])),
            np.array((self.position[0], 0)),
            np.array((self.position[0], height)),
        ]:
            if self.canSee(wall):
                diff = self.position - wall
                desired += diff / (self.distance(wall) + 1e-10) ** 2
        return setMag(desired, self.maxForce)

    def flock(self, playerSplit):
        self.acceleration = 2 * self.seperation(playerSplit[self.type])
        self.acceleration += self.align(playerSplit[self.type])
        self.acceleration += self.cohesion(playerSplit[self.type])
        self.acceleration += self.cohesion(playerSplit[targets[self.type]])
        self.acceleration -= self.cohesion(playerSplit[enemies[self.type]])
        self.acceleration += 10 * self.avoidWalls()
        self.acceleration = setMag(self.acceleration, self.maxForce)

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


def battle(players):
    np.random.shuffle(players)
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            if players[i].type != players[j].type:
                if players[i].intersect(players[j]):
                    if players[i].type == targets[players[j].type]:
                        players[j].type = players[i].type
                    else:
                        players[i].type = players[j].type


def update(players):
    playerSplit = {}
    for i in types:
        playerSplit[i] = [p for p in players if p.type == i]
    for p in players:
        p.flock(playerSplit)
        p.update()
    battle(players)


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
