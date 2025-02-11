from models.Game import Game
from models.Enum.EnumObjectType import EnumObjectType
import random
from models.GameObject import GameObject


class ControllerGame():
    @staticmethod 
    def new_game():


        game = Game()
        game.game_objects = []
        player = GameObject()
        player.position = (7, 13)
        player.game_object_type = EnumObjectType.Player
        game.game_objects.append(player)


        aliens = (
            [EnumObjectType.GreenAlien],
            [EnumObjectType.RedAlien]
            )
        
        row_lenght = 10
        row_count = 3
        map_width, map_height = game.map_size

        offset_x = (map_width - row_lenght) // 2
        offset_y = (map_height - row_count) // 2
        
        for x in range(row_lenght):
            for y in range(row_count):
                if y == 0:
                    obj_type = EnumObjectType.RedAlien
                else:
                    obj_type = EnumObjectType.GreenAlien
                obj_game = GameObject()
                obj_game.position = (x+ offset_x, y+ offset_y)
                obj_game.game_object_type = obj_type
                game.game_objects.append(obj_game)

        return game