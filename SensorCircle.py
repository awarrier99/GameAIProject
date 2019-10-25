import pygame


class SensorCircle(pygame.Rect):

    def __init__(self, range):
        pygame.Rect.__init__(self, 0, 0, range, range)
