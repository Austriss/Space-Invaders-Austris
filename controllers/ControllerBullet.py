import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType
from models.Game import Game

class ControllerBullet(GameObject):

    @staticmethod
    def update(bullet: GameObject, game_objects: List[GameObject], delta_milisec: float, game: Game):
        
        if bullet.game_object_type == EnumObjectType.Bullet:

            new_position = list(bullet.position) 
            new_position[1] -= bullet.movement_speed * delta_milisec

            #in game bounds
            if new_position[1] < 0:
                if bullet in game_objects:
                    game_objects.remove(bullet)
                    return
            bullet.position = tuple(new_position)
            for object in list(game_objects): 
                if object.game_object_type in (EnumObjectType.RedAlien, EnumObjectType.GreenAlien):
                    if ControllerBullet.Collision(bullet, object):
                        if bullet in game_objects:
                            game_objects.remove(bullet)
                        if object in game_objects:
                            game_objects.remove(object)
                        game.score += 1
                        return

    @staticmethod
    def Collision(bullet: GameObject, alien: GameObject):
        if (bullet.position[0] < alien.position[0] + 1 and
            bullet.position[0] + 1 > alien.position[0] and
            bullet.position[1] < alien.position[1] + 1 and
            bullet.position[1] + 1 > alien.position[1]):
            return True
        return False

    