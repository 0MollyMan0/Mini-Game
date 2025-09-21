import pygame
from game.settings import *
from game.entities import *
from game.utils import *
from game.assets import *

pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Window
pygame.display.set_caption("Mini-Game") # Name of the window
clock = pygame.time.Clock() # Time
sounds = load_sounds() # Pre load all the sounds
fonts = load_fonts() # Pre load all the fonts

# Buttons
play_button = Button(PLAY_BUTTON_X, PLAY_BUTTON_Y, PLAY_BUTTON_WIDTH, PLAY_BUTTON_HEIGHT, "PLAY", fonts["big"])

# Timer
start_ticks = None

# Player
player = Player(PLAYER_INIT_X, PLAYER_INIT_Y, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED)

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
target = Target(0, 0, TARGET_WIDTH, TARGET_HEIGHT, TARGET_COLOR, 1)
target.rect = random_position(TARGET_WIDTH, TARGET_HEIGHT, obstacles)

# Boost
boosts = [
    Boost(0, 0, BOOST_WIDTH, BOOST_HEIGHT, BOOST_COLOR),
    Boost(0, 0, BOOST_WIDTH, BOOST_HEIGHT, BOOST_COLOR),
    Boost(0, 0, BOOST_WIDTH, BOOST_HEIGHT, BOOST_COLOR),
]
for boost in boosts:
    boost.rect = random_position(BOOST_WIDTH, BOOST_HEIGHT, obstacles)

# Others
score = 0
end = False
game_started = False

# Start of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ########
    # Menu #
    ########
    if not game_started:
        screen.fill((25,25,25))
        title_text = fonts["title"].render("Mini Game", True, WHITE)
        screen.blit(title_text, TITLE_POSITION)
        credits_text = fonts["default"].render("by MollyMan", True, WHITE)
        screen.blit(credits_text, CREDITS_POSITION)
        play_button.draw(screen)
        pygame.display.flip()
        play_button.update()
        if play_button.is_clicked(event):
            game_started = True
    ########
    # Game #
    ########
    else:
        if start_ticks is None:
            start_ticks = pygame.time.get_ticks()
    
    # Timer
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        if elapsed_time >= TIME_LIMIT:
            end = True

        # Player and target collision
        if player.rect.colliderect(target):
            sounds["collect"].play()
            score += 1
            valid_position = False
            target.rect = random_position(TARGET_WIDTH, TARGET_HEIGHT, obstacles+boosts)
        
        # Boosts
        for boost in boosts:
            # Player and Boosts
            if player.rect.colliderect(boost):
                boost.start = pygame.time.get_ticks()
                sounds["boost"].play()
                boost.rect.x, boost.rect.y = -100, -100
                boost.active = True
            # Boost re-activation
            if boost.active and pygame.time.get_ticks() - boost.start > BOOST_TIME_EFFECT:
                boost.active = False
            if boost.start != None and pygame.time.get_ticks() - boost.start > BOOST_TIME_RESPAWN:
                boost.rect = random_position(BOOST_WIDTH, BOOST_HEIGHT, obstacles+boosts)
                boost.start = None
        player.speed = PLAYER_SPEED_BOOST if any(b.active for b in boosts) else PLAYER_SPEED

        # Player and obstacle collision
        if is_colli_others(player.rect, obstacles):
            sounds["hit"].play()
            score = 0
            player.rect.x, player.rect.y = 50, 50
            
        # Player Moving
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Security to not go across the borders
        player.rect.x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, player.rect.x))
        player.rect.y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, player.rect.y))

    # Display the elements
        # Background
        screen.fill((25,25,25))
        # Obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        # Accelerators
        for boost in boosts:
            boost.draw(screen)
        # Target
        target.draw(screen)
        # Player
        player.draw(screen)
        # Score
        score_text = fonts["default"].render(f"Score:{score}", True, WHITE)
        screen.blit(score_text, SCORE_POSITION)
        # Timer
        timer_text = fonts["default"].render(f"Time:{TIME_LIMIT - elapsed_time}", True, WHITE)
        screen.blit(timer_text, TIMER_POSITION)
        ##############
        # End Screen #
        ##############
        if end:
            # if Win
            if score >= WIN_SCORE:
                sounds["win"].play()
                end_game_text = fonts["big"].render("WIN", True, (0,255,0))
                screen.blit(end_game_text, (SCREEN_WIDTH/2 - 90, SCREEN_HEIGHT/2 - 100))
            # if Lose
            else:
                sounds["lose"].play()
                end_game_text = fonts["big"].render("GAME OVER", True, (255,0,0))
                screen.blit(end_game_text, (SCREEN_WIDTH/2 - 220, SCREEN_HEIGHT/2 - 100))
            # Final Score
            final_score_text = fonts["default"].render(f"Final Score: {score}", True, WHITE)
            screen.blit(final_score_text, (SCREEN_WIDTH//2 - 170, SCREEN_HEIGHT//2 - 20))
            # Indication to restart or quit
            final_indication_text = fonts["default"].render(f"Press R to Restart / Q to Quit", True, WHITE)
            screen.blit(final_indication_text, (SCREEN_WIDTH//2 - 355, SCREEN_HEIGHT//2 + 100))
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