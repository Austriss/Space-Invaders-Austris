from models.Enum.EnumObjectType import EnumObjectType

class GameObject:
    position: tuple[int, int] = (0, 0)
    game_object_type: EnumObjectType = EnumObjectType
