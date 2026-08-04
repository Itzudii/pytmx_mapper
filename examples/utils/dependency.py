import pygame
from settings import TILESIZE,BASESIZE
def get_frames(url,col,both = True,offset_l=0,offset_r=0,offset_t=0,scale_factor=None):
    img = pygame.image.load(url)
    w = img.get_width()
    h = img.get_height()
    tilesize= w//col
    ratiox = tilesize/BASESIZE
    ratioy = h/BASESIZE
    if not scale_factor:
        scale_factor = (TILESIZE*ratiox,TILESIZE*ratioy)

    frames_orignal = [img.subsurface(pygame.Rect(tilesize*i+offset_l,offset_t,(tilesize-offset_l)-offset_r,h-offset_t)) for i in range(col)]
    if scale_factor:
        frames_orignal =  transform_imgs(frames_orignal,scale_factor)
    if both:
        frames_filp = [pygame.transform.flip(img.subsurface(pygame.Rect(tilesize*i+offset_l,offset_t,(tilesize-offset_l)-offset_r,h-offset_t)),1,0) for i in range(col)]
        if scale_factor:
            frames_filp =  transform_imgs(frames_filp,scale_factor)
        return {1:frames_orignal,-1:frames_filp}
    
    return {1:frames_orignal}

def get_img(url,scale_factor = None):
    img = pygame.image.load(url)
    w = img.get_width()
    h = img.get_height()
    ratiox = w/BASESIZE
    ratioy = h/BASESIZE
    if not scale_factor:
        scale_factor = (TILESIZE*ratiox,TILESIZE*ratioy)

    return pygame.transform.scale(img,scale_factor) 

def transform_imgs(imgs,size:tuple):
    return [pygame.transform.scale(img,size) for img in imgs]


def define_collide_rect(img,center,w,h):
    rect = img.get_rect()
    rect.center = center
    rect.w = w
    rect.h = h