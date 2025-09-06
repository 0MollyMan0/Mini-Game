import pygame
pygame.init()

# Basic necessary things
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-Game")
clock = pygame.time.Clock()

# Definition of game elements
player_x, player_y = 50, 50
player_width, player_height = 50, 50
player = pygame.Rect(player_x, player_y, player_width, player_width)
player_speed = 5
blue_rectangle = pygame.Rect(700, 500, 80, 40)

# Start of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
# Game logic
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
    screen.fill((25,25,25))
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 0, 255), blue_rectangle)
    pygame.draw.circle(screen, (0, 255, 0), (400, 300), 30)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()