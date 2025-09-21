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

class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = font.render(text, True, (0, 0, 0))
        self.default_color = (200, 200, 200)
        self.hover_color = (250, 250, 250)
        self.bg_color = self.default_color
        self.font = font

    def update(self):
        if self.is_hover():
            self.bg_color = self.hover_color
        else:
            self.bg_color = self.default_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect) 
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and 
            event.button == 1 and 
            self.rect.collidepoint(event.pos)
        )
    
    def is_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)