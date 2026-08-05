import pygame
from typing import Dict,Tuple,Any

def transform_img(flag:Tuple[int,int,int],image:pygame.Surface)->pygame.Surface:
    TRANSFORMS:Dict[Any,Any] = {
        (0, 0, 0): lambda s: s,
        (1, 0, 0): lambda s: pygame.transform.flip(s, True, False),
        (0, 1, 0): lambda s: pygame.transform.flip(s, False, True),
        (1, 1, 0): lambda s: pygame.transform.flip(s, True, True),

        (0, 0, 1): lambda s: pygame.transform.flip(pygame.transform.rotate(s, 90), True, False),
        (1, 0, 1): lambda s: pygame.transform.rotate(s, 90),
        (0, 1, 1): lambda s: pygame.transform.rotate(s, -90),
        (1, 1, 1): lambda s: pygame.transform.flip(pygame.transform.rotate(s, 90), False, True),
    }
    return TRANSFORMS[flag](image)

def get_frames(url,col):
    img = pygame.image.load(url)
    w = img.get_width()
    h = img.get_height()
    tilesize= w//col

    frames_orignal = [img.subsurface(pygame.Rect(tilesize*i,0,tilesize,h)) for i in range(col)]
    return frames_orignal

def get_transform_images(url,col,size,flag):
    imgs = get_frames(url,col)
    scale_img = [pygame.transform.scale(img,size) for img in imgs]
    return [transform_img((int(flag.flip_x),int(flag.flip_y),int(flag.flip_diag)),img) for img in scale_img]
