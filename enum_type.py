from enum import IntEnum

# Author: Hao Luo

class STATE(IntEnum):
    """Enum class that represents node state"""
    INIT = 0
    REQUEST = 1
    HELD = 2
    RELEASE = 3

