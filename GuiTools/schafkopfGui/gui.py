import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schafkopf GUI")
GREEN = (51, 255, 51)
FPS = 60


def drawWindow():
    WIN.fill(GREEN)
    pygame.display.update()


def drawGameState()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.
        drawWindow()
    pygame.quit()


if __name__ == "__main__":
    main()
