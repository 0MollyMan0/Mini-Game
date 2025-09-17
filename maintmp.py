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

# Score
score = 0
# Accelerators
accelerator_width, accelerator_height = 30, 30
accelerators = [
    pygame.Rect(random.randint(0, WIDTH - accelerator_width), random.randint(0, HEIGHT - accelerator_height), accelerator_width, accelerator_height),
    pygame.Rect(random.randint(0, WIDTH - accelerator_width), random.randint(0, HEIGHT - accelerator_height), accelerator_width, accelerator_height),
    pygame.Rect(random.randint(0, WIDTH - accelerator_width), random.randint(0, HEIGHT - accelerator_height), accelerator_width, accelerator_height),
]
accelerator_color = (249, 255, 36)
speed_boost_start = None
# Chrono
start_ticks = pygame.time.get_ticks()
# Constant
end = False
waiting = False
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
        end = True

    # Player and target collision
    if player.colliderect(target):
        collect_sound.play()
        score += 1
        valid_position = False
        while not valid_position:
            target.x = random.randint(0, WIDTH - target_width)
            target.y = random.randint(0, HEIGHT - target_height)
            valid_position = True
            for obstacle in obstacles: 
                if target.colliderect(obstacle):
                    valid_position = False
                    break
    
    # Player and accelerators
    if speed_boost_start is not None:
        if pygame.time.get_ticks() - speed_boost_start > 2000:  # 2 secondes de boost
            player_speed = 5
            speed_boost_start = None

    for accelerator in accelerators:
        if player.colliderect(accelerator):
            speed_boost_start = pygame.time.get_ticks()
            player_speed = 7
            accelerator_sound.play()
            valid_position = False
            while not valid_position:
                target.x = random.randint(0, WIDTH - target_width)
                target.y = random.randint(0, HEIGHT - target_height)
                if not is_colli_obstacles(target, obstacles):
                    valid_position = True

    # Player and obstacle collision
    if is_colli_obstacles(player, obstacles):
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
    # Accelerators
    for accelerator in accelerators:
        pygame.draw.rect(screen, accelerator_color, accelerator)
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