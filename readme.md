<div align="center">

# PyTMX Mapper

A high-performance map renderer and utility library built on top of PyTMX for pygame.  
Load TMX maps, render static and animated tiles, manage decorations, collisions, and map objects with automatic scaling.


</div>

About
===============================================================================
**For Python 3.9+**
PyTMX Mapper is a high-performance TMX map renderer and utility library built on top of PyTMX for pygame. It is designed to simplify loading, rendering, and managing maps created with the Tiled Map Editor while giving developers complete control over game logic.

The library automatically loads only the assets used by a map, caches images and transformed surfaces for fast rendering, and supports both static and animated tiles and decorations. It also scales the entire map—including tiles, object positions, collision rectangles, and decorations—to any tile size with a single configuration value.

PyTMX Mapper provides:

Fast cached rendering of TMX maps.
Automatic support for static and animated tile layers.
Static and animated decoration object layers.
Collision rectangle extraction with custom properties.
Map object loading with metadata, transforms, and custom collider definitions.
Built-in camera support for efficient world rendering.
Layer-order rendering that preserves the order defined in Tiled.
A lightweight API that leaves game logic, entities, AI, and animations entirely under the developer's control.

PyTMX Mapper focuses solely on rendering maps and exposing map data. It does not manage game objects, physics, enemies, or players, allowing it to integrate easily into any pygame project regardless of architecture.
## Features

**pygame-ce is fully supported.**

PyTMX Mapper is built specifically for **pygame** and is designed to make rendering TMX maps fast, simple, and scalable. It extends PyTMX by providing a lightweight rendering system while leaving game logic entirely to the developer.

Current capabilities include:

* Static and animated tile rendering.
* Static and animated decoration object rendering.
* Automatic image caching for high-performance drawing.
* Automatic scaling of maps, tiles, objects, and collision rectangles.
* Collision rectangle extraction with custom properties.
* Map object loading with metadata, transforms, and custom collider definitions.
* Built-in camera support.
* Rendering order that matches the layer order defined in Tiled.

### Design Philosophy

PyTMX Mapper is **not** a game engine.

It does **not** manage players, enemies, NPCs, AI, physics, collisions, animations, or game state. Instead, it focuses on rendering TMX maps efficiently and exposing map data in a clean Python API so developers can integrate it into any project architecture.

Game objects are returned as lightweight data structures containing their position, size, properties, transforms, and custom collider definitions. How these objects are instantiated, updated, and rendered is entirely controlled by the user.

### Current Limitations

* Infinite (chunked) TMX maps are **not currently supported**.
* Maps must use standard finite TMX layers.
* Saving or editing TMX files is **not supported**.
* PyTMX Mapper is a rendering and map-loading library, **not** a map editor.

### Future Goals

The initial release focuses on platformer-style games. Future versions aim to support additional map styles while maintaining the same simple API and high rendering performance.


*Released under the MIT*
## Documentation

