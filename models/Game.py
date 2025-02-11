from dataclasses import dataclass
from dataclasses import field
from models.GameObject import GameObject
from typing import List
#from dataclasses_json import dataclass_json

#@dataclass_json
@dataclass
class Game:
    game_objects: List[GameObject] = field(default=list)
    map_size: tuple[int, int] = (15, 15)
    score: int = 0
    cell_size: int = 32