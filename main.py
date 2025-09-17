import pygame
from game.settings import *
from game.entities import *
from game.utils import *
from game.assets import *

pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Window
pygame.display.set_caption("Mini-Game") # Name of the window
clock = pygame.time.Clock() # Time
sounds = load_sounds() # Pre load all the sounds
fonts = load_fonts() # Pre load all the fonts

# Chrono
start_ticks = pygame.time.get_ticks()

# Player
player = Player(50, 50, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED)

# Obstacles
obstacles = [
    Obstacle(300, 150, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(300, 400, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(300, 650, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(600, 150, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(600, 400, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(600, 650, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(900, 150, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(900, 400, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
    Obstacle(900, 650, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR),
]

# Target
target = Target(300, 200, TARGET_WIDTH, TARGET_HEIGHT, TARGET_COLOR, 1)

# Boost
boosts = [
    Boost(10 , 10, BOOST_WIDTH, BOOST_HEIGHT, BOOST_COLOR),
    Boost(20, 20, BOOST_WIDTH, BOOST_HEIGHT, BOOST_COLOR),
    Boost(30, 30, BOOST_WIDTH, BOOST_HEIGHT, BOOST_COLOR),
]

# Start of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Game logic
    # Chrono
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    if elapsed_time >= TIME_LIMIT:
        end = True

    # Player and target collision
    if player.colliderect(target):
        sounds["collect"].play()
        score += 1
        valid_position = False
        while not valid_position:
            target.x = random.randint(0, WIDTH - TARGET_WIDTH)
            target.y = random.randint(0, HEIGHT - TARGET_HEIGHT)
            valid_position = True
            for obstacle in obstacles: 
                if target.colliderect(obstacle):
                    valid_position = False
                    break
    
    # Player and accelerators
    if speed_boost_start is not None:
        if pygame.time.get_ticks() - speed_boost_start > 2000:  # 2 secondes de boost
            PLAYER_SPEED = 5
            speed_boost_start = None

    for boost in boosts:
        if player.colliderect(boost):
            speed_boost_start = pygame.time.get_ticks()
            PLAYER_SPEED = 7
            sounds["boost"].play()
            valid_position = False
            while not valid_position:
                target.x = random.randint(0, WIDTH - TARGET_WIDTH)
                target.y = random.randint(0, HEIGHT - TARGET_HEIGHT)
                if not is_colli_others(target, obstacles):
                    valid_position = True

    # Player and obstacle collision
    if is_colli_others(player, obstacles):
        sounds["hit"].play()
        score = 0
        player.x, player.y = 50, 50
         
    # Player Moving
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Security to not go across the borders
    player.x = max(0, min(WIDTH - PLAYER_WIDTH, player.x))
    player.y = max(0, min(HEIGHT - PLAYER_HEIGHT, player.y))

# Display the elements
    # Background
    screen.fill((25,25,25))
    # Obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)
    # Accelerators
    for boost in boosts:
        pygame.draw.rect(screen, BOOST_COLOR, boost)
    # Target
    pygame.draw.rect(screen, TARGET_COLOR, target)
    # Player
    pygame.draw.rect(screen, PLAYER_COLOR, player)
    # Score
    score_text = fonts["default"].render(f"Score:{score}", True, WHITE)
    screen.blit(score_text, SCORE_POSITION)
    # Chrono
    timer_text = fonts["default"].render(f"Time:{TIME_LIMIT - elapsed_time}", True, WHITE)
    screen.blit(timer_text, TIMER_POSITION)
    # End Screen
    if end:
        # if Win
        if score >= WIN_SCORE:
            sounds["win"].play()
            end_game_text = fonts["end"].render("WIN", True, (0,255,0))
            screen.blit(end_game_text, (WIDTH/2 - 90, HEIGHT/2 - 100))
        # if Lose
        else:
            sounds["lose"].play()
            end_game_text = fonts["end"].render("GAME OVER", True, (255,0,0))
            screen.blit(end_game_text, (WIDTH/2 - 220, HEIGHT/2 - 100))
        # Final Score
        final_score_text = fonts["default"].render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (WIDTH//2 - 170, HEIGHT//2 - 20))
        # Indication to restart or quit
        final_indication_text = fonts["default"].render(f"Press R to Restart / Q to Quit", True, WHITE)
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
    clock.tick(FPS)

pygame.mixer.quit()
pygame.quit()