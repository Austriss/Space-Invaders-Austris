from dataclasses import dataclass
from dataclasses import field
from models.GameObject import GameObject
from typing import List
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Game:
    __instance = None

    game_objects: List[GameObject] = field(default=list)
    map_size: tuple[int, int] = (15, 15)
    score: int = 0
    player_lives: int = 3
    cell_size: int = 32
    direction_change: bool = False
    alien_move_down: bool = False
    is_game_over: bool = False
    
    def __init__(self):
        if Game.__instance is not None:
            raise Exception("Game is singleton")
        Game.__instance = self

    @staticmethod
    def instance():
        if Game.__instance is None:
            Game()
        return Game.__instance
    
    @property
    def get_map_size(self):
        return self.map_size
    
    @property
    def get_map_width(self):
        return self.map_size[0]
    
    @property
    def get_map_height(self):
        return self.map_size[1]
    
    @property
    def get_cell_size(self):
        return self.cell_size
    
    @property
    def get_score(self):
        return self.score
