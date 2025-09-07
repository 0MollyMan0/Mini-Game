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
score_position = (10, 10)
# Obstacle
obstacle = pygame.Rect(340, 240, 60, 60)
obstacle_color = (125, 137, 215)
# Chrono
start_ticks = pygame.time.get_ticks()
time_limit = 20  # in seconds
timer_position = (WIDTH-175, 10)
# Constant
white = (255, 255, 255)
end_game_font = pygame.font.Font("./font/PressStart2P-Regular.ttf", 48)
font = pygame.font.Font("./font/PressStart2P-Regular.ttf", 24)

# Start of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
# Game logic

    # Chrono
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    if elapsed_time >= time_limit:
        if score >= 10:
            end_game_text = end_game_font.render("WIN", True, (0,255,0))
            screen.blit(end_game_text, (WIDTH/2 - 100, HEIGHT/2 - 100))
        else:
            end_game_text = end_game_font.render("GAME OVER", True, (255,0,0))
            screen.blit(end_game_text, (WIDTH/2 - 220, HEIGHT/2 - 100))
        pygame.display.flip()
        pygame.time.delay(5000)  # attendre 5 secondes
        running = False

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
    score_text = font.render(f"Score:{score}", True, white)
    screen.blit(score_text, score_position)
    # Chrono
    timer_text = font.render(f"Time:{time_limit - elapsed_time}", True, white)
    screen.blit(timer_text, timer_position)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()