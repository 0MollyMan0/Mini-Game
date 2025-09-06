import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Window")

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((25,25,25))

    red_rectangle = pygame.Rect(50, 50, 50, 50)
    blue_rectangle = pygame.Rect(700, 500, 80, 40)
    pygame.draw.rect(screen, (255, 0, 0), red_rectangle)
    pygame.draw.rect(screen, (0, 0, 255), blue_rectangle)
    pygame.draw.circle(screen, (0, 255, 0), (400, 300), 30)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()