import pygame
import sys
from level import Level

class App():
    def __init__(self):
        pygame.init()
        self.level = Level()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.level.map.window_width,self.level.map.window_height))
        self.isRunning = True
        self.dt = 0
        self.level.load()

    def event_handling(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                    break
                self.level.event_handle(event)

    def key_handling(self):
        key = pygame.key.get_pressed()
        self.level.key_handle(key)

    
    def run(self):
        while self.isRunning:
            self.screen.fill((0,0,0))

            self.event_handling()
            
            self.key_handling()

            self.level.update()

            self.level.draw(self.screen)

            pygame.display.flip()

            self.dt = self.clock.tick(60)//1000

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()