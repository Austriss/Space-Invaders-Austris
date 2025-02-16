from models.Game import Game
from models.Enum.EnumObjectType import EnumObjectType
from models.GameObject import GameObject
from models.Enum.EnumObjectDirection import EnumObjectDirection


class ControllerGame():
    move_down_dist = 1

    @staticmethod
    def new_game():

        game = Game()
        game.game_objects = []
        player = GameObject()
        player.position = (7, 13)
        player.game_object_type = EnumObjectType.Player
        game.game_objects.append(player)

        row_lenght = 10
        row_count = 3
        map_width, map_height = game.map_size

        offset_x = (map_width - row_lenght) // 2
        offset_y = (map_height - row_count) // 2

        for x in range(row_lenght):
            for y in range(row_count):
                if y == 0:  # first row - red alien
                    obj_type = EnumObjectType.RedAlien
                else:
                    obj_type = EnumObjectType.GreenAlien
                obj_game = GameObject()
                obj_game.position = (x + offset_x, y + offset_y)
                obj_game.direction = EnumObjectDirection.Right
                obj_game.game_object_type = obj_type
                game.game_objects.append(obj_game)

        return game

    def __init__(self, game: Game):
        self.game = game
        self.move_down = False
        self.direction_change = False

    def update(self, delta_milisec: float):
        aliens = [obj for obj in self.game.game_objects if obj.game_object_type in
                  (EnumObjectType.GreenAlien, EnumObjectType.RedAlien)]
        map_width = self.game.map_size[0]

        border_check = any(alien.position[0] <= 0 or alien.position[0] >= map_width - 1 for alien in aliens)

        if border_check and not self.direction_change:
            self.game.move_down = True
            self.direction_change = True 


            for alien in aliens:
                if alien.direction == EnumObjectDirection.Right:
                    alien.direction = EnumObjectDirection.Left
                elif alien.direction == EnumObjectDirection.Left:
                    alien.direction = EnumObjectDirection.Right

        elif not border_check:
            self.direction_change = False

        if self.game.move_down:
            for alien in aliens:
                alien.position = (alien.position[0], alien.position[1] + 1)
            self.game.move_down = False