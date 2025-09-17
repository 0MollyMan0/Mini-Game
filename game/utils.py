import random
import pygame
from game.settings import WIDTH, HEIGHT

def is_colli_others(rect, others):
    for other in others:
        if rect.colliderect(other):
            return True
    return False

# Search a correct random position
def random_position(width, height, obstacles=[], extra_rects=[]):
    rect = pygame.Rect(0, 0, width, height)
    valid_position = False
    attempts = 0
    MAX_ATTEMPTS = 200

    while not valid_position and attempts < MAX_ATTEMPTS:
        rect.x = random.randint(0, WIDTH - width)
        rect.y = random.randint(0, HEIGHT - height)
        attempts += 1

        if (not is_colli_others(rect, obstacles)
                and all(not rect.colliderect(r) for r in extra_rects)):
            valid_position = True

    return rect
