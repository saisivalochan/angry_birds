import pygame
import sys

projectiles_l = []
projectiles_r = []
max_drag = 100
wind = pygame.math.Vector2(0, 0)  # Global wind vector

def set_wind(speed, direction):
    
    #Sets the wind vector based on speed and direction.

    global wind
    wind = pygame.math.Vector2(speed, 0).rotate_rad(direction)

def draw_trajectory(screen, start, vel, acc, num_dots=10, t_step=1, color=(0,0,0), radius=4):

    #Draws num_dots small circles along the parabolic path

    for i in range(1, num_dots + 1):
        t = i * t_step
        pos = start + vel * t - 0.5 * acc * t**2
        pygame.draw.circle(screen, color, (int(pos.x), int(pos.y)), radius)

class projectile:
    def __init__(self,image,pos,velocity,acceleration = (0,0),bird_type = None):
        self.image = image
        self.rect = image.get_rect(center = pos)
        self.vel = pygame.math.Vector2(velocity)
        self.acc = pygame.math.Vector2(acceleration)
        self.bird_type = bird_type
    def draw(self,scr):
        scr.blit(self.image,self.rect)

    def update(self):
        self.acc += wind
        if self.vel.x != 0:
            self.vel.x += self.acc.x
        if self.vel.y != 0:
            self.vel.y += self.acc.y
        self.rect.x -= self.vel.x
        self.rect.y -= self.vel.y
def get_collision_side(rect1, rect2):
    
    #Determines which side of rect1 is collided with rect2.

    
    # Calculate the differences between the edges of the rectangles
    
    dx_left = abs(rect1.left - rect2.right)  # Distance from rect2's right to rect1's left
    dx_right = abs(rect1.right - rect2.left)  # Distance from rect2's left to rect1's right
    dy_top = abs(rect1.top - rect2.bottom)  # Distance from rect2's bottom to rect1's top
    dy_bottom = abs(rect1.bottom - rect2.top)  # Distance from rect2's top to rect1's bottom

    # Find the smallest difference to determine the collision side
    min_diff = min(dx_left, dx_right, dy_top, dy_bottom)

    if min_diff == dy_top:
        return "top"
    elif min_diff == dy_bottom:
        return "bottom"
    elif min_diff == dx_left:
        return "left"
    elif min_diff == dx_right:
        return "right"