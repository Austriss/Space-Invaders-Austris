from models.Enum.EnumAlienEventType import EnumAlienEventType

class Event:
    def __init__(self, event_type: EnumAlienEventType, data=None):
        self.event_type = event_type
        self.data = data