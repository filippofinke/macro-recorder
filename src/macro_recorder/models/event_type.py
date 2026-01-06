from enum import Enum


class EventType(str, Enum):
    MOVE = "move"
    CLICK = "click"
    SCROLL = "scroll"
