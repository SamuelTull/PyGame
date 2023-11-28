import pygame
import math 
from helper import Ray,draw
from helper import randomWalls,randomTriangles,fromPoints,fromPointsMirror,printPositionToLog

screen_width = 1000
screen_height = 1000

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

N_rays=3000
#Walls = fromPointsMirror(screen_width,screen_height) 
Walls = randomWalls(screen_width,screen_height)
while True:
    (x,y) = pygame.mouse.get_pos()
    x = min(screen_width,max(0,x))
    y = min(screen_height,max(0,y))
    Rays = []
    for i in range(N_rays):
        angle = i * 2 * math.pi/N_rays
        x1 = x + 1420 * math.cos(angle)
        y1 = y + 1420 * math.sin(angle)
        Rays.append(Ray(x,y,x1,y1,Walls))
    #printPositionToLog()
    draw(screen,Rays,Walls)


