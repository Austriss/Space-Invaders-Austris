import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType
from models.Enum.EnumObjectDirection import EnumObjectDirection


class ControllerPlayer(GameObject):
    @staticmethod
    def set_direction(player: GameObject, direction: EnumObjectDirection):
        direction: EnumObjectDirection = EnumObjectDirection.NotSet
        player.game_object_direction = direction

    @staticmethod   
    def update(player: GameObject, game_objects: List[GameObject], delta_milisec: float):

     if player.game_object_type == EnumObjectType.Player:

      new_position = list(player.position) 

      key = pygame.key.get_pressed()

      if key[pygame.K_RIGHT]:
            new_position = (player.position[0] + player.movement_speed * delta_milisec, player.position[1])
      elif key[pygame.K_LEFT]:
            new_position = (player.position[0] - player.movement_speed * delta_milisec, player.position[1])

         
      player.position = tuple(new_position)
