import pygame

from Player import Player
from util import Loc


class Game:
    def __init__(self):
        self._running = True
        self.screen = None
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(Loc(100, 100))
        self.background = None
        self.size = self.width, self.height = 640, 400
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.playtime = 0

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), pygame.HWACCEL | pygame.DOUBLEBUF)
        pygame.display.set_caption("James and Ashvins Autistic AI")

        self.all_sprites.add(self.player)

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 155, 155))
        self.background = self.background.convert()
        self.screen.blit(self.background, (0, 0))

    def redraw(self):
        self.screen.blit(self.background, (0, 0))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def check_event_queue(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                if event.key == pygame.K_RIGHT:
                    self.player.loc.x += 3
                    self.player.rect.center = (self.player.loc.x, self.player.loc.y)

    def mainloop(self):
        pygame.key.set_repeat(1)
        while self._running:
            milliseconds = self.clock.tick(self.FPS)
            self.playtime += milliseconds / 1000.0
            self.check_event_queue()
            self.all_sprites.update()
            self.redraw()

    def cleanup(self):
        self.background = self.screen = self.all_sprites = None
        pygame.quit()

    def run(self):
        self.setup()
        self.mainloop()
        self.cleanup()


if __name__ == "__main__":
    game = Game()
    game.run()
