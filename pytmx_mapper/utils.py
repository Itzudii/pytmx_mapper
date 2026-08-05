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


