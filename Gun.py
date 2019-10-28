import pygame


class Gun(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Pistol(Gun):

    def __init__(self, loc):
        super().__init__()
        self.fire_delay = 30
        self.damage = 10
        self.ammo = 15
        self.image = pygame.image.load('GunSprites/pistol_1.png')
        self.rect = self.image.get_rect()
        self.rect.center = loc.as_tuple()


class SubMachine1(Gun):

    def __init__(self, loc):
        super().__init__()
        self.fire_delay = 12
        self.damage = 5
        self.ammo = 25
        self.image = pygame.image.load('GunSprites/submachinegun_1.png')
        self.rect = self.image.get_rect()
        self.rect.center = loc.as_tuple()


class SubMachine2(Gun):

    def __init__(self, loc):
        super().__init__()
        self.fire_delay = 8
        self.damage = 4
        self.ammo = 25
        self.image = pygame.image.load('GunSprites/submachinegun_2.png')
        self.rect = self.image.get_rect()
        self.rect.center = loc.as_tuple()


class AssualtRifle1(Gun):

    def __init__(self, loc):
        super().__init__()
        self.fire_delay = 17
        self.damage = 8
        self.ammo = 30
        self.image = pygame.image.load('GunSprites/assualtrifle_1.png')
        self.rect = self.image.get_rect()
        self.rect.center = loc.as_tuple()


class AssualtRifle2(Gun):

    def __init__(self, loc):
        super().__init__()
        self.fire_delay = 15
        self.damage = 10
        self.ammo = 30
        self.image = pygame.image.load('GunSprites/assualtrifle_2.png')
        self.rect = self.image.get_rect()
        self.rect.center = loc.as_tuple()



