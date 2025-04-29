import pygame
import sys
import random

o = 35

def bird_l(type):
    if type == 1:
        image = pygame.image.load("Images/blues_l.png")
        image = pygame.transform.scale(image,(o,o))
    if type == 2:
        image = pygame.image.load("Images/bomb_l.png")
        image = pygame.transform.scale(image,(o,o))
    if type == 3:
        image = pygame.image.load("Images/chuk_l.png")
        image = pygame.transform.scale(image,(o,o))
    if type == 4:
        image = pygame.image.load("Images/red_l.png")
        image = pygame.transform.scale(image,(o,o))
    return image
def bird_r(type):
    if type == 1:
        image = pygame.image.load("Images/blues_r.png")
        image = pygame.transform.scale(image,(o,o))
    if type == 2:
        image = pygame.image.load("Images/bomb_r.png")
        image = pygame.transform.scale(image,(o,o))
    if type == 3:
        image = pygame.image.load("Images/chuk_r.png")
        image = pygame.transform.scale(image,(o,o))
    if type == 4:
        image = pygame.image.load("Images/red_r.png")
        image = pygame.transform.scale(image,(o,o))
    return image

bird_types_l = [random.randint(1,4) for _ in range(3)]
birds_l = [bird_l(t) for t in bird_types_l]

bird_types_r = [random.randint(1,4) for _ in range(3)]
birds_r = [bird_r(t) for t in bird_types_r]

#using get_rect
rect_l = [image.get_rect(bottomright=(365+(o+5)*(birds_l.index(image)),515)) for image in birds_l]
rect_r = [image.get_rect(topleft=(775+(o+5)*(birds_r.index(image)),480)) for image in birds_r]
def birds_draw_left(scr):
    for i in range(3):
        scr.blit(birds_l[i],rect_l[i])
def birds_draw_right(scr):
    for i in range(3):
        scr.blit(birds_r[i],rect_r[i])