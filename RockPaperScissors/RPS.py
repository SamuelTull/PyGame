import pygame, sys
import numpy as np
from math import pi, sin, cos, sqrt


args = {
    "N": 3,
    "N_players": 75,
    "width": 1000,
    "height": 1000,
    "maxSpeed": 2,
    "maxForce": 0.1,
    "r": 18,
    "perception": 50,
    "N_grids": 3,
    "draw": "image",
}


class player:
    def __init__(self):
        self.position = args["width"] * np.random.rand(2)
        self.velocity = np.random.normal(0, 1, 2)
        self.acceleration = np.zeros(2)
        self.type = np.random.choice(types)
        self.maxSpeed = args["maxSpeed"]
        self.maxForce = args["maxForce"]
        self.r = args["r"]
        self.perception = args["perception"]
        self.draw = self.drawCircle if args["draw"] == "circle" else self.drawImage

    def update_random(self):
        a = 2 * pi * np.random.rand()
        self.position += self.maxSpeed * np.array((sin(a), cos(a)))

    def drawImage(self, screen):
        screen.blit(images[self.type], self.position - self.r)

    def drawCircle(self, screen):
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
            np.array((args["width"], self.position[1])),
            np.array((self.position[0], 0)),
            np.array((self.position[0], args["height"])),
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
        self.acceleration -= 5 * self.cohesion(playerSplit[enemies[self.type]])
        self.acceleration += 10 * self.avoidWalls()
        self.acceleration = setMag(self.acceleration, self.maxForce)

    def screenLoop(self):
        if self.position[0] > args["width"]:
            self.position[0] = 0 + 1e-1
        elif self.position[0] < 0:
            self.position[0] = args["width"] - 1e-1
        if self.position[1] > args["height"]:
            self.position[1] = 0 + 1e-1
        elif self.position[1] < 0:
            self.position[1] = args["height"] - 1e-1

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
    playerGridSplit = gridSplit(players)
    for players in playerGridSplit.values():
        playerSplit = {}
        for i in types:
            playerSplit[i] = [p for p in players if p.type == i]
        for p in players:
            p.flock(playerSplit)
            p.update()
        battle(players)


def gridSplit(players):
    playerGridSplit = {i: [] for i in range(args["N_grids"] ** 2)}
    for p in players:
        i = p.position[0] // (args["width"] / args["N_grids"])
        j = p.position[1] // (args["height"] / args["N_grids"])
        playerGridSplit[args["N_grids"] * i + j].append(p)
    return playerGridSplit


def draw(screen, players):
    screen.fill(0)
    for p in players:
        p.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("enter")
                return True
    return False


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((args["width"], args["height"]))
    colours = {0: [100, 255, 255], 1: [255, 100, 255], 2: [255, 255, 100]}
    images = {}
    for i, picture in enumerate(
        [
            pygame.image.load("rock.png").convert(),
            pygame.image.load("paper.png").convert(),
            pygame.image.load("scissors.png").convert(),
        ]
    ):
        images[i] = pygame.transform.scale(picture, (2 * args["r"], 2 * args["r"]))
    types = np.arange(args["N"])
    targets, enemies = {}, {}
    for i in types:
        targets[i] = (i + 1) % args["N"]
        enemies[i] = (i - 1) % args["N"]
    players = np.array([player() for _ in range(args["N_players"])])
    while True:
        reset = False
        while not reset:
            update(players)
            reset = draw(screen, players)
