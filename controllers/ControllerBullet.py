import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType
from models.Game import Game


UFO_KILL_SCORE = 50
ALIEN_KILL_SCORE = 10

class ControllerBullet():

    @staticmethod
    def update(bullet: GameObject, game_objects: List[GameObject], delta_milisec: float, game: Game):
        
        if bullet.game_object_type == EnumObjectType.Bullet or bullet.game_object_type == EnumObjectType.AlienBullet:
            new_position = list(bullet.position)
            if bullet.game_object_type == EnumObjectType.Bullet:
                new_position[1] -= bullet.movement_speed * delta_milisec
            elif bullet.game_object_type == EnumObjectType.AlienBullet:
                new_position[1] += bullet.movement_speed * delta_milisec
            #map bullet bounds
            if new_position[1] < 0 or new_position[1] > game.map_size[1]:
                if bullet in game_objects:
                    game_objects.remove(bullet)
                    return
                
            bullet.position = tuple(new_position)

            for obj in list(game_objects):
                if obj.game_object_type in (EnumObjectType.YellowAlien,
                                                EnumObjectType.GreenAlien,
                                                EnumObjectType.BlueAlien,
                                                EnumObjectType.RedAlien) and bullet.game_object_type == EnumObjectType.Bullet:

                    if ControllerBullet.collision(bullet, obj):
                        if bullet in game_objects:
                            game_objects.remove(bullet)
                        if obj in game_objects:
                            game_objects.remove(obj)
                        if obj.game_object_type == EnumObjectType.RedAlien:
                            game.score += UFO_KILL_SCORE
                        else:
                            game.score += ALIEN_KILL_SCORE
                        return 
                elif obj.game_object_type == EnumObjectType.Player and bullet.game_object_type == EnumObjectType.AlienBullet:
                    if ControllerBullet.collision(bullet, obj):
                        if bullet in game_objects:
                            game_objects.remove(bullet)
                            game.player_lives -= 1
                        return
                        


    @staticmethod
    def collision(bullet: GameObject, target: GameObject):
        if (bullet.position[0] < target.position[0] + 1 and
            bullet.position[0] + 1 > target.position[0] and
            bullet.position[1] < target.position[1] + 1 and
            bullet.position[1] + 1 > target.position[1]):
            return True
        return False

    