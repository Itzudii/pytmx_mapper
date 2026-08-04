import pygame
import pytmx

from pathlib import Path
from collections import defaultdict

from pytmx_mapper.utils import transform_img
from pytmx_mapper.animation import Animation
from pytmx_mapper.camera import Camera
from pytmx_mapper.model import Collider, DrawItem, MapFlag, MapRect, MapObject
from pytmx_mapper.layers import Layer
from typing import List,Dict,Tuple,Any



class TileMap():
    def __init__(self,filename:str,layers_struct:Dict[str,Any],tilesize:int):
        self.filename = filename
        self.layers_structure = layers_struct

        self.data = pytmx.TiledMap(filename)
        self.tilesize = tilesize
        self.scale_factor = self.tilesize/self.data.tilewidth
        self.window_width = self.data.width*self.tilesize
        self.window_height = self.data.height*self.tilesize

        self._cache_images:Dict[Any,pygame.Surface] = dict()
        self._cache_surface:Dict[Any,pygame.Surface] = dict()

        self.layers:Dict[str,List[DrawItem]] = dict()
        self.draw_order:List[str] = []

        self.colliders:Dict[str,List[Collider]] = dict()
        self.objs:Dict[str,defaultdict[str,List[MapObject]]] = dict()

        self.camera = Camera(self.window_width,self.window_height)

    def get_surface_by_gid_helper(self,gid:int,gid_:int|None=None):
        src,rect,flag = self.data.get_tile_image_by_gid(gid)
        if gid_ is not None:
            _,_,flag = self.data.get_tile_image_by_gid(gid_)
        src = Path(src).resolve()

        img = self._cache_images.get(src,None)
        if not img:
            img = pygame.image.load(src).convert_alpha()
            self._cache_images[src] = img

        if (tuple(flag),gid) not in self._cache_surface:
            raw = img.subsurface(pygame.Rect(*rect))
            modfy_img = transform_img(flag,raw)
            self._cache_surface[(tuple(flag),gid)] = pygame.transform.scale_by(modfy_img,self.scale_factor)

        subsurface = self._cache_surface.get((tuple(flag),gid))
        return subsurface

    def get_surface_by_gid(self,gid:int):
        return self.get_surface_by_gid_helper(gid)

    def get_transfrom_frames_by_gid(self,gid:int,frames:Any)->List[pygame.Surface]:
        f:List[pygame.Surface] = []
        for frame in frames:
            img = self.get_surface_by_gid_helper(frame.gid,gid)
            f.append(img)
        return f

    def get_surface_by_obj_helper(self,obj:pytmx.pytmx.TiledObject, gid_:int|None = None):
        gid = obj.gid if gid_ is None else gid_
        rect:Tuple[float,float] = (obj.width,obj.height)
        src,_,_ = self.data.get_tile_image_by_gid(gid)
        flag = (obj.flip_x,obj.flip_y,obj.flip_diag)
        
        source = Path(src).resolve()

        img = self._cache_images.get(source,None)
        if not img:
            img = pygame.image.load(source).convert_alpha()
            self._cache_images[source] = img
      
        if (gid,rect,flag) not in self._cache_surface:
            raw = pygame.transform.scale(img,(rect[0],rect[1]))
            modfy_img = transform_img(flag,raw)
            self._cache_surface[(gid,rect,flag)] = pygame.transform.scale_by(modfy_img,self.scale_factor)
        subsurface = self._cache_surface.get((gid,rect,flag))
        return subsurface
    
    def get_surface_by_obj(self,obj:pytmx.pytmx.TiledObject):
        return self.get_surface_by_obj_helper(obj)

    def get_transfrom_frames_by_obj(self,obj:pytmx.pytmx.TiledObject,frames:Any)->List[pygame.Surface]:
        f:List[pygame.Surface] = []
        for frame in frames:
            img = self.get_surface_by_obj_helper(obj,frame.gid)
            f.append(img)
        return f

            
    def load_collision_rect_of_normal_tiles(self,layername:str):
        layer:Any = self.data.get_layer_by_name(layername)
        collision_tiles:List[Collider] =[]
        for obj in layer:
            rect = pygame.Rect(obj.x*self.scale_factor,obj.y*self.scale_factor,obj.width*self.scale_factor,obj.height*self.scale_factor)
            collision_tiles.append(Collider(obj.name,rect,layername,obj.properties))
        return collision_tiles

    def load_normal_tiles(self,layername:str):
        
        normal_tiles = []
        layer:Any = self.data.get_layer_by_name(layername)

        for x,y,gid in layer.iter_data():
            if gid != 0:
                prop = self.data.get_tile_properties_by_gid(gid)
                if prop and 'frames' in prop:
                    # animated
                    frames = prop['frames']
                    f = self.get_transfrom_frames_by_gid(gid,frames)
                    ani = Animation(f,100)
                    normal_tiles.append(DrawItem(None,(x*self.tilesize,y*self.tilesize),ani))
                else:
                    # static
                    img = self.get_surface_by_gid(gid)
                    normal_tiles.append(DrawItem(img,(x*self.tilesize,y*self.tilesize),None))
        return normal_tiles

    def load_decorations_objs(self,layername:str):
        decorations=[]
        layer = self.data.get_layer_by_name(layername)
        for obj in layer:
            prop = obj.properties
            frames = prop.get('frames')
            if frames:
                # animated
                frame = self.get_transfrom_frames_by_obj(obj,frames) 
                ani = Animation(frame,100)
                decorations.append(DrawItem(None,(obj.x*self.scale_factor,obj.y*self.scale_factor),ani))
            else:
                # static
                img = self.get_surface_by_obj(obj)
                decorations.append(DrawItem(img,(obj.x*self.scale_factor,obj.y*self.scale_factor),None))
        return decorations

    def load_objs(self,layername:str):
        objs = defaultdict(list)
        layer:Any = self.data.get_layer_by_name(layername)
        for  obj in layer:
            transform = MapFlag(
                rotate=obj.rotation,
                flip_x=obj.flip_x,
                flip_y=obj.flip_y,
                flip_diag=obj.flip_diag
            )
            prop = obj.properties
            rects = []
            for collide in prop.get('colliders',()):
                r = MapRect(
                    name = collide.name,
                    type = collide.type,
                    x = collide.x,
                    y = collide.y,
                    w = collide.width,
                    h = collide.height,
                    rotation = collide.rotation
                )
                rects.append(r)
        
            objs[obj.name].append(MapObject(
                gid=obj.gid,
                raw_gid=obj.raw_gid,
                name=obj.name,
                type=obj.type,
                pos=(obj.x*self.scale_factor,obj.y*self.scale_factor),
                size=(obj.width*self.scale_factor,obj.height*self.scale_factor),
                prop=obj.properties,
                transform=transform,
                rects=rects
            ))
        return objs

    
    def load(self):
        for layername,type in self.layers_structure.items():
            match (type):
                case Layer.NORMAL:self.layers[layername] = self.load_normal_tiles(layername)
                case Layer.DECORATION:self.layers[layername] = self.load_decorations_objs(layername)
                case Layer.COLLIDE:self.colliders[layername] = self.load_collision_rect_of_normal_tiles(layername)
                case Layer.OBJECT:self.objs[layername] = self.load_objs(layername)

        for layer in self.data.visible_layers:
            if layer.name in self.layers:
                self.draw_order.append(layer.name)

    def draw(self,layername:str,screen:pygame.Surface)->None:
        for item in self.layers[layername]:
            if item.animation:
                item.animation.update()
                screen.blit(item.animation.image,self.camera.apply_pos(item.pos))
            else:
                screen.blit(item.image,self.camera.apply_pos(item.pos))

    def draw_colliders(self,screen:pygame.Surface,layername:str,color:Tuple[int,int,int]):
        for collider in self.colliders[layername]:
            pygame.draw.rect(screen, color, self.camera.apply_rect(collider.rect), 1)

    def draw_layers(self,screen:pygame.Surface):
        for layername in self.draw_order:
            self.draw(layername,screen)



