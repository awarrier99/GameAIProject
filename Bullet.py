import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, loc, dir):
        pygame.sprite.Sprite.__init__(self)
        self.loc = loc
        self.dir = dir
        self.image = pygame.Surface((10, 2))
        self.image = pygame.transform.rotozoom(self.image, dir, 1)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (loc.x, loc.y)

    def update(self):
        pass
