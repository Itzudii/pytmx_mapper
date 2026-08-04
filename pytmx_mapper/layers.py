'''
PyTMX Mapper
Copyright (c) 2026 Uditya Patel
Licensed under the MIT License.
See LICENSE file in the project root for full license text.
'''
from enum import Enum
class Layer(Enum):
    NORMAL = "n"
    OBJECT = "o"
    DECORATION = "d"
    COLLIDE = "c"
