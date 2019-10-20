import pygame
from pygame.locals import *

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

    move_ticker = 0
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        if move_ticker == 0:
            move_ticker = 6
            player.direction += 3

    if keys[K_RIGHT]:
        if move_ticker == 0:
            move_ticker = 6
            player.direction -= 3
    if keys[K_w]:
        if move_ticker == 0:
            move_ticker = 6
            player.y -= 3
    if keys[K_a]:
        if move_ticker == 0:
            move_ticker = 6
            player.x -= 3
    if keys[K_s]:
        if move_ticker == 0:
            move_ticker = 6
            player.y += 3
    if keys[K_d]:
        if move_ticker == 0:
            move_ticker = 6
            player.x += 3

    if move_ticker > 0:
        move_ticker -= 1


    all_sprites.update()
    redraw_game_window()

