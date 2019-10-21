import pygame

from World import World
from Player import Player
from util import Loc, Keys, Actions


class Game:
    def __init__(self):
        self._running = True
        self.screen = None
        self.all_sprites = pygame.sprite.Group()
        self.size = self.width, self.height = 658, 420
        self.player_step = 7
        self.world = World((int(self.width / self.player_step), int(self.height / self.player_step)), self.player_step)
        self.player = Player(Loc(33, 33))
        self.background = None
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

                self.handle_keys(event.key)

    def handle_keys(self, keys):
        if Keys.keyright(keys):
            self.world.move(self.player, Actions.R)
        if Keys.keyleft(keys):
            self.world.move(self.player, Actions.L)
        if Keys.keyup(keys):
            self.world.move(self.player, Actions.U)
        if Keys.keydown(keys):
            self.world.move(self.player, Actions.D)

    def mainloop(self):
        while self._running:
            milliseconds = self.clock.tick(self.FPS)
            self.playtime += milliseconds / 1000.0
            self.check_event_queue()
            self.handle_keys(pygame.key.get_pressed())
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
