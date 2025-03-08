from models.Enum.EnumObjectDirection import EnumObjectDirection
from models.GameObject import GameObject
from models.Game import Game
from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumAlienEventType import EnumAlienEventType
from utils.Observer.Observer import Observer
from utils.commands.AlienCommand import AlienCommand
from views.factories.GameObjectFactory import GameObjectFactory
import random
from typing import List

ALIEN_STEP_SIZE = 0.5
ALIEN_MOVE_INTERVAL = 1000
ALIEN_RANDOM_SHOOT_CHANCE = 0.01


class ControllerAlien(Observer):

    def __init__(self, alien: GameObject):
        Observer.__init__(self)
        self.game_object_factory = GameObjectFactory()
        self._alien = alien
        self.step_size = ALIEN_STEP_SIZE
        self.move_time = 0
        self.move_interval = ALIEN_MOVE_INTERVAL
        self.shoot_timer = 0
        self.shoot_interval = random.randint(2000, 5000)
        self.can_shoot = False
        self.last_direction = EnumObjectDirection.Right
    
    
    def on_event(self, event):
        if isinstance(event.data, AlienCommand):
            self.process_event_command(event.data)
    
    def process_event_command(self, command: AlienCommand):
        if command.command_type == EnumAlienEventType.CHANGE_DIRECTION:
            self._alien.direction = command.direction
            self.last_direction = command.direction
        elif command.command_type == EnumAlienEventType.STOP:
            if command.direction != EnumObjectDirection.NotSet:
                self.last_direction = command.direction
            self._alien.direction = EnumObjectDirection.NotSet
        elif command.command_type == EnumAlienEventType.RESUME:
            self._alien.direction = self.last_direction



    def update_movement(self, game: Game, delta_milisec: float):
        self.move_time += delta_milisec
        if (
            self.move_time >= self.move_interval 
            and not game.alien_move_down
            and self._alien.direction != EnumObjectDirection.NotSet
            ):
            self.move_time = 0
            self.move()


    def update_shooting(self, game: Game, delta_milisec: float):
        self.shoot_timer += delta_milisec
        #random alien shooting
        if self.shoot_timer >= self.shoot_interval and not self.can_shoot:
            self.can_shoot = True

        if self.can_shoot:
            if random.random() < ALIEN_RANDOM_SHOOT_CHANCE:
                self.shoot(game.game_objects)
                self.shoot_timer = 0
                self.shoot_interval = random.randint(2000, 5000)
                self.can_shoot = False
            else:
                self.can_shoot = False
                self.shoot_timer = 0
                self.shoot_interval = random.randint(2000, 5000)

    def game_update(self, game: Game, delta_milisec: float):
        self.update_movement(game, delta_milisec)
        self.update_shooting(game, delta_milisec)

    def move(self):
        #if not direction notset
        x, y = self._alien.get_position()
        if self._alien.direction == EnumObjectDirection.Right:
            self._alien.set_position(x + self.step_size, y)
        elif self._alien.direction == EnumObjectDirection.Left:
            self._alien.set_position(x - self.step_size, y)

    def update_ufo(self, ufo: GameObject, game: Game, delta_milisec: float):
        if ufo.direction == EnumObjectDirection.Right:
            ufo.position = (ufo.position[0] + ufo.movement_speed * delta_milisec, ufo.position[1])
        else:
            ufo.position = (ufo.position[0] - ufo.movement_speed * delta_milisec, ufo.position[1])

    # random alien shooting
    def shoot(self, game_objects: List[GameObject]):
        x, y = self._alien.get_position()
        bullet = self.game_object_factory.create_game_object(object_type=EnumObjectType.AlienBullet,
                                                              direction = EnumObjectDirection.Down,
                                                              position=(x, y + 1))
        game_objects.append(bullet)