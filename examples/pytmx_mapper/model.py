'''
PyTMX Mapper
Copyright (c) 2026 Uditya Patel
Licensed under the MIT License.
See LICENSE file in the project root for full license text.
'''
import pygame
from pytmx_mapper.animation import Animation
from dataclasses import dataclass
from typing import Tuple,Dict,Any,List
    
@dataclass
class Collider:
    name: str
    rect: pygame.Rect
    layer: str
    properties: Dict[Any,Any]

@dataclass(slots=True)
class DrawItem:
    image: pygame.Surface | None
    pos: tuple[int, int]
    animation: Animation | None

@dataclass
class MapRect:
    name:str
    type:str
    x:float
    y:float
    w:float
    h:float
    rotation:float

@dataclass
class MapFlag:
    rotate:float
    flip_x:float
    flip_y:float
    flip_diag:float

@dataclass
class MapObject:
    gid:int
    raw_gid:int
    name:str
    type:str
    pos:Tuple[int,int]
    size:Tuple[int,int]
    prop:Dict[Any,Any]
    transform:MapFlag
    rects:List[MapRect]
    

