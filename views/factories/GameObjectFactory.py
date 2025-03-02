from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumObjectDirection import EnumObjectDirection
from models.GameObject import GameObject



class GameObjectFactory:
    def create_game_object(self, object_type: EnumObjectType, position: tuple[int, int] = (0, 0), direction: EnumObjectDirection = EnumObjectDirection.NotSet) -> GameObject:
        game_object = GameObject()
        game_object.game_object_type = object_type
        game_object.position = position
        game_object.direction = direction

        if object_type == EnumObjectType.Player:
            if position == (0, 0): #check if default before changing
                game_object.position = (7, 13)
        elif object_type in (EnumObjectType.YellowAlien, EnumObjectType.GreenAlien, EnumObjectType.BlueAlien, EnumObjectType.RedAlien):
            if direction == EnumObjectDirection.NotSet: #check if default before changing
                game_object.direction = EnumObjectDirection.Right
        elif object_type == EnumObjectType.Bullet:
            game_object.direction = EnumObjectDirection.Up
        elif object_type == EnumObjectType.AlienBullet:
            game_object.direction = EnumObjectDirection.Down

        return game_object