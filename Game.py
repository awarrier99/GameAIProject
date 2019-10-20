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
player = Player((50, 50))
walk_count = 0
max_walk_count = 19


def redraw_game_window():
    global walk_count
    global player
    screen.blit(background, (0, 0))

    if walk_count > max_walk_count:
        walk_count = 0

    screen.blit(player.feet_walk[walk_count//3], player.location)
    screen.blit(player.rifle_walk[walk_count//3], player.location)
    walk_count += 1
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

    redraw_game_window()

