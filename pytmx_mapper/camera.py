import pygame
from typing import Tuple,Any
class Camera:
    def __init__(self, screen_width:int, screen_height:int):
        self.offset = pygame.Vector2()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def focus(self, target:Any):
        # Center camera on player
        self.offset.x = target.rect.centerx - self.screen_width // 2
        self.offset.y = target.rect.centery - self.screen_height // 2

    def apply_rect(self, rect:pygame.Rect):
        return rect.move(-self.offset.x, -self.offset.y)

    def apply_pos(self, pos:Tuple[int,int]):
        return (
            pos[0] - self.offset.x,
            pos[1] - self.offset.y
        )

    def can_draw(self,pos,size):
        x= pos[0] - self.offset.x
        y= pos[1] - self.offset.y
        if -size[0] < x <self.screen_width and -size[1] < y <self.screen_height:
            return (x,y)
        return None