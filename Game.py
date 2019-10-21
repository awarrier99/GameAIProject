import pygame

from Player import Player
from util import Loc, Keys, Actions
from VisualSensors import VisualSensors
from World import World


class Game:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = 665, 437
        self.all_sprites = pygame.sprite.Group()
        self.player_step = 19
        self.world = World((self.width, self.height), self.player_step)
        self.player = Player(self.world.to_pixels(Loc(2, 2)))
        self.world.player = self.player
        self.background = None
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.playtime = 0
        self.visual_sensors = None
        self.last_grid = (0, 0)
        self.mouse_down = False
        self.key_1 = False
        self.key_2 = False

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWACCEL | pygame.DOUBLEBUF)
        self.visual_sensors = VisualSensors(self.player)
        pygame.display.set_caption("James and Ashvin's (autistic) 'AI'")

        self.all_sprites.add(self.player)

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 155, 155))
        self.background = self.background.convert()
        self.screen.blit(self.background, (0, 0))

    def redraw(self):
        self.screen.blit(self.background, (0, 0))
        self.world.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.visual_sensors.draw(self.screen)
        pygame.display.flip()

    def check_event_queue(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                if event.key == pygame.K_1:
                    self.key_1 = True
                if event.key == pygame.K_2:
                    self.key_2 = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self.key_1 = False
                if event.key == pygame.K_2:
                    self.key_2 = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                self.last_grid = (0, 0)
        if self.mouse_down and self.key_1:
            self.last_grid = self.world.create_wall(self.last_grid)
        if self.mouse_down and self.key_2:
            x, y = pygame.mouse.get_pos()
            self.world.goal_loc = self.world.to_grids(Loc(x, y))

    def handle_keys(self, keys):
        if Keys.upright(keys):
            self.world.move(self.player, Actions.UR)
        elif Keys.downright(keys):
            self.world.move(self.player, Actions.DR)
        elif Keys.right(keys):
            self.world.move(self.player, Actions.R)
        elif Keys.upleft(keys):
            self.world.move(self.player, Actions.UL)
        elif Keys.downleft(keys):
            self.world.move(self.player, Actions.DL)
        elif Keys.left(keys):
            self.world.move(self.player, Actions.L)
        elif Keys.up(keys):
            self.world.move(self.player, Actions.U)
        elif Keys.down(keys):
            self.world.move(self.player, Actions.D)

    def mainloop(self):
        while self._running:
            milliseconds = self.clock.tick(self.FPS)
            self.playtime += milliseconds / 1000.0
            self.check_event_queue()
            self.handle_keys(pygame.key.get_pressed())
            self.all_sprites.update()
            self.visual_sensors.update()
            self.world.update()
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
