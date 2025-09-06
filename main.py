import pygame
import random
pygame.init()

# Basic necessary things
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-Game")
clock = pygame.time.Clock()

# Definition of game elements
# Player
player_x, player_y = 50, 50
player_width, player_height = 50, 50
player = pygame.Rect(player_x, player_y, player_width, player_width)
player_speed = 5
player_color = (255, 0, 0)
# Target
target_x, target_y = 300, 200
target_width, target_height = 20, 20
target = pygame.Rect(target_x, target_y, target_width, target_height)
target_color = (0, 200, 0)
# Score
score = 0
score_color = (10, 10)
# Obstacle
obstacle = pygame.Rect(340, 240, 60, 60)
obstacle_color = (125, 137, 215)

# Start of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
# Game logic

    # Player and target collision
    if player.colliderect(target):
        target.x = random.randint(0, WIDTH - target_width)
        target.y = random.randint(0, HEIGHT - target_height)
        score += 1

    # Player and obstacle collision
    if player.colliderect(obstacle):
        score = 0
        player.x, player.y = 50, 50
         
    # Player Moving
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

# Security to not go across the borders
    player.x = max(0, min(WIDTH - player_width, player.x))
    player.y = max(0, min(HEIGHT - player_height, player.y))

# Display the elements
    # Background
    screen.fill((25,25,25))
    # Obstacle
    pygame.draw.rect(screen, obstacle_color, obstacle)
    # Target
    pygame.draw.rect(screen, target_color, target)
    # Player
    pygame.draw.rect(screen, player_color, player)
    # Score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, score_color)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()