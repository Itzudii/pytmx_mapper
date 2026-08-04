from typing import List
from pygame import Surface

class Animation:
    def __init__(self,frames:List[Surface],duration:float=53.3):
        self.frames = frames
        self.animation_speed = 16/duration
        self.idx = 0
        self.idx_f = 0
        self.isfinished = False

    def update(self):
        self.idx_f += self.animation_speed
        self.idx = int(self.idx_f)

        if self.idx >= len(self.frames):
            self.idx = 0
            self.idx_f = 0
            self.isfinished = True
        else:
            self.isfinished = False

    @property
    def index(self):
        return self.idx
    
    @property
    def image(self):
        return self.frames[self.idx]

    @property
    def finished(self):
        return self.isfinished