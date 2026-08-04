import pygame
class Partical(pygame.sprite.Sprite):
    def __init__(self,lifespan):
        super().__init__()
        self.life = lifespan
        self.max_life = lifespan

    def update(self):
        self.life -= 1
        alpha = int(255 * (self.life / self.max_life))
        self.img.set_alpha(alpha)
        if self.life == 0:
            self.kill()

    def __type__(self):
        return Partical