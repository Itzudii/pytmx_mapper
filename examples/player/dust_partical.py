import random 
from utils.dependency import get_img
from utils.partical import Partical
from settings import TILESIZE
class Dust(Partical):
    img = get_img(r"assets\Other\Dust Particle.png",(TILESIZE//3,TILESIZE//3))
    def __init__(self, lifespan):
        super().__init__(lifespan)
        self.img = self.__class__.img.convert_alpha()
        self.w = self.img.get_width()

    def draw(self,screen,camera):
        screen.blit(self.img,camera.apply_pos((self.x-self.w//2,self.y-self.w//2)))

class DustH(Dust):
    def __init__(self,x,y,lifespan,h):
        super().__init__(lifespan)
        self.x = x
        self.y = y
        self.df = lifespan/h

    def update(self):
        super().update()
        if self.life >= self.max_life/2:
            self.y -= self.df
        else:
            self.y += self.df

class DustJ(Dust):
    def __init__(self,x,y,lifespan,h):
        super().__init__(lifespan)
        self.x = x
        self.y = y

    def update(self):
        super().update()
        self.y -= 1
    
        

class DustF(Dust):
    def __init__(self,x,y,lifespan,h):
        super().__init__(lifespan)
        self.x = x
        self.y = y
        self.df = lifespan/h
        self.speed = random.choice((2,-2))

    def update(self):
        super().update()
        if self.life >= self.max_life/2:
            self.y -= self.df
        else:
            self.y += self.df

        self.x += self.speed
            
class DustV(Dust):
    def __init__(self,x,y,lifespan):
        super().__init__(lifespan)
        self.x = x
        self.y = y
        self.vel_y = 0
        self.gravity = .3

        self.direction = random.choice((1,-1))
        self.vel_x = self.x
        self.speed = random.random()

    def update(self):
        super().update()
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.direction == -1:
            self.vel_x += self.speed
            self.x = round(self.vel_x)
        elif self.direction == 1:
            self.vel_x -= self.speed
            self.x = round(self.vel_x)
