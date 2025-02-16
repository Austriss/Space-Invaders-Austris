import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType
from models.Game import Game

class ControllerBullet(GameObject):

    @staticmethod
    def update(bullet: GameObject, game_objects: List[GameObject], delta_milisec: float):
        
        if bullet.game_object_type == EnumObjectType.Bullet:
            map_size = Game.map_size

            new_position = list(bullet.position) 

            new_position[1] -= bullet.movement_speed * delta_milisec

            #in game bounds
            if new_position[1] >= map_size[1]:
                game_objects.remove(bullet)
            elif new_position[1] < 0:
                game_objects.remove(bullet)
            else:
                bullet.position = tuple(new_position)
