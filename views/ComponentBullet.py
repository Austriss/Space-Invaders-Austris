import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType


class ComponentBullet:
    def __init__(self, game_object: GameObject):
        self.game_object = game_object
        self.pygame_surfaces: List[pygame.Surface] = []

        self.bullet_image = "assets/images/bullet.png"

        if self.game_object.game_object_type == EnumObjectType.Bullet or self.game_object.game_object_type == EnumObjectType.AlienBullet:
                self.load_surface(self.bullet_image)

    def load_surface(self, image_path: str):
        surface = pygame.image.load(image_path)
        self.pygame_surfaces.append(surface)
        
    
    def render(self, screen: pygame.Surface, cell_size: int):
        if self.pygame_surfaces:
            screen_x = self.game_object.position[0] * cell_size
            screen_y = self.game_object.position[1] * cell_size
            screen.blit(self.pygame_surfaces[0], (screen_x, screen_y))

