import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumObjectDirection import EnumObjectDirection
from views.factories.GameObjectFactory import GameObjectFactory
from models.Game import Game
import time


class ControllerPlayer():
    can_shoot = True

    def __init__(self):
       self.game_object_factory = GameObjectFactory()

    @staticmethod
    def set_direction(player: GameObject, direction: EnumObjectDirection):
        direction: EnumObjectDirection = EnumObjectDirection.NotSet
        player.direction = direction

    @staticmethod   
    def update(player: GameObject, game_objects: List[GameObject], delta_milisec: float, game: Game):
     if player.game_object_type == EnumObjectType.Player:
      map_size = Game.map_size
      new_position = list(player.position)

      keys = pygame.key.get_pressed()

      if keys[pygame.K_RIGHT]:
            new_position[0] += player.movement_speed * delta_milisec
      if keys[pygame.K_LEFT]:
            new_position[0] -= player.movement_speed * delta_milisec


      # Keep player in map bounds
      if new_position[0] >= map_size[0]:
            new_position[0] = map_size[0] - 1
      elif new_position[0] < 0:
            new_position[0] = 0

      player.position = tuple(new_position)

    def fire(self, player: GameObject, game_objects: List[GameObject], game: Game):
      bullet = self.game_object_factory.create_game_object(object_type = EnumObjectType.Bullet,
                                                           position = [player.position[0], player.position[1] - 1],
                                                           direction = EnumObjectDirection.Up)
      bullet.movement_speed = 0.008
      game.game_objects.append(bullet)
