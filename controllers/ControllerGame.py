from models.Game import Game
from loguru import logger
from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumObjectDirection import EnumObjectDirection
from models.Enum.EnumAlienEventType import EnumAlienEventType
from utils.commands.AlienCommand import AlienCommand
from utils.Observer.Observer import Subject
from utils.Observer.Event import Event
from views.factories.GameObjectFactory import GameObjectFactory
import random

ALIEN_ROW_LENGHT = 10
ALIEN_ROW_COUNT = 3
UFO_INTERVAL_MIN = 15
UFO_INTERVAL_MAX = 30
ALIEN_INTERVAL_MIN = 10
ALIEN_INTERVAL_MAX = 20
ALIEN_STOP_TIME = 5

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
        self.alien_timer_interval = random.randint(ALIEN_INTERVAL_MIN, ALIEN_INTERVAL_MAX) * 1000
        self.alien_stop_timer = 0
        self.alien_resume_timer = 0
        self.alien_stop = False
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

    def reset_ufo_timer_interval(self):
        self.ufo_timer_interval = random.randint(UFO_INTERVAL_MIN, UFO_INTERVAL_MAX) * 1000

    def reset_alien_timer_interval(self):
        self.alien_timer_interval = random.randint(ALIEN_INTERVAL_MIN, ALIEN_INTERVAL_MAX) * 1000

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

            #check one aliens direction
            if aliens[0].direction == EnumObjectDirection.Right:
                new_direction = EnumObjectDirection.Left
            else:
                new_direction = EnumObjectDirection.Right

            command = AlienCommand(EnumAlienEventType.CHANGE_DIRECTION, new_direction)
            self.notify(Event(EnumAlienEventType.CHANGE_DIRECTION, command)) 

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
            if self.ufo_timer >= self.ufo_timer_interval:
                self.spawn_ufo()
        elif self.ufo:
            if self.ufo.position[0] > self.game.map_size[0] or self.ufo.position[0] < -1:
                if self.ufo in self.game.game_objects:
                    self.game.game_objects.remove(self.ufo)
                self.ufo = None
                self.reset_ufo_timer_interval()
                self.ufo_timer = 0
        
        #aliens randomly stop for 5sec
            #get one alien direction
        last_direction = aliens[0].direction
        if not self.alien_stop:
            self.alien_stop_timer += delta_milisec
            if self.alien_stop_timer >= self.alien_timer_interval:
                self.alien_stop = True
                command = AlienCommand(EnumAlienEventType.STOP, last_direction)
                self.notify(Event(EnumAlienEventType.STOP, command))
                self.reset_alien_timer_interval()
                self.alien_stop_timer = 0
        elif self.alien_stop:
            self.alien_resume_timer += delta_milisec
            if self.alien_resume_timer >= ALIEN_STOP_TIME * 1000:
                self.alien_stop = False
                command = AlienCommand(EnumAlienEventType.RESUME, last_direction)
                self.notify(Event(EnumAlienEventType.RESUME, command))
                self.reset_alien_timer_interval()
                self.alien_resume_timer = 0

        
        #GameOver check
        if self.game.player_lives < 1:
            self.game.is_game_over = True
        elif not aliens:
            self.game.is_game_over = True
        if self.game.is_game_over:
            return

    def spawn_ufo(self):
        if self.ufo is None:
            self.ufo = self.game_object_factory.create_game_object(position=(0,1),
                                                                   object_type=EnumObjectType.RedAlien,
                                                                   direction = EnumObjectDirection.Right)
            self.game.game_objects.append(self.ufo)
            self.ufo_timer = 0

