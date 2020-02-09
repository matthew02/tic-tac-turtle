"""GameModel exceptions."""


class GameModelError(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidPlayer(GameModelError):
    pass

class InvalidSpace(GameModelError):
    pass

