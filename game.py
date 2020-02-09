#!/usr/bin/env python3

"""Tic-tac-toe game using turtle and MVC design pattern.

Usage:
    python3 game.py
"""

import sys

from controller import GameController
from model import GameModel
from view import GameView


def main() -> None:
    model = GameModel()
    controller = GameController(model)
    view = GameView(controller, board_size = 300, grid_size = 3)

if __name__ == '__main__':
    main()

