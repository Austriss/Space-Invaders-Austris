from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumObjectDirection import EnumObjectDirection
from dataclasses import dataclass

@dataclass
class GameObject:
    position: tuple[int, int] = (0, 0)
    game_object_type: EnumObjectType = EnumObjectType
    direction: EnumObjectDirection = EnumObjectDirection.NotSet
    movement_speed: float = 0.003

