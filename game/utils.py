import random
import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT

def is_colli_others(rect, others):
    for other in others:
        if rect.colliderect(other):
            return True
    return False

# Search a correct and random position
def random_position(width, height, others=[]):
    rect = pygame.Rect(0, 0, width, height)
    valid_position = False
    attempts = 0
    MAX_ATTEMPTS = 200

    while not valid_position and attempts < MAX_ATTEMPTS:
        rect.x = random.randint(0, SCREEN_WIDTH - width)
        rect.y = random.randint(0, SCREEN_HEIGHT - height)
        attempts += 1

        if (not is_colli_others(rect, others)):
            valid_position = True

    return rect

def draw_overlay(screen, color=(0, 0, 0), alpha=150):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*color, alpha))  
    screen.blit(overlay, (0, 0))
