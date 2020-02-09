from typing import List

from model import GameModel


class GameController(object):
    def __init__(self, model: GameModel):
        self.model = model

    def make_play(self, space: List[int]) -> int:
        played = self.model.check_space(space)
        if played:
            return 0
        return self.model.get_current_player()

