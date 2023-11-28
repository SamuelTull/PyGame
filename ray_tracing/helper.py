import pygame
import random
import sys 
import math
class Wall():
    def __init__(self,x1,y1,x2,y2):
        self.a = (x1,y1)
        self.b = (x2,y2)

    def show(self,screen):
        pygame.draw.line(screen,(255,100,100),self.a,self.b,5)
    
class Ray():
    def __init__(self,x1,y1,x2,y2,Walls):
        self.a = (x1,y1)
        self.b = (x2,y2)
        self.colour = (255,200,200)
        for wall in Walls:
            self.cast(wall)

    def cast(self,wall):
        # intersectimg ? 
        # if yes find intersection point 
        # if point makes line shorter make it shorter
        (x1,y1) = self.a 
        (x2,y2) = self.b
        (x3,y3) = wall.a
        (x4,y4) = wall.b
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)+1e-10)
        u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)+1e-10)
        if 0<=t<=1 and 0<=u<=1:
            self.b = (x1+t*(x2-x1),y1+t*(y2-y1))
    
    def castPlayerCheat(self,x,y,r):
        (x1,y1) = self.a 
        (x2,y2) = self.b
        (x3,y3) = (x-r,y)
        (x4,y4) = (x+r,y)
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)+1e-10)
        u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)+1e-10)
        if 0<=t<=1 and 0<=u<=1:
            return True
        (x3,y3) = (x,y-r)
        (x4,y4) = (x,y+r)
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)+1e-10)
        u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)+1e-10)
        if 0<=t<=1 and 0<=u<=1:
            return True
        return False

    def castPlayer(self,x,y,r):
        (x1,y1) = self.a 
        (x2,y2) = self.b
        A = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) 
        B = -2 * x * (x2 - x1) -2 * y * (y2 - y1)
        C = x * x + y * y + r * r
        if B * B - 4 * A * C > 0:
            t = -B + math.sqrt ( B * B - 4 * A * C)
            t /= 2*A
            if 0 <= t <= 1:
                self.colour = (255,0,0)
                return True
        return False


    def show(self,screen):
        pygame.draw.line(screen,self.colour,self.a,self.b,10)

class Light():
    def __init__(self,x=500,y=500,xv=0,yv=0):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.xa = 0
        self.ya = 0 
        self.r = 10

    def applyForce(self,i,j):
        self.xa += i
        self.ya += j

    def move(self):
        self.x += self.xv
        self.y += self.yv
        self.xv += self.xa
        self.yv += self.ya
        self.xa = 0
        self.ya = 0
        if self.reset():
            self.x = 500
            self.y = 500

    def reset(self):
        if self.x > 2000 or self.x < -1000:
            return True
        if self.y > 2000 or self.y < -1000:
            return True
        return False

    def show(self,screen):
        pygame.draw.circle(screen,(100,255,100),(self.x,self.y),self.r)


def draw(screen,Rays=[],Boundaries=[],Items=[]):
    screen.fill(0)
    for ray in Rays:
        ray.show(screen)
    for boundary in Boundaries:
        boundary.show(screen)
    for item in Items:
        item.show(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def printPositionToLog():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                (x,y) = pygame.mouse.get_pos()
                print(x,y)

def randomWalls(screen_width,screen_height):
    Walls=[]
    for i in range (2):
        for j in range(2):
            x1 = random.random() * ((i+1) * screen_width/2 - i * screen_width/2) + (i * screen_width/2)
            x2 = random.random() * ((i+1) * screen_width/2 - i * screen_width/2) + (i * screen_width/2)
            y1 = random.random() * ((j+1) * screen_height/2 - j * screen_height/2) + (j * screen_height/2)
            y2 = random.random() * ((j+1) * screen_height/2 - j * screen_height/2) + (j * screen_height/2)
            Walls.append(Wall(x1,y1,x2,y2))
    return Walls

def randomTriangles(screen_width,screen_height):
    Walls=[]
    for i in range (2):
        for j in range(2):
            x1 = random.random() * ((i+1) * screen_width/2 - i * screen_width/2) + (i * screen_width/2)
            x2 = random.random() * ((i+1) * screen_width/2 - i * screen_width/2) + (i * screen_width/2)
            x3 = random.random() * ((i+1) * screen_width/2 - i * screen_width/2) + (i * screen_width/2)
            y1 = random.random() * ((j+1) * screen_height/2 - j * screen_height/2) + (j * screen_height/2)
            y2 = random.random() * ((j+1) * screen_height/2 - j * screen_height/2) + (j * screen_height/2)
            y3 = random.random() * ((j+1) * screen_height/2 - j * screen_height/2) + (j * screen_height/2)        
            Walls.append(Wall(x1,y1,x2,y2))
            Walls.append(Wall(x2,y2,x3,y3))
            Walls.append(Wall(x3,y3,x1,y1))
    return Walls

def fromPoints(screen_width,screen_height):
    Walls=[]
    with open('Python/Pygame/ray_tracing/points.txt') as f:
        lines=f.readlines()
    points=[]
    for line in lines:
        points.append([int(x) for x in line.split()])
    for i in range(len(points)-1):
        Walls.append(Wall(points[i][0],points[i][1],points[i+1][0],points[i+1][1]))
    return Walls


def fromPointsMirror(screen_width,screen_height):
    Walls=[]
    with open('Python/Pygame/ray_tracing/points.txt') as f:
        lines=f.readlines()
    points=[]
    for line in lines:
        points.append([int(x) for x in line.split()])
    for i in range(len(points)-1):
        Walls.append(Wall(points[i][0],points[i][1],points[i+1][0],points[i+1][1]))
    for j in range(len(points)-1):
        i=len(points)-j-1
        Walls.append(Wall(screen_width-points[i][0],points[i][1],screen_width-points[i-1][0],points[i-1][1]))
    return Walls

"""
heart:
500 350
450 225
325 125
150 150
50 350
100 550
500 900
"""