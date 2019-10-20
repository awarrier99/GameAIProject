import pygame


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400

    def init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def loop(self):
        pass

    def render(self):
        pass

    def cleanup(self):
        pygame.quit()

    def execute(self):
        self.init()

        while self._running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.loop()
            self.render()
        self.cleanup()


if __name__ == "__main__":
    app = App()
    app.execute()
