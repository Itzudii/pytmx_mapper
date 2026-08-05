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
    size:tuple[int, int]
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
    flip_x:bool
    flip_y:bool
    flip_diag:bool

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
    

