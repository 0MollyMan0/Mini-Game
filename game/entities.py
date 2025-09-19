import pygame
from game.utils import *

class Entity:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Player(Entity):
    def __init__(self, x, y, size, color, speed):
        super().__init__(x, y, size, size, color)
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Obstacle(Entity):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)

class Target(Entity):
    def __init__(self, x, y, w, h, color, value):
        super().__init__(x, y, w, h, color)
        self.value = value
        
class Boost(Entity):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)
        self.active = False
        self.start = None
