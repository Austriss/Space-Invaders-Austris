from models.Game import Game
from models.Enum.EnumObjectType import EnumObjectType
from models.GameObject import GameObject
from models.Enum.EnumObjectDirection import EnumObjectDirection
from controllers.ControllerAlien import ControllerAlien
from models.Observer.Observer import Subject
import random


UFO_INTERVAL_MIN = 15
UFO_INTERVAL_MAX = 30
class ControllerGame(Subject):
    __instance = None

    def __init__(self):
        if ControllerGame.__instance is not None:
            raise Exception("ControllerGame singleton")
        Subject.__init__(self)
        self._game: Game = None
        self.player_controller = None 
        self.game_objects_controllers = []
        self.move_down = False
        self.direction_change = False
        self.ufo_timer = 0
        self.ufo_timer_interval = random.randint(UFO_INTERVAL_MIN, UFO_INTERVAL_MAX) * 1000
        self.has_ufo = False
        self.ufo = None
        ControllerGame.__instance = self  

    @staticmethod
    def instance():
        if ControllerGame.__instance is None:
            ControllerGame()
        return ControllerGame.__instance

    @property
    def game(self):
        return self._game
    
    def set_game(self, game):
        self._game = game

    def new_game(self):
        game_instance = Game.instance()
        self._game = game_instance


        self._game.game_objects = []
        player = GameObject()
        player.position = (7, 13)
        player.game_object_type = EnumObjectType.Player
        self._game.game_objects.append(player)

        ROW_LENGHT = 10
        ROW_COUNT = 3
        map_width, map_height = self._game.map_size


        offset_x = (map_width - ROW_LENGHT) // 2
        offset_y = ((map_height - ROW_COUNT) // 2) -3



        for x in range(ROW_LENGHT):
            for y in range(ROW_COUNT):
                if y == 0:
                    obj_type = EnumObjectType.YellowAlien
                elif y == 1:
                    obj_type = EnumObjectType.GreenAlien
                elif y == 2:
                    obj_type = EnumObjectType.BlueAlien
                obj_game = GameObject()
                obj_game.position = (x + offset_x, y + offset_y)
                obj_game.direction = EnumObjectDirection.Right
                obj_game.game_object_type = obj_type
                self._game.game_objects.append(obj_game)

        return self._game



    def update(self, delta_milisec: float):
        aliens = [obj for obj in self.game.game_objects if obj.game_object_type in
                  (EnumObjectType.GreenAlien, EnumObjectType.YellowAlien, EnumObjectType.BlueAlien)]
        map_width = self.game.map_size[0]

        border_check = any(alien.position[0] <= 0 or alien.position[0] >= map_width - 1 for alien in aliens)

        #alien direction change if at border
        if border_check and not self.direction_change:
            self.game.move_down = True
            self.direction_change = True
            self.notify("alien_direction_change") 

        elif not border_check:
            self.direction_change = False
        #alien move down after direction change
        if self.game.move_down:
            for alien in aliens:
                alien.position = (alien.position[0], alien.position[1] + 1)
            self.game.move_down = False

        #update ufo spawn
        if self.ufo is None:
            self.ufo_timer += delta_milisec
            if self.ufo_timer >= self.ufo_timer_interval:
                self.spawn_ufo()
        elif self.ufo:
            if self.ufo.position[0] > self.game.map_size[0] or self.ufo.position[0] < -1:
                if self.ufo in self.game.game_objects:
                    self.game.game_objects.remove(self.ufo)
                self.ufo = None
                self.ufo_timer_interval = random.randint(UFO_INTERVAL_MIN, UFO_INTERVAL_MAX) * 1000
                self.ufo_timer = 0

    def spawn_ufo(self):
        if self.ufo is None:
            self.ufo = GameObject()
            self.ufo.position = (0, 1)
            self.ufo.game_object_type = EnumObjectType.RedAlien
            self.ufo.direction = EnumObjectDirection.Right
            self.ufo.movement_speed = 1e-3
            self.game.game_objects.append(self.ufo)
            self.ufo_timer = 0

