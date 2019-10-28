import pygame
import settings

from Player import Player
from util import PixelLoc, GridLoc, Keys, Actions, Colors
from VisualSensors import VisualSensors
from World import World
from Workers import Workers
from Gun import Gun


class Game:
    def __init__(self):
        self.__running = True
        self.screen = None
        self.player = Player(GridLoc(2, 2).to_pixel())
        self.world = World(self.player)
        self.all_sprites = None
        self.background = None
        self.clock = pygame.time.Clock()
        self.playtime = 0
        self.visual_sensors = None
        self.last_grid = GridLoc(-1, -1)
        self.input_map = {}
        self.input_debounce = 0

    def setup(self):
        if settings.ai_mode:
            print('Running in AI mode. Move controls disabled')
        pygame.init()
        self.screen = pygame.display.set_mode(settings.size, pygame.HWACCEL | pygame.DOUBLEBUF)
        self.visual_sensors = [VisualSensors(self.player, *settings.size)]
        pygame.display.set_caption('James and Ashvin\'s Game \'AI\'')

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 155, 155))
        self.background = self.background.convert()

        if settings.dirty_rects:
            self.all_sprites = pygame.sprite.LayeredDirty(self.player)
            self.all_sprites.clear(self.screen, self.background)
        else:
            self.all_sprites = pygame.sprite.Group(*self.world.colliders, *self.world.guns, self.player)

        self.screen.blit(self.background, (0, 0))

    def draw_stats(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        actor = 'AI' if settings.ai_mode else 'Player'
        stat_str = '{}: {} (grid) | {} (pixels) | {} degrees (direction)'
        stats = stat_str.format(actor, self.player.loc.to_grid(), self.player.loc, round(self.player.direction, 2))
        text = font.render(stats, True, Colors.WHITE, Colors.BLACK)
        text_rect = text.get_rect()
        text_rect.center = (settings.width * 0.7, settings.height * 0.98)
        text_rect.width, text_rect.height = 750, 20
        self.screen.blit(text, text_rect)

    def redraw(self):
        if not settings.dirty_rects:
            self.screen.blit(self.background, (0, 0))
        wall_rects, old_wall_rects = self.world.draw(self.screen, self.background)
        dirty_rects = self.all_sprites.draw(self.screen)

        if settings.visuals:
            for vs in self.visual_sensors:
                vs.draw(self.screen, self.world.draw_path, self.world.goal_loc, self.world.collision_lines)
        if settings.stats:
            self.draw_stats()
        if settings.dirty_rects:
            pygame.display.update(dirty_rects + wall_rects + old_wall_rects)
        else:
            pygame.display.flip()

    def input(self, in_):
        if in_ in self.input_map:
            return self.input_map[in_]
        return False

    def check_inputs(self):
        if self.input_debounce > 0:
            self.input_debounce -= 1
        if self.input('mouse_down') and self.input(pygame.K_1):
            self.last_grid = self.world.create_wall(self.last_grid)
        if self.input('mouse_down'):
            self.player.shoot(self.world.colliders, self.world.grid.walls)
        if self.input('mouse_down') and self.input(pygame.K_2):
            x, y = pygame.mouse.get_pos()
            self.world.set_goal(x, y)
        if self.input(pygame.K_F1) and not self.input_debounce:
            settings.toggle('stats')
            self.input_debounce = 10
        if self.input(pygame.K_F2) and not self.input_debounce:
            settings.toggle('visuals')
            self.input_debounce = 10
        if self.input(pygame.K_F3) and not self.input_debounce:
            settings.toggle('ai_mode')
            if settings.ai_mode:
                settings.pathfinding = True
            self.world.toggle_ai()
            self.input_debounce = 10
        if self.input(pygame.K_F4) and not self.input_debounce:
            if not settings.ai_mode:
                settings.toggle('pathfinding')
                self.world.toggle_pathfinding()
            self.input_debounce = 10

    def check_event_queue(self):
        ins = self.input_map
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                else:
                    ins[event.key] = True
            elif event.type == pygame.KEYUP:
                ins[event.key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ins['mouse_down'] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                ins['mouse_down'] = False
                self.last_grid = GridLoc(-1, -1)

        self.check_inputs()

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
        while self.__running:
            milliseconds = self.clock.tick(settings.FPS)
            self.playtime += milliseconds / 1000.0

            caption = 'James and Ashvin\'s Game \'AI\'  FPS: {}'.format(round(self.clock.get_fps(), 1))
            if settings.ai_mode:
                caption += ' | AI Mode'
            pygame.display.set_caption(caption)

            self.check_event_queue()
            if not settings.ai_mode:
                self.handle_keys(pygame.key.get_pressed())

            self.all_sprites.update()
            if settings.visuals:
                for vs in self.visual_sensors:
                    vs.update()
            self.world.update()
            self.redraw()

    def cleanup(self):
        self.background = self.screen = self.all_sprites = None
        Workers._pool.terminate()
        Workers._pool.join()
        pygame.quit()

    def run(self):
        self.setup()
        self.mainloop()
        self.cleanup()
