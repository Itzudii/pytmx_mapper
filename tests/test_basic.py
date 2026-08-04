"""
Basic tests for PyTMX Mapper.

Run:
    pytest tests/
"""
    
from pathlib import Path

import pygame
import pytest
from pytmx_mapper.map import TileMap
from pytmx_mapper.layers import Layer


pygame.init()

pygame.display.set_mode((1, 1))
ASSET_DIR = Path(__file__).parent.parent / "assets"
TMX_FILE = ASSET_DIR / "map.tmx"


LAYERS = {
    "normal_tile": Layer.NORMAL,
    "collision_normal_tile": Layer.COLLIDE,
    "decoration_object_layer": Layer.DECORATION,
    "object_layer": Layer.OBJECT,
}


@pytest.fixture(scope="module")
def tilemap():
    m = TileMap(TMX_FILE, LAYERS, tilesize=32)
    m.load()
    return m


def test_map_load(tilemap):
    """Map loads successfully."""
    assert tilemap.data is not None


def test_window_size(tilemap):
    """Window size is computed correctly."""
    assert tilemap.window_width > 0
    assert tilemap.window_height > 0


def test_tile_layers_loaded(tilemap):
    """Normal and decoration layers are loaded."""
    assert "normal_tile" in tilemap.layers
    assert "decoration_object_layer" in tilemap.layers


def test_collision_layer_loaded(tilemap):
    """Collision rectangles are loaded."""
    assert "collision_normal_tile" in tilemap.colliders
    assert len(tilemap.colliders["collision_normal_tile"]) > 0


def test_object_layer_loaded(tilemap):
    """Object layer is parsed."""
    assert "objects" in tilemap.objs


def test_draw_order(tilemap):
    """Visible layer order matches draw order."""
    expected = [
        layer.name
        for layer in tilemap.data.visible_layers
        if layer.name in tilemap.layers
    ]

    assert tilemap.draw_order == expected


def test_surface_cache(tilemap):
    """Tile images are cached."""
    gid = next(iter(tilemap.data.images.keys()))
    img1 = tilemap.get_surface_by_gid(gid)
    img2 = tilemap.get_surface_by_gid(gid)

    assert img1 is img2


def test_draw_layers(tilemap):
    """Rendering should not raise exceptions."""
    screen = pygame.Surface(
        (tilemap.window_width, tilemap.window_height),
        pygame.SRCALPHA,
    )

    tilemap.draw_layers(screen)


def test_draw_colliders(tilemap):
    """Collider rendering should not raise exceptions."""
    screen = pygame.Surface(
        (tilemap.window_width, tilemap.window_height),
        pygame.SRCALPHA,
    )

    tilemap.draw_colliders(
        screen,
        "collision_normal_tile",
        (255, 0, 0),
    )