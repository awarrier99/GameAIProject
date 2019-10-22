import pygame

from Player import Player
from util import Loc, Keys, Actions
from VisualSensors import VisualSensors
from World import World

from argparse import ArgumentParser


class Game:
    def __init__(self, cfg):
        self._running = True
        self.screen = None
        self.size = self.width, self.height = cfg['width'] or 1085, cfg['height'] or 735
        self.ppg = cfg['ppg'] or 35
        self.__ai_mode = cfg['ai']
        self._enable_dirty_rects = cfg['dirty_rects']
        self.world = World((self.width, self.height), self.ppg, cfg['move_frames'], self.__ai_mode, self._enable_dirty_rects)
        self.player = Player(self.world.to_pixels(Loc(2, 2)))
        self.all_sprites = None
        self.world.player = self.player
        self.background = None
        self.clock = pygame.time.Clock()
        self.FPS = cfg['fps'] or 60
        self.playtime = 0
        self._enable_visuals = not cfg['novisuals']
        self.visual_sensors = None
        self.last_grid = (0, 0)
        self.mouse_down = False
        self.key_1 = False
        self.key_2 = False

    def setup(self):
        if self.__ai_mode:
            print('Running in AI mode. Move controls disabled')
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWACCEL | pygame.DOUBLEBUF)
        if self._enable_visuals:
            self.visual_sensors = VisualSensors(self.player, self.world.to_pixels, self.world.ppg, *self.size)
        pygame.display.set_caption("James and Ashvin's (autistic) 'AI'")

        if self._enable_dirty_rects:
            self.all_sprites = pygame.sprite.LayeredDirty(self.player)
        else:
            self.all_sprites = pygame.sprite.Group()
            self.all_sprites.add(self.player)
            self.all_sprites.add(*self.world.colliders)

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 155, 155))
        self.background = self.background.convert()
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.clear(self.screen, self.background)

    def redraw(self):
        if not self._enable_dirty_rects:
            self.screen.blit(self.background, (0, 0))
        wall_rects, old_wall_rects = self.world.draw(self.screen, self.background)
        dirty_rects = self.all_sprites.draw(self.screen)
        if self._enable_visuals:
            self.visual_sensors.draw(self.screen, self.world.path, self.world.goal_loc)
        if self._enable_dirty_rects:
            pygame.display.update(dirty_rects + wall_rects + old_wall_rects)
        else:
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
            pygame.display.set_caption("James and Ashvin's (autistic) 'AI'  FPS: " + str(round(self.clock.get_fps(), 1)))
            self.check_event_queue()
            if not self.__ai_mode:
                self.handle_keys(pygame.key.get_pressed())
            self.all_sprites.update()
            if self._enable_visuals:
                self.visual_sensors.update()
            self.world.update()
            self.redraw()

    def cleanup(self):
        self.background = self.screen = self.all_sprites = None
        self.world.ai._pool.terminate()
        self.world.ai._pool.join()
        pygame.quit()

    def run(self):
        self.setup()
        self.mainloop()
        self.cleanup()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--novisuals', action='store_true', help='whether to show visual sensors for debugging')
    parser.add_argument('-w', '--width', type=int, help='width of the game screen')
    parser.add_argument('-t', '--height', type=int, help='height of the game screen')
    parser.add_argument('-p', '--ppg', type=int, help='pixels per grid position')
    parser.add_argument('-f', '--fps', type=int, help='frames per second')
    parser.add_argument('-m', '--move-frames', type=int, help='number of frames to move for')
    parser.add_argument('-a', '--ai', action='store_true', help='whether to run in AI mode')
    parser.add_argument('-d', '--dirty-rects', action='store_true', help='whether to use dirty rect rendering')
    config = vars(parser.parse_args())
    game = Game(config)
    game.run()
