import pygame
from models.Enum.EnumObjectDirection import EnumObjectDirection
from models.GameObject import GameObject
from models.Game import Game
from models.Enum.EnumObjectType import EnumObjectType
from models.Observer.Observer import Observer
import random
from typing import List

class ControllerAlien(Observer):

    def __init__(self, alien: GameObject):
        Observer.__init__(self)
        self.alien = alien
        self.step_size = 0.5
        self.move_time = 0
        self.move_interval = 1000
        self.shoot_timer = 0
        self.shoot_interval = random.randint(2000, 5000)
        self.can_shoot = False

    def on_event(self, event):
        if event == 'alien_direction_change':
            self.direction_change()

    def direction_change(self):
        if self.alien.direction == EnumObjectDirection.Right:
            self.alien.direction = EnumObjectDirection.Left
        elif self.alien.direction == EnumObjectDirection.Left:
            self.alien.direction = EnumObjectDirection.Right

    def update_movement(self, game: Game, delta_milisec: float):
        self.move_time += delta_milisec
        if self.move_time >= self.move_interval and not game.move_down:
            self.move_time = 0
            self.move()


    def update_shooting(self, game: Game, delta_milisec: float):
        self.shoot_timer += delta_milisec
        #random alien shooting
        if self.shoot_timer >= self.shoot_interval and not self.can_shoot:
            self.can_shoot = True

        if self.can_shoot:
            if random.random() < 0.01:
                self.shoot(game.game_objects)
                self.shoot_timer = 0
                self.shoot_interval = random.randint(2000, 5000)
                self.can_shoot = False
            else:
                self.can_shoot = False
                self.shoot_timer = 0
                self.shoot_interval = random.randint(2000, 5000)
                
    def update(self, subject, event=None, data=None, delta_milisec=None):
        if event == 'alien_direction_change':
            self.direction_change()
        else:
            if isinstance(subject, Game):
                self.update_movement(subject, delta_milisec)
                self.update_shooting(subject, delta_milisec)

    def game_update(self, game: Game, delta_milisec: float):

        self.update_movement(game, delta_milisec)
        self.update_shooting(game, delta_milisec)

    def move(self):
        if self.alien.direction == EnumObjectDirection.Right:
            self.alien.position = (self.alien.position[0] + self.step_size, self.alien.position[1])
        elif self.alien.direction == EnumObjectDirection.Left:
            self.alien.position = (self.alien.position[0] - self.step_size, self.alien.position[1])

    def update_ufo(self, ufo: GameObject, game: Game, delta_milisec: float):
        if ufo.direction == EnumObjectDirection.Right:
            ufo.position = (ufo.position[0] + ufo.movement_speed * delta_milisec, ufo.position[1])
        else:
            ufo.position = (ufo.position[0] - ufo.movement_speed * delta_milisec, ufo.position[1])

    # random alien shooting
    def shoot(self, game_objects: List[GameObject]):
        bullet = GameObject()
        bullet.game_object_type = EnumObjectType.AlienBullet
        bullet.position = (self.alien.position[0], self.alien.position[1] + 1)
        bullet.direction = EnumObjectDirection.Down
        bullet.movement_speed = 1e-3
        game_objects.append(bullet)