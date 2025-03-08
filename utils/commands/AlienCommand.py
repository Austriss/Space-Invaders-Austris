from models.Enum.EnumAlienEventType import EnumAlienEventType
from models.Enum.EnumObjectDirection import EnumObjectDirection

class AlienCommand:
    def __init__(self, command_type: EnumAlienEventType, direction: EnumObjectDirection.NotSet):
        self.command_type = command_type
        self.direction = direction