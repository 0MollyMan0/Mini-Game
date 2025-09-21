import pygame

def load_sounds():
    return {
        "collect": pygame.mixer.Sound("assets/sounds/collect-coin-8bit.mp3"),
        "hit": pygame.mixer.Sound("assets/sounds/hurt-8bit.mp3"),
        "win": pygame.mixer.Sound("assets/sounds/win-8bit.mp3"),
        "lose": pygame.mixer.Sound("assets/sounds/lose-8bit.mp3"),
        "boost": pygame.mixer.Sound("assets/sounds/speed-boost-8bit.wav"),
    }

def load_fonts():
    return {
        "title": pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 100),
        "big": pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 48),
        "default": pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 24),
    }