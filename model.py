"""Implements the data model for a tic-tac-toe game."""

from typing import List


class GameModel(object):
    def __init__(self, grid_size: int = 3):
        self.grid_size = grid_size
        self.board = [[0 for i in range(grid_size)]
                      for j in range(grid_size)]

        self.current_player = 1

    def check_space(self, space: List[int]) -> bool:
        """Checks if a space has been played."""
        return bool(self.board[space[0]][space[1]])

    def get_current_player(self) -> int:
        return self.current_player

