import pygame
import random
pygame.init()
pygame.mixer.init()

# Basic necessary things
WIDTH, HEIGHT = 1200, 800
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
win_score = 1
# Obstacles
obstacles = [
    pygame.Rect(300, 150, 40, 40),
    pygame.Rect(300, 400, 40, 40),
    pygame.Rect(300, 650, 40, 40),
    pygame.Rect(600, 150, 40, 40),
    pygame.Rect(600, 400, 40, 40),
    pygame.Rect(600, 650, 40, 40),
    pygame.Rect(900, 150, 40, 40),
    pygame.Rect(900, 400, 40, 40),
    pygame.Rect(900, 650, 40, 40),
]
obstacle_color = (125, 137, 215)
# Chrono
start_ticks = pygame.time.get_ticks()
time_limit = 10  # in seconds
timer_position = (WIDTH-175, 10)
# Sounds
collect_sound = pygame.mixer.Sound("sounds/collect-coin-8bit.mp3")
hit_sound = pygame.mixer.Sound("sounds/hurt-8bit.mp3")
win_sound = pygame.mixer.Sound("./sounds/win-8bit.mp3")
lose_sound = pygame.mixer.Sound("./sounds/lose-8bit.mp3")
# Constant
end = False
waiting = False
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
        sound_played = False
        end = True

    # Player and target collision
    if player.colliderect(target):
        collect_sound.play()
        target.x = random.randint(0, WIDTH - target_width)
        target.y = random.randint(0, HEIGHT - target_height)
        score += 1

    # Player and obstacle collision
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            hit_sound.play()
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
    # Obstacles
    for obstacle in obstacles:
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
    # End Screen
    if end:
        # To play the final sound 1 time per party
        if not sound_played:
            # if Win
            if score >= win_score:
                win_sound.play()
                end_game_text = end_game_font.render("WIN", True, (0,255,0))
                screen.blit(end_game_text, (WIDTH/2 - 90, HEIGHT/2 - 100))
            # if Lose
            else:
                lose_sound.play()
                end_game_text = end_game_font.render("GAME OVER", True, (255,0,0))
                screen.blit(end_game_text, (WIDTH/2 - 220, HEIGHT/2 - 100))
            sound_played = True
        # Final Score
        final_score_text = font.render(f"Final Score: {score}", True, white)
        screen.blit(final_score_text, (WIDTH//2 - 170, HEIGHT//2 - 20))
        # Indication to restart or quit
        final_indication_text = font.render(f"Press R to Restart / Q to Quit", True, white)
        screen.blit(final_indication_text, (WIDTH//2 - 355, HEIGHT//2 + 100))
        # Refresh Screen
        pygame.display.flip()
        # To restart
        pygame.event.clear()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart
                        score = 0
                        player.x, player.y = 50, 50
                        target.x, target.y = 300, 200
                        end = False
                        waiting = False
                        start_ticks = pygame.time.get_ticks()
                    elif event.key == pygame.K_q:
                        waiting = False
                        running = False
                elif event.type == pygame.QUIT:
                        waiting = False
                        running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()