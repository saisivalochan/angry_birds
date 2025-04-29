import pygame
import sys
import random

# Fixing variables
p = 75  # Height and width of blocks in pixels
start_y = 440
class Block:
    def __init__(self, block_type, x, y):
        self.type = block_type
        self.image = self.load_image(block_type)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100  # Default health for each block

    def load_image(self, block_type):
        if block_type == 1 :
            image = pygame.image.load("Images/wooden_block.png")
        if block_type == 2 :
            image = pygame.image.load("Images/rock_block.png")
        if block_type == 3:
            image = pygame.image.load("Images/ice_block.png")
        if block_type == 4:
            image = pygame.image.load("Images/wooden_block.png")
        image = pygame.transform.scale(image, (p, p))
        return image

    def draw(self, scr):
        scr.blit(self.image, self.rect)
    
    def fall(self, target_y):
        
        #Moves the block downward until it aligns with the target position.

        if self.rect.y < target_y:
            self.rect.y += 2  # Adjust the speed of the fall (2 pixels per frame)
            if self.rect.y > target_y:  # Ensure it doesn't overshoot
                self.rect.y = target_y

    def draw_health_bar(self, scr, be, health):
        # Black background for the health bar
        be.rect(scr, "black", (self.rect.x + 5, self.rect.y + 5, 65, 7))
        # Green health bar proportional to the block's health
        health_width = int(65 * (self.health / 100))
        health.rect(scr, "green", (self.rect.x + 5, self.rect.y + 5, health_width, 7))
    

def blockgen(rows, columns, x_start, y_start, left=True):
    blocks = []
    for i in range(rows):
        row = []
        for j in range(columns):
            x = x_start + ((p-5) * j) if left else x_start - ((p-5) * j)
            y = y_start - ((p-5) * i)
            block_type = random.randint(1, 4)
            row.append(Block(block_type, x, y))
        blocks.append(row)
    return blocks

# Generate blocks for left and right sides
row = 4
column = 3
block_rect_l = blockgen(row, column, 0, 440, left=True)
block_rect_r = blockgen(row, column, 1125, 440, left=False)

def block_draw_left(blocks, scr):
    for row in blocks:
        for block in row:
            if block is not None:
                block.draw(scr)

def block_draw_right(blocks, scr):
    for row in blocks:
        for block in row:
            if block is not None:
                block.draw(scr)

def energy_bars(blocks, scr, be, health):
    for row in blocks:
        for block in row:
            if block is not None:
                block.draw_health_bar(scr, be, health)