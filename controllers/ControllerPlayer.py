import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumObjectDirection import EnumObjectDirection
from models.Game import Game


class ControllerPlayer():
    @staticmethod
    def set_direction(player: GameObject, direction: EnumObjectDirection):
        direction: EnumObjectDirection = EnumObjectDirection.NotSet
        player.direction = direction

    @staticmethod   
    def update(player: GameObject, game_objects: List[GameObject], delta_milisec: float, game: Game):

     if player.game_object_type == EnumObjectType.Player:
      map_size = Game.map_size

      new_position = list(player.position) 

      key = pygame.key.get_pressed()

      if key[pygame.K_RIGHT]:
            new_position[0] += player.movement_speed * delta_milisec
      elif key[pygame.K_LEFT]:
            new_position[0] -= player.movement_speed * delta_milisec
      elif key[pygame.K_SPACE]:
            ControllerPlayer.fire(player, game_objects, game)


      #in game bounds
      if new_position[0] >= map_size[0]:
            new_position[0] = map_size[0] - 1
      elif new_position[0] < 0:
            new_position[0] = 0

      player.position = tuple(new_position)

    @staticmethod
    def fire(player: GameObject, game_objects: List[GameObject], game: Game):
      bullet = GameObject()
      bullet.position = [player.position[0], player.position[1] - 1]
      bullet.game_object_type = EnumObjectType.Bullet
      bullet.movement_speed = 0.008
      game.game_objects.append(bullet)
