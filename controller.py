from typing import List

from model import GameModel


class GameController(object):
    def __init__(self, model: GameModel):
        self.model = model

    def make_play(self, space: List[int]) -> int:
        if not self.model.is_space_empty(space):
            return 0
        current_player = self.model.get_active_player()
        self.model.make_play(space)
        self.model.advance_player_order()
        return current_player

