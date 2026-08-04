import pygame

from settings import TILESIZE,BASESIZE

from pytmx_mapper.map import TileMap
from pytmx_mapper.layers import Layer
from player.model import Player


class Level():
    tilesize=TILESIZE
    def __init__(self):
        layers = {
            "normal_tile":Layer.NORMAL,
            "collision_normal_tile":Layer.COLLIDE, 
            "decoration_object_layer":Layer.DECORATION, 
            "decoration_object_layer_foreground":Layer.DECORATION,
        }
        self.map = TileMap('mapdata/map.tmx',layers,TILESIZE)
        self.checkpoints = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.boxs = pygame.sprite.Group()
        self.camera = self.map.camera


    def load(self):
        self.map.load()
        self.landblocks = [collider.rect for collider in self.map.colliders['collision_normal_tile']]
        self.player = Player((100,100))
    


    def event_handle(self,event):
        self.player.event_handle(event)
        pass

    def key_handle(self,key):
        self.player.key_handle(key)
        pass

    def draw(self,screen):
        self.map.draw_layers(screen)
        self.map.draw_colliders(screen,'collision_normal_tile',(255,0,0))

        for flag in self.checkpoints:
            flag.draw(screen)

        for box in self.boxs:
            box.draw(screen)

        for fruit in self.fruits:
            fruit.draw(screen)

        self.player.draw(screen,self.camera)

    def collisions(self):
        
        for flag in self.checkpoints:
            if flag.rect.colliderect(self.player.rect) and self.player.move:
                flag.hit()
                # save coord

        for fruit in self.fruits:
            if fruit.rect.colliderect(self.player.rect):
                fruit.hit()
                #  increase points

        for box in self.boxs:
            if box.rect.colliderect(self.player.rect):
                box.get_break()
                #  increase points


    def update(self):
        pass
        # self.collisions()
        # self.checkpoints.update()
        # self.fruits.update()
        # self.boxs.update()
        self.player.update(level=self)
        self.camera.focus(self.player)




















