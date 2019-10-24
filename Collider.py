import pygame


class Collider(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        blue = 0, 0, 128
        self.image = pygame.Surface((34, 34))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = loc.as_tuple()

    def update(self):
        pass