This README provides a quick introduction to **PyTMX Mapper**. Complete documentation, API reference, tutorials, and examples are available in the **docs/** directory. Practical examples demonstrating rendering, collision loading, object loading, scaling, and camera usage can be found in the **examples/** folder.

### Table of Contents

1. Installation
2. Quick Start
3. Creating a TileMap
4. Layer Types
5. Rendering Maps
6. Camera
7. Collision Layers
8. Decoration Layers
9. Object Layers
10. Scaling Maps
11. API Reference

---

# Design Goals and Features

* Fast cached rendering for TMX maps.
* Automatic rendering of static and animated tile layers.
* Automatic rendering of static and animated decoration object layers.
* Automatic image loading and caching.
* Automatic scaling of maps, tiles, decorations, objects, and collision rectangles.
* Camera support for world rendering.
* Collision rectangle extraction with custom properties.
* Lightweight map object data with transforms and collider definitions.
* Preserves the layer order defined in Tiled.
* Designed specifically for pygame and pygame-ce.
* Minimal runtime overhead after loading.

---

# Why use PyTMX Mapper?

### PyTMX Mapper is fast

* Loads only the assets referenced by the current map.
* Uses aggressive caching to avoid repeated image loading and transformations.
* Performs almost no per-frame calculations during rendering.
* Optimized for efficient rendering of large TMX maps.

### PyTMX Mapper is simple

* Render an entire TMX map with only a few lines of code.
* Resize the entire world by changing a single tile size value.
* Clean API that separates rendering from gameplay logic.
* Uses familiar pygame objects such as `Surface` and `Rect`.

### PyTMX Mapper is flexible

* Supports both static and animated tiles.
* Supports static and animated decoration objects.
* Returns collision rectangles with custom properties.
* Returns map object metadata so developers can instantiate their own game entities.
* Does not impose a game architecture, ECS, physics engine, or entity system.

### PyTMX Mapper is lightweight

PyTMX Mapper focuses exclusively on loading and rendering TMX maps. It intentionally leaves players, enemies, NPCs, physics, AI, animations, and game logic under the developer's control, making it easy to integrate into existing pygame projects.

### Current Limitations

* Infinite (chunked) TMX maps are not currently supported.
* Saving or editing TMX files is not supported.
* Requires PyTMX for TMX parsing.
* Designed for pygame and pygame-ce.


# Installation

## Install from source

Clone the repository and install it locally:

```bash
git clone https://github.com/YOUR_USERNAME/pytmx-mapper.git
cd pytmx-mapper
pip install .
```

For development:

```bash
pip install -e .
```

## Requirements

* Python **3.9+**
* pygame **2.5+** (or pygame-ce)
* PyTMX (not official) the fork repo in my github.

## Verify the installation

```python
from pytmx_mapper.map import TileMap

print("PyTMX Mapper installed successfully!")
```

# Basic Usage

## Loading a TMX Map

Create a layer mapping that tells **PyTMX Mapper** how each Tiled layer should be handled.

```python
from pytmx_mapper.map import TileMap
from pytmx_mapper.layers import Layer

layers = {
    "normal_tile": Layer.NORMAL,
    "collision_normal_tile": Layer.COLLIDE,
    "decoration_object_layer": Layer.DECORATION,
    "decoration_object_layer_foreground": Layer.DECORATION,
    "core_objects": Layer.OBJECT,
}

tilemap = TileMap(
    "mapdata/map.tmx",
    layers,
    tilesize=32
)

tilemap.load()
```

---

## Rendering the Map

Render every drawable layer in the same order they appear in **Tiled**.

```python
while running:
    tilemap.draw_layers(screen)
```

---

## Layer Types

The `layers` dictionary maps a Tiled layer name to a `Layer` type.

```python
layers = {
    "normal_tile": Layer.NORMAL,
    "collision_normal_tile": Layer.COLLIDE,
    "decoration_object_layer": Layer.DECORATION,
    "decoration_object_layer_foreground": Layer.DECORATION,
    "core_objects": Layer.OBJECT,
}
```

### Available Layer Types

| Layer              | Description                                                                                                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Layer.NORMAL`     | Tile layer containing static or animated tiles.                                                                                                                               |
| `Layer.COLLIDE`    | Object layer containing collision rectangles.                                                                                                                                 |
| `Layer.DECORATION` | Object layer containing decorative images (static or animated).                                                                                                               |
| `Layer.OBJECT`     | Object layer containing gameplay objects such as players, enemies, NPCs, traps, pickups, etc. Objects are returned as data only—the user manages their creation and behavior. |

---

## Drawing Collision Rectangles (Debug)

Collision rectangles are not rendered automatically. They are intended for collision detection and debugging.

```python
tilemap.draw_colliders(
    screen,
    "collision_normal_tile",
    (255, 0, 0)
)
```

---

## Accessing Collision Rectangles

Retrieve the collision rectangles for your own physics or collision system.

```python
land_blocks = [
    collider.rect
    for collider in tilemap.colliders["collision_normal_tile"]
]
```

You can also access each collider's metadata:

```python
for collider in tilemap.colliders["collision_normal_tile"]:
    print(collider.name)
    print(collider.properties)
```

---

## Accessing Map Objects

Object layers are loaded as lightweight data structures.

```python
players = tilemap.objs["core_objects"]["player"]

for obj in players:
    print(obj.name)
    print(obj.type)
    print(obj.pos)
    print(obj.size)
    print(obj.properties)
```

Instantiate your own game objects using the returned data.

```python
player = Player(obj)
enemy = Enemy(obj)
```

PyTMX Mapper intentionally does **not** update or draw gameplay objects.

---

## Camera

A built-in camera is included for scrolling maps.

```python
player = Player()

tilemap.camera.focus(player)
```

The camera is automatically applied when calling:

```python
tilemap.draw_layers(screen)
```

or

```python
tilemap.draw_colliders(screen, "collision_normal_tile", (255, 0, 0))
```

---

## Automatic Scaling

Change the tile size once and the entire map scales automatically.

```python
tilemap = TileMap(
    "mapdata/map.tmx",
    layers,
    tilesize=64
)
```

PyTMX Mapper automatically scales:

* Tile layers
* Decoration layers
* Object positions
* Object sizes
* Collision rectangles
* Animated tiles
* Animated decorations

No additional scaling code is required.



Working with Maps
===============================================================================

TiledMap objects are returned from the loader.  They contain layers, objects,
and a bunch of useful functions for getting information about the map.  In
general, all of the pytmx types are not meant to be modified after being
returned from the loader.  While there is a potential for modifying them,
its not a supported function, and may change any time.  Please consider them
read-only.

Here is a list of attributes for use.  (ie: TiledMap.layers):

- layers: all layers in order
- tile_properties: dictionary of tile properties {GID: {props...}, ...}
- layernames: dictionary of layers with names: {name: layer, ...}
- images: list of all images in use, indexed by GID.  Index 0 is always None.
- version
- orientation
- width: width of map in tiles, not pixels
- height: height of map in tiles, not pixels
- tileheight: height of tile in pixels.  may differ between layers.
- tilewidth: width of tile in pixels.  may differ between layers.
- background_color: map background color specified in Tiled
- properties: all user created properties about the map


#### Optional loading flags

All loaders support the following flags:
- load_all_tiles: if True, all tiles will be loaded, even if unused
- invert_y: used for OpenGL graphics libs.  Screen origin is at lower-left
- allow_duplicate_names: Force load maps with ambiguous data (see 'reserved names')

```python
from pytmx.util_pygame import load_pygame
tiled_map = load_pygame(path_to_tmx_file, invert_y=True)
```

#### Loading from XML

Most pytmx objects support loading from XML strings.  For some objects, they require
references to other objects (like a layer has references to a tileset) and won't load
directly from XML.  They can only be loaded if the entire map is loaded first.  If you
want to store XML in a database or something, you can load the entire map with an XML string:

```python
import pytmx
tiled_map = pytmx.TiledMap.from_xml_string(some_string_here)
```

#### Custom Image Loading

The pytmx.TiledMap object constructor accepts an optional keyword "image_loader".  The argument should be a function that accepts filename, colorkey (false, or a color) and pixelalpha (boolean) arguments.  The function should return another function that will accept a rect-like object and any flags that the image loader might need to know, specific to the graphics library.  Since that concept might be difficult to understand, I'll illustrate with some code.  Use the following template code to load images from another graphics library.

 ```python
import pytmx

def other_library_loader(filename, colorkey, **kwargs):

    # filename is a file to load an image from
    # here you should load the image in whatever lib you want

    def extract_image(rect, flags):
    
        # rect is a (x, y, width, height) area where a particular tile is located
        # flags is a named tuple that indicates how tile is flipped or rotated
    
        # use the rect to specify a region of the image file loaded in the function
        # that encloses this one.
        
        # return an object to represent the tile
        
        # what is returned here will populate TiledMap.images, be returned by
        # TiledObject.Image and included in TiledTileLayer.tiles()

    return extract_image

level_map_and_images = pytmx.TiledMap("leveldata.tmx", image_loader=other_library_loader)
```

#### Accessing layers

Layers are accessed through the TiledMap class and there are a few ways to get references to them:

```python
# get a layer by name
layer_or_group = tiled_map.get_layer_by_name("base layer")

# TiledMap.layers is a list of layers and object groups
layer = tiled_map.layers[layer_index_number]

# easily get references to just the visible tile layers
for layer in tiled_map.visible_tile_layers:
    ...

# just get references to visible object groups
for group in tile_map.visible_object_groups:
    ...
```

# Working with Tile Layers

PyTMX Mapper automatically loads and prepares tile layers for rendering. During loading, all images are cached, transformed (flip/rotation), scaled to the configured tile size, and animations are initialized.

Each drawable layer contains a list of `DrawItem` objects.

## Drawing Tile Layers

The simplest way to render a layer is:

```python
tilemap.draw("normal_tile", screen)
```

Or draw every registered drawable layer in the correct Tiled render order:

```python
tilemap.draw_layers(screen)
```

---

## Static and Animated Tiles

`Layer.NORMAL` supports both static and animated tiles.

Animated tiles are detected automatically from the TMX file and converted into `Animation` objects during loading.

No additional code is required.

```python
layers = {
    "ground": Layer.NORMAL,
}

tilemap = TileMap("map.tmx", layers, 32)
tilemap.load()

while running:
    tilemap.draw_layers(screen)
```

---

## DrawItem Structure

Each drawable layer stores a list of `DrawItem` objects.

```python
@dataclass
class DrawItem:
    image: pygame.Surface | None
    pos: tuple[int, int]
    animation: Animation | None
```

* `image` — Static tile image.
* `pos` — World position.
* `animation` — Animation instance for animated tiles.

Exactly one of `image` or `animation` will be available.

---

## Accessing Layer Data

Drawable layers are available after calling `load()`.

```python
ground = tilemap.layers["ground"]

for item in ground:
    print(item.pos)

    if item.image:
        print("Static tile")

    if item.animation:
        print("Animated tile")
```

---

## Automatic Image Caching

PyTMX Mapper automatically caches:

* Source images
* Tile surfaces
* Rotated tiles
* Flipped tiles
* Scaled tiles

Each unique tile is processed only once during loading, minimizing runtime overhead.

---

## Automatic Tile Scaling

Changing the tile size automatically rescales every tile.

```python
tilemap = TileMap(
    "map.tmx",
    layers,
    tilesize=64
)
```

The following are scaled automatically:

* Tile images
* Tile positions
* Animated frames
* Flipped tiles
* Rotated tiles

No manual scaling is required.

---

## Tile Animations

Animated tiles exported by **Tiled** are detected automatically.

Each frame is loaded, transformed, scaled, and stored inside an `Animation` object.

During rendering, animations are updated automatically.

```python
while running:
    tilemap.draw_layers(screen)
```

No animation update code is required for map tiles.

---

## Performance

Tile rendering is optimized for minimal runtime overhead.

During `load()`:

* Only assets referenced by the current map are loaded.
* Images are cached.
* Transformations (flip and rotation) are applied once.
* Scaling is performed once.
* Animated frames are prepared.

During `draw()`:

* Static tiles are rendered with a single `blit()`.
* Animated tiles update their current frame before rendering.
* The camera offset is applied automatically.

This design keeps per-frame calculations to a minimum, making PyTMX Mapper suitable for large TMX maps.
# Working with Objects

Unlike tile and decoration layers, **object layers are not rendered by PyTMX Mapper**.

Instead, the library converts every object into lightweight Python data structures that your game can use to create players, enemies, NPCs, traps, pickups, checkpoints, or any other gameplay entity.

This keeps PyTMX Mapper focused on map rendering while giving you complete control over game logic.

---

## Object Layers

Object layers are registered using `Layer.OBJECT`.

```python
from pytmx_mapper.layers import Layer

layers = {
    "objects": Layer.OBJECT,
}
```

After loading the map:

```python
tilemap.load()
```

all objects become available through:

```python
tilemap.objs
```

---

## Accessing Objects

Objects are grouped by their **name**.

```python
players = tilemap.objs["objects"]["player"]
enemies = tilemap.objs["objects"]["enemy"]
coins = tilemap.objs["objects"]["coin"]
```

Each key contains a list of `MapObject` instances.

```python
for enemy in tilemap.objs["objects"]["enemy"]:
    print(enemy.pos)
```

---

## MapObject

Every object is converted into a `MapObject`.

```python
@dataclass
class MapObject:
    gid: int
    raw_gid: int

    name: str
    type: str

    pos: tuple[int, int]
    size: tuple[int, int]

    prop: dict

    transform: MapFlag
    rects: list[MapRect]
```

### Attributes

| Attribute   | Description                                        |
| ----------- | -------------------------------------------------- |
| `gid`       | Internal GID after PyTMX processing.               |
| `raw_gid`   | Original TMX GID including flip flags.             |
| `name`      | Object name defined in Tiled.                      |
| `type`      | Object type defined in Tiled.                      |
| `pos`       | Scaled world position `(x, y)`.                    |
| `size`      | Scaled object size `(width, height)`.              |
| `prop`      | Custom properties defined in Tiled.                |
| `transform` | Rotation and flip information.                     |
| `rects`     | Custom collider rectangles attached to the object. |

---

## Object Transform

Transformation information is available through `MapFlag`.

```python
enemy.transform.rotate
enemy.transform.flip_x
enemy.transform.flip_y
enemy.transform.flip_diag
```

```python
@dataclass
class MapFlag:
    rotate: float
    flip_x: bool
    flip_y: bool
    flip_diag: bool
```

---

## Object Colliders

If a tileset object contains **Tile Collision Editor** shapes, they are automatically exported as `MapRect` objects.

```python
for rect in enemy.rects:
    print(rect.name)
    print(rect.type)
```

```python
@dataclass
class MapRect:
    name: str
    type: str

    x: float
    y: float

    w: float
    h: float

    rotation: float
```

This allows developers to create hitboxes, hurtboxes, attack zones, trigger areas, or custom collision shapes directly inside **Tiled**, without hardcoding them in Python.

---

## Custom Properties

Every custom property created in Tiled is available through `prop`.

```python
enemy.prop["health"]
enemy.prop["speed"]
enemy.prop["damage"]
```

Example:

```python
health = enemy.prop.get("health", 100)
speed = enemy.prop.get("speed", 4)
```

---

## Creating Game Objects

PyTMX Mapper does **not** create or manage gameplay entities.

Instead, instantiate your own classes using the returned `MapObject`.

```python
for data in tilemap.objs["objects"]["enemy"]:
    enemy = Enemy(data)
    enemies.add(enemy)
```

Likewise:

```python
for data in tilemap.objs["objects"]["player"]:
    player = Player(data)
```

This design allows each object instance to have its own health, AI, animations, inventory, or behavior without the map library making any assumptions.

---

## Automatic Scaling

All object positions and sizes are automatically scaled using the tile size specified when creating the `TileMap`.

This means changing:

```python
tilemap = TileMap(
    "map.tmx",
    layers,
    tilesize=64
)
```

automatically scales:

* Object positions
* Object sizes
* Collision rectangles
* Tile collision data

No additional scaling code is required.

---

## Design Philosophy

PyTMX Mapper intentionally separates **map rendering** from **game logic**.

The library is responsible for:

* Loading TMX maps
* Rendering tile layers
* Rendering decoration layers
* Loading collision layers
* Loading object metadata

Your game is responsible for:

* Creating entities
* Updating entities
* Rendering entities
* Physics
* AI
* Combat
* Animation states
* Saving game data

This separation keeps the library lightweight, flexible, and suitable for projects of any size.


Understanding Properties
===============================================================================

Properties are a powerful feature of Tiled that allows the level designer to
assign key/value data to individual maps, tilesets, tiles, and objects.  pytmx
includes full support for reading this data so you can set parameters for stuff
in Tiled, instead of maintaining external data files, or even values in source.

Properties are created by the user in tiled.  There is also another set of data
that is part of each object, accessed by normal object attributes.  This other
data is not set directly by the user, but is instead set by tiled.  Typical
data that is object attributes are: 'name', 'x', 'opacity', or 'id'.

If the user sets data for an object in Tiled, it becomes part of 'properties'.
'Properties' is just a normal python dictionary.

```python
# get data normally set by Tiled
obj.name
obj.x
obj.opacity

# get data set by the user in Tiled
obj.properties['hit points']
obj.properties['goes to 11']
```

Individual tile properties are accessed through the the parent map object:

```
tiled_map = TiledMap('level1.tmx')
props = tiled_map.get_tile_properties(x, y, layer)
props = tiled_map.get_tile_properties_by_gid(tile_gid)
```


# Camera & Scrolling Maps

PyTMX Mapper includes a lightweight built-in camera for rendering scrolling maps. The camera automatically offsets every drawable layer, allowing you to create side-scrolling, top-down, or large open-world maps without manually adjusting tile positions.

---

## Focusing the Camera

Center the camera on any object that exposes a `rect` attribute (such as a `pygame.sprite.Sprite`).

```python
player = Player()

tilemap.camera.focus(player)
```

Typically, this is called once per frame after updating the player.

```python
while running:
    player.update()

    tilemap.camera.focus(player)

    tilemap.draw_layers(screen)
```

---

## Automatic Rendering

The camera is applied automatically when rendering the map.

```python
tilemap.draw_layers(screen)
```

No manual offset calculations are required.

The camera is also applied when drawing collision rectangles for debugging.

```python
tilemap.draw_colliders(
    screen,
    "collision_normal_tile",
    (255, 0, 0)
)
```

---

## Camera Utilities

The camera exposes helper methods for converting world coordinates into screen coordinates.

### Position

```python
screen_pos = tilemap.camera.apply_pos(world_pos)
```

### Rectangle

```python
screen_rect = tilemap.camera.apply_rect(world_rect)
```

These methods are useful when drawing your own game objects, UI markers, or debug information so everything stays aligned with the map.

---

## Camera Responsibility

The built-in camera only affects map rendering and coordinate conversion.

It does **not**:

* Move or update game objects.
* Perform culling or visibility checks.
* Manage zoom.
* Control gameplay logic.

Developers remain free to implement custom camera behavior while continuing to use PyTMX Mapper's rendering utilities.

