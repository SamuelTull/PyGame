import pygame
import math 
from helper import Ray,draw,Light,Wall
from helper import randomWalls,randomTriangles,fromPoints,fromPointsMirror,printPositionToLog

screen_width = 1000
screen_height = 1000

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

N_rays=800
mouse_r = 10
Walls = randomWalls(screen_width,screen_height)
light = Light(xv=1,yv=1) 
found = False
Walls += [Wall(300,0,300,1000)]
while not found:
    (i,j) = pygame.mouse.get_pos()
    light.move()
    (x,y) = ( light.x , light.y )
    mouse_angle = math.atan2( (j - y) , (i - x)) % math.tau        
    wall = Wall(i-mouse_r,j,i+mouse_r,j)
    wall2 = Wall(i,j-mouse_r,i,j+mouse_r)
    Rays = []
    for a in range(N_rays):
        angle = a * math.tau / N_rays
        x1 = x + 1440 * math.cos(angle)
        y1 = y + 1440 * math.sin(angle)
        ray = Ray(x,y,x1,y1,Walls)
        if mouse_angle - 0.01 < angle < mouse_angle  + 0.01 or angle<0.03 or angle>math.tau-0.01:
            if ray.castPlayerCheat(i,j,mouse_r):
                ray.colour = (255,0,0)     
                found = True   
        Rays.append(ray)
    draw(screen,Rays,Walls+[wall,wall2],[light])

print("found")
while True:
    draw(screen,Rays,Walls,[light])

