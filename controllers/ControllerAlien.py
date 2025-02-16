import pygame
from models.Enum.EnumObjectDirection import EnumObjectDirection
from models.GameObject import GameObject
from models.Game import Game

class ControllerAlien:

    def __init__(self, alien: GameObject):
        self.alien = alien
        self.step_size = 0.5
        self.move_timer = 0
        self.move_interval = 1000
    def update(self, game: Game, delta_milisec: float):
        self.move_timer += delta_milisec

        if self.move_timer >= self.move_interval and not game.move_down:
            self.move_timer = 0
            self.move()

    def move(self):
        if self.alien.direction == EnumObjectDirection.Right:
            self.alien.position = (self.alien.position[0] + self.step_size, self.alien.position[1])
        elif self.alien.direction == EnumObjectDirection.Left:
            self.alien.position = (self.alien.position[0] - self.step_size, self.alien.position[1])