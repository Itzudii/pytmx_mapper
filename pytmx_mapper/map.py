import pygame
import pytmx

from pathlib import Path
from collections import defaultdict

from pytmx_mapper.utils import transform_img
from pytmx_mapper.animation import Animation
from pytmx_mapper.camera import Camera
from pytmx_mapper.model import Collider, DrawItem, MapFlag, MapRect, MapObject, MapShape
from pytmx_mapper.layers import Layer
from typing import List,Dict,Tuple,Any



class TileMap():
    def __init__(self,filename:str,layers_struct:Dict[str,Any],tilesize:int):
        self.filename = filename
        self.layers_structure = layers_struct

        self.data = pytmx.TiledMap(filename)

        self.width = self.data.width
        self.height = self.data.height

        self.tilesize = tilesize
        self.scale_factor = self.tilesize/self.data.tilewidth

        self.width_px = self.data.width*self.tilesize
        self.height_px = self.data.height*self.tilesize

        self.visible_tiles_x = self.width_px // self.tilesize + 2
        self.visible_tiles_y = self.height_px // self.tilesize + 2

        self._cache_images:Dict[Any,pygame.Surface] = dict()
        self._cache_surface:Dict[Any,pygame.Surface] = dict()
        self.id_to_obj = dict()

        self.layers:Dict[str,List[List[DrawItem]]] = dict()
        self.draw_order:List[str] = []

        self.colliders:Dict[str,List[Collider]] = dict()
        self.objs:Dict[str,defaultdict[str,List[MapObject]]] = dict()
        self.shapes:Dict[str,defaultdict[str,List[MapObject]]] = dict()

        self.camera = Camera(self.width_px,self.height_px)


    def resize_map(self,size:Tuple[int,int]):
        width_px = size[0]
        height_px = size[1]
        self.camera = Camera(width_px,height_px)
        self.visible_tiles_x = width_px // self.tilesize + 2
        self.visible_tiles_y = height_px // self.tilesize + 2

    def _load_cache_image(self, src):
        source = Path(src).resolve()

        img = self._cache_images.get(source)
        if img is None:
            img = pygame.image.load(source).convert_alpha()
            self._cache_images[source] = img

        return img


    

    def _get_surface_by_gid_helper(self,gid:int,gid_:int|None=None):
        src,rect,flag = self.data.get_tile_image_by_gid(gid)
        if gid_ is not None:
            _,_,flag = self.data.get_tile_image_by_gid(gid_)
        # src = Path(src).resolve()

        img = self._load_cache_image(src)
        # img = self._cache_images.get(src)
        # if img is None:
        #     img = pygame.image.load(src).convert_alpha()
        #     self._cache_images[src] = img

        if (gid,tuple(flag)) not in self._cache_surface:
            raw = img.subsurface(pygame.Rect(*rect))
            modfy_img = transform_img(flag,raw)
            self._cache_surface[(gid,tuple(flag))] = pygame.transform.scale_by(modfy_img,self.scale_factor)

        subsurface = self._cache_surface.get((gid,tuple(flag)))
        return subsurface

    def get_surface_by_gid(self,gid:int):
        return self._get_surface_by_gid_helper(gid)

    def get_transfrom_frames_by_gid(self,gid:int,frames:Any)->List[pygame.Surface]:
        f:List[pygame.Surface] = []
        for frame in frames:
            img = self._get_surface_by_gid_helper(frame.gid,gid)
            f.append(img)
        return f

    def _get_surface_by_obj_helper(self,obj:pytmx.pytmx.TiledObject, gid_:int|None = None):
        flag = (obj.flip_x,obj.flip_y,obj.flip_diag)
        rect:Tuple[float,float] = (obj.width,obj.height)

        gid = obj.gid if gid_ is None else gid_
        src,_,_ = self.data.get_tile_image_by_gid(gid)
        
        # source = Path(src).resolve()

        # img = self._cache_images.get(source,None)
        # if not img:
        #     img = pygame.image.load(source).convert_alpha()
        #     self._cache_images[source] = img
        img = self._load_cache_image(src)
      
        if (gid,rect,flag) not in self._cache_surface:
            raw = pygame.transform.scale(img,(rect[0],rect[1]))
            modfy_img = transform_img(flag,raw)
            self._cache_surface[(gid,rect,flag)] = pygame.transform.scale_by(modfy_img,self.scale_factor)
        subsurface = self._cache_surface.get((gid,rect,flag))
        return subsurface
    
    def get_surface_by_obj(self,obj:pytmx.pytmx.TiledObject):
        return self._get_surface_by_obj_helper(obj)

    def get_transfrom_frames_by_obj(self,obj:pytmx.pytmx.TiledObject,frames:Any)->List[pygame.Surface]:
        f:List[pygame.Surface] = []
        for frame in frames:
            img = self._get_surface_by_obj_helper(obj,frame.gid)
            f.append(img)
        return f

            
    def load_collision_rect_of_normal_tiles(self,layername:str):
        layer:Any = self.data.get_layer_by_name(layername)
        collision_tiles:List[Collider] =[]
        for obj in layer:
            rect = pygame.Rect(obj.x*self.scale_factor,obj.y*self.scale_factor,obj.width*self.scale_factor,obj.height*self.scale_factor)
            collision_tiles.append(Collider(obj.name,rect,layername,obj.properties))
        return collision_tiles
    
    def _create_draw_item(self, image, animation, x, y, w, h):
        return DrawItem(
            image,
            (x*self.scale_factor, y*self.scale_factor),
            (w*self.scale_factor, h*self.scale_factor),
            animation
        )

    def load_normal_tiles(self,layername:str):
        
        layer:Any = self.data.get_layer_by_name(layername)
        normal_tiles = [[None for _ in range(layer.width)] for _ in range(layer.height)]

        for x,y,gid in layer.iter_data():
            if gid != 0:
                prop = self.data.get_tile_properties_by_gid(gid)
                if prop and 'frames' in prop:
                    # animated
                    frames = prop['frames']
                    f = self.get_transfrom_frames_by_gid(gid,frames)
                    ani = Animation(f,frames[0].duration)
                    normal_tiles[y][x] = DrawItem(None,(x*self.tilesize,y*self.tilesize),(self.tilesize,self.tilesize),ani)
                else:
                    # static
                    img = self.get_surface_by_gid(gid)
                    normal_tiles[y][x] = DrawItem(img,(x*self.tilesize,y*self.tilesize), (self.tilesize,self.tilesize),None)
        return normal_tiles

    def load_decorations_objs(self,layername:str):
        layer = self.data.get_layer_by_name(layername)
        decorations=[[None for _ in range(self.data.width)] for _ in range(self.data.height)]
        for obj in layer:
            prop = obj.properties
            frames = prop.get('frames')
            if frames:
                # animated
                frame = self.get_transfrom_frames_by_obj(obj,frames) 
                ani = Animation(frame,frames[0].duration)
                decorations[obj.y//self.tilesize][obj.x//self.tilesize] = self._create_draw_item(None,ani,obj.x,obj.y,obj.width,obj.height)
                # decorations.append(self._create_draw_item(None,ani,obj.x,obj.y,obj.width,obj.height))
            else:
                # static
                img = self.get_surface_by_obj(obj)
                decorations.append(self._create_draw_item(img,None,obj.x,obj.y,obj.width,obj.height))
                decorations.append(self._create_draw_item(img,None,obj.x,obj.y,obj.width,obj.height))
        return decorations

    def load_objs(self,layername:str):
        objs = defaultdict(list)
        layer:Any = self.data.get_layer_by_name(layername)
        for  obj in layer:
            transform = MapFlag(
                rotate=obj.rotation,
                flip_x=obj.flip_x if hasattr(obj,"flip_x") else False,
                flip_y=obj.flip_y if hasattr(obj,"flip_y") else False,
                flip_diag=obj.flip_diag if hasattr(obj,"flip_diag") else False
            )
            prop = obj.properties
            rects = []
            for collide in prop.get('colliders',()):
                r = MapRect(
                    name = collide.name,
                    type = collide.type,
                    x = (obj.x+collide.x)*self.scale_factor,
                    y = (obj.y+collide.y)*self.scale_factor,
                    w = collide.width*self.scale_factor,
                    h = collide.height*self.scale_factor,
                    rotation = collide.rotation,
                    dif_x = collide.x*self.scale_factor,
                    dif_y = collide.y*self.scale_factor,
                )
                rects.append(r)
            if len(rects) == 0:
                r = MapRect(
                    name = '',
                    type = '',
                    x = (obj.x)*self.scale_factor,
                    y = (obj.y)*self.scale_factor,
                    w = obj.width*self.scale_factor,
                    h = obj.height*self.scale_factor,
                    rotation = 0,
                    dif_x = 0,
                    dif_y = 0,
                )
                rects.append(r)

            # print(obj.id)
            o = MapObject(
                id = obj.id,
                gid=obj.gid,
                raw_gid=obj.raw_gid if hasattr(obj,"raw_gid") else None,
                name=obj.name,
                type=obj.type,
                pos=(obj.x*self.scale_factor,obj.y*self.scale_factor),
                size=(obj.width*self.scale_factor,obj.height*self.scale_factor),
                prop=obj.properties,
                transform=transform,
                rects=rects
            )
            self.id_to_obj[obj.id] = o
            objs[obj.name].append(o)

        print('Object loaded successfully')
        return objs

    def load_polygons(self,layername):
        objs = defaultdict(list)
        layer:Any = self.data.get_layer_by_name(layername)
        for  obj in layer:

            o=MapShape(
                id = obj.id,
                points=[(point.x*self.scale_factor,point.y*self.scale_factor) for point in obj.points] if hasattr(obj,"points") else [],
                name=obj.name,
                type=obj.type,
                pos=(obj.x*self.scale_factor,obj.y*self.scale_factor),
                size=(obj.width*self.scale_factor,obj.height*self.scale_factor),
                prop=obj.properties,
                rotate = obj.rotation

            )
            self.id_to_obj[obj.id] = o
            objs[obj.name].append(o)
        return objs

    def get_obj_by_id(self,id):
        return self.id_to_obj.get(id)
    
    def load(self):
        for layername,type in self.layers_structure.items():
            match (type):
                case Layer.NORMAL:self.layers[layername] = self.load_normal_tiles(layername)
                case Layer.DECORATION:self.layers[layername] = self.load_decorations_objs(layername)
                case Layer.COLLIDE:self.colliders[layername] = self.load_collision_rect_of_normal_tiles(layername)
                case Layer.OBJECT:self.objs[layername] = self.load_objs(layername)
                case Layer.SHAPE:self.shapes[layername] = self.load_polygons(layername)

        for layer in self.data.visible_layers:
            if layer.name in self.layers:
                self.draw_order.append(layer.name)


    def _draw_layer(self, layername: str, screen: pygame.Surface):
        layer = self.layers[layername]
    
        ox = self.camera.offset.x
        oy = self.camera.offset.y
        draw = screen.blit
    
        start_x = max(0, int(ox // self.tilesize))
        end_x = min(start_x + self.visible_tiles_x, self.data.width)
    
        start_y = max(0, int(oy // self.tilesize))
        end_y = min(start_y + self.visible_tiles_y, self.data.height)
    
        for y in range(start_y, end_y):
            row = layer[y]
            for x in range(start_x, end_x):
                item = row[x]
                if item is not None:
                    pos = (item.pos[0] - ox, item.pos[1] - oy)
    
                    if item.animation:
                        item.animation.update()
                        draw(item.animation.image, pos)
                    else:
                        draw(item.image, pos)

    def draw_layers(self,screen:pygame.Surface):
        for layername in self.draw_order:
            self._draw_layer(layername,screen)

    def draw_colliders(self,screen:pygame.Surface,layername:str,color:Tuple[int,int,int]):
        for collider in self.colliders[layername]:
            pygame.draw.rect(screen, color, self.camera.apply_rect(collider.rect), 1)



