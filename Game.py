import pygame

from Player import Player

pygame.init()
screen = pygame.display.set_mode((640,480),)
pygame.display.set_caption("James and Ashvins Autistic AI")
# ------ constants ------------
clock = pygame.time.Clock()
mainloop = True
FPS = 30
playtime = 0
# ------- background ---------
background = pygame.Surface(screen.get_size())
background.fill((255,155,155))
background = background.convert()
screen.blit(background, (0,0))

# -------- sprites ---------
player = Player((100, 100))

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

def redraw_game_window():

    screen.blit(background, (0, 0))

    all_sprites.draw(screen)
    pygame.display.flip()


# --------- mainloop ----------
while mainloop:

    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    all_sprites.update()
    redraw_game_window()

