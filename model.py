"""Implements the data model for a tic-tac-toe game."""

from typing import List

import model_error as GameModelError


class GameModel(object):
    def __init__(self, grid_size: int = 3):
        self.grid_size = grid_size
        self.board = [[0 for i in range(grid_size)]
                      for j in range(grid_size)]

        self.turn_order = [1, 2]
        self.number_of_players = len(self.turn_order)
        self.active_player = self.turn_order[0]

    def advance_player_order(self) -> int:
        """Advance the active player to the next player in turn order.

        Returns: The new active player.
        """
        active_player_turn_order = self.turn_order.index(self.active_player)
        try:
            next_player = self.turn_order[active_player_turn_order + 1]
        except IndexError:
            next_player = self.turn_order[0]
        self.active_player = next_player
        return self.active_player

    def change_active_player(self, player: int) -> int:
        """Changes the active player.

        Returns: The new active player.

        Raises:
            InvalidPlayer: If the requested player is not found.
        """
        if player not in self.turn_order:
            raise GameModelError.InvalidPlayer("Player not found.")
        self.active_player = player
        return self.active_player

    def get_active_player(self) -> int:
        """Returns the currently active player."""
        return self.active_player

    def is_space_empty(self, space: List[int]) -> bool:
        """Checks if a space is empty (playable).

        Raises:
            InvalidSpace: If the requested space is outside the grid.
        """
        try:
            return not bool(self.board[space[0]][space[1]])
        except IndexError:
            raise GameModelError.InvalidSpace(
                "This space does not exist on the game board."
            )

    def make_play(self, space: List[int]) -> bool:
        """Marks a space on the board as occupied by the active player."""
        try:
            self.board[space[0]][space[1]] = self.active_player
        except IndexError:
            raise GameModelError.InvalidSpace(
                "This space does not exist on the game board."
            )

