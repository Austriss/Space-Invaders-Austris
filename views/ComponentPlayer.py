import pygame
from models.GameObject import GameObject
from typing import List
from models.Enum.EnumObjectType import EnumObjectType


class ComponentPlayer:
    def __init__(self, game_object: GameObject):
        self.game_object = game_object
        self.pygame_surfaces: List[pygame.Surface] = []

        self.player_image = "assets/images/player.png"

        
        if self.game_object.game_object_type == EnumObjectType.Player:
                self.load_surface(self.player_image)

    def load_surface(self, image_path: str):
        surface = pygame.image.load(image_path)
        self.pygame_surfaces.append(surface)

    def render(self, screen: pygame.Surface, cell_size: int):
        if self.pygame_surfaces:
            screen_x = self.game_object.position[0] * cell_size
            screen_y = self.game_object.position[1] * cell_size
            screen.blit(self.pygame_surfaces[0], (screen_x, screen_y))