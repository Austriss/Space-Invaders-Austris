from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumObjectDirection import EnumObjectDirection
from dataclasses import dataclass

@dataclass
class GameObject:
    position: tuple[int, int] = (0, 0)
    game_object_type: EnumObjectType = EnumObjectType
    direction: EnumObjectDirection = EnumObjectDirection.NotSet
    movement_speed: float = 0.003

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position
