import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("MINU ESIMENE MANG")

font = pygame.font.SysFont("arial", 50)
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 35))

    text = font.render("MANG TOOTAB!", True, (0, 255, 255))
    screen.blit(text, (250, 200))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
