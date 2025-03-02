from models.Game import Game
from loguru import logger
from models.Enum.EnumObjectType import EnumObjectType
from models.GameObject import GameObject
from models.Enum.EnumObjectDirection import EnumObjectDirection
from controllers.ControllerAlien import ControllerAlien
from models.Observer.Observer import Subject
from views.factories.GameObjectFactory import GameObjectFactory
import random

ALIEN_ROW_LENGHT = 10
ALIEN_ROW_COUNT = 3
UFO_INTERVAL_MIN = 15
UFO_INTERVAL_MAX = 30

class ControllerGame(Subject):
    __instance = None

    def __init__(self):
        if ControllerGame.__instance is not None:
            logger.error("ControllerGame singleton")
        Subject.__init__(self)
        self._game: Game = None
        self.ufo_timer = 0
        self.ufo_timer_interval = random.randint(UFO_INTERVAL_MIN, UFO_INTERVAL_MAX) * 1000
        self.ufo = None
        self.game_object_factory = GameObjectFactory()
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

    def get_ufo_timer(self):
        return self.ufo_timer
    
    def reset_ufo_timer(self):
        self.ufo_timer = 0
    
    def reset_ufo_timer_interval(self):
        self.ufo_timer_interval = random.randint(UFO_INTERVAL_MIN, UFO_INTERVAL_MAX) * 1000

    def set_game_over(self):
        self.game.is_game_over = True

    def new_game(self):
        game_instance = Game.instance()
        self._game = game_instance


        self._game.game_objects = []
        player = self.game_object_factory.create_game_object(EnumObjectType.Player)
        self._game.game_objects.append(player)


        map_width, map_height = self._game.map_size


        offset_x = (map_width - ALIEN_ROW_LENGHT) // 2
        offset_y = ((map_height - ALIEN_ROW_COUNT) // 2) -3


        for x in range(ALIEN_ROW_LENGHT):
            for y in range(ALIEN_ROW_COUNT):
                if y == 0:
                    obj_type = EnumObjectType.YellowAlien
                elif y == 1:
                    obj_type = EnumObjectType.GreenAlien
                elif y == 2:
                    obj_type = EnumObjectType.BlueAlien
                alien_game_object = self.game_object_factory.create_game_object(obj_type, position=(x+ offset_x, y+ offset_y))
                self._game.game_objects.append(alien_game_object)
        return self._game

    def update(self, delta_milisec: float):
        aliens = [obj for obj in self.game.game_objects if obj.game_object_type in
                  (EnumObjectType.GreenAlien, EnumObjectType.YellowAlien, EnumObjectType.BlueAlien)]
        map_width = self.game.map_size[0]

        border_check = any(alien.position[0] <= 0 or alien.position[0] >= map_width - 1 for alien in aliens)

        #alien direction change if at border
        if border_check and not self.direction_change:
            self.game.alien_move_down = True
            self.direction_change = True
            self.notify("alien_direction_change") 

        elif not border_check:
            self.direction_change = False
        #alien move down after direction change
        if self.game.alien_move_down:
            for alien in aliens:
                alien.position = (alien.position[0], alien.position[1] + 1)
            self.game.alien_move_down = False

        #update ufo spawn
        if self.ufo is None:
            self.ufo_timer += delta_milisec
            if self.get_ufo_timer() >= self.ufo_timer_interval:
                self.spawn_ufo()
        elif self.ufo:
            if self.ufo.position[0] > self.game.map_size[0] or self.ufo.position[0] < -1:
                if self.ufo in self.game.game_objects:
                    self.game.game_objects.remove(self.ufo)
                self.ufo = None
                self.reset_ufo_timer_interval()
                self.reset_ufo_timer()
        
        #GameOver check
        if self.game.player_lives < 1:
            self.set_game_over()
        elif not aliens:
            self.set_game_over()
        if self.game.is_game_over:
            return

    def spawn_ufo(self):
        if self.ufo is None:
            self.ufo = self.game_object_factory.create_game_object(position=(0,1),
                                                                   object_type=EnumObjectType.RedAlien,
                                                                   direction = EnumObjectDirection.Right)
            self.game.game_objects.append(self.ufo)
            self.reset_ufo_timer()

