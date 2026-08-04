import pygame
from utils.dependency import get_frames

class Effect(pygame.sprite.Sprite):
    def __init__(self,frames,centerx,centery,direction):
        super().__init__()
        self.frames = frames[direction]
        self.len = len(self.frames)
        self.w = self.frames[0].get_width()
        self.h = self.frames[0].get_height()

        self.centerx = centerx
        self.centery = centery
        # animation
        self.animation_speed = .2
        self.idx = 0
        self.idx_f = 0
        self.isfinished = False

    def animation_loop(self):
            self.idx_f += self.animation_speed
            self.idx = int(self.idx_f)
            print(self.idx)
    
            if self.idx >= self.len:
                self.idx = 0
                self.idx_f = 0
                self.isfinished = True
            else:
                self.isfinished = False

    def draw(self,screen):
        centerx = self.centerx - self.w//2
        centery = self.centery - self.h//2
        screen.blit(self.frames[self.idx],(centerx,centery))

    def update(self):
        self.animation_loop()

        if self.isfinished:
            self.kill()
        # else:
            


class Appear(Effect):
    # scale_value = (TILESIZE*3,TILESIZE*3)
    def __init__(self,centerx,centery,direction):
            frames = get_frames(r'assets\Main Characters\Appearing (96x96).png',7)
            super().__init__(frames,centerx,centery,direction)

class Disappear(Effect):
    # scale_value = (TILESIZE*3,TILESIZE*3)
    def __init__(self,centerx,centery,direction):
            frames = get_frames(r'assets\Main Characters\Desappearing (96x96).png',7)
            super().__init__(frames,centerx,centery,direction)

