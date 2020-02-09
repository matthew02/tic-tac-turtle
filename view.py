"""Implements the view for a tic-tac-toe game using tkinter and Turtle."""

from turtle import Turtle, Screen, Shape
from typing import List, Optional

from controller import GameController


class GameView(object):
    """This class handles the user facing part of the game. This draws the
    game board and components."""

    def __init__(
        self,
        controller: GameController,
        board_size: int,
        grid_size: int = 3
    ) -> None:
        self.controller = controller

        #### Setup the screen.
        # Change it to a square 50% larger than the game board size.
        self.screen = Screen()
        screen_size = int(board_size * 1.5)
        self.resize_screen(screen_size, screen_size)

        #### Setup the game board.
        # Initialize the turtle that will draw the game board.
        self.board = GameView.new_turtle()
        self.lineweight = board_size / 60
        self.board.pensize(self.lineweight)
        self.board.speed(0)
        #self.board.dot(0)

        self.board_size = board_size
        self.grid_size = grid_size
        self.grid_line_spacing = board_size / grid_size


        #### Create our player markers.
        marker_scale = board_size / 100 / grid_size
        marker_lineweight = 8 * marker_scale
        self.create_player_shapes()
        x_marker = GameView.new_turtle('x marker',
                                              marker_scale,
                                              marker_lineweight)
        o_marker = GameView.new_turtle('o marker',
                                              marker_scale,
                                              marker_lineweight)
        self.players = [x_marker, o_marker]

        #### Final initialization
        self.draw_board()
        self.screen.onclick(self.mouse_click)
        self.screen.mainloop()

    def create_player_shapes(self, color: str = 'black') -> None:
        """Creates custom turtle shapes for the x and o player markers.

        This method sets up custom shapes that can be used with the
        turtle.shape() method. Recall that you could make your turtle look
        like an actual turtle (instead of the default arrow shape) by calling
        turtle.shape('turtle'). After this method has been called, you can
        change the sape of your turtle to an x or an o by calling
        turtle.shape('x marker') or turtle.shape('o marker').

        These shapes are initialized at a size appropriate for display on a
        3x3 grid on a 300px game board.
        """

        # Build the x out of a backslash and forward slash.
        # These numbers are the vertices of the slashes.
        backslash = ((-25,-25), (25,25))
        forwardslash = ((-25,25), (25,-25))
        shape = Shape('compound')
        shape.addcomponent(backslash, '', color)
        shape.addcomponent(forwardslash, '', color)
        self.screen.register_shape('x marker', shape)

        # Approximate the o with a 20-sided polygon.
        # These numbers are the vertices of the polygon.
        circle = (( 00.00,-25.00), ( 07.73,-23.78), ( 14.69,-20.23),
                  ( 20.23,-14.69), ( 23.78,-07.73), ( 25.00, 00.00),
                  ( 23.78, 07.73), ( 20.23, 14.69), ( 14.69, 20.23),
                  ( 07.73, 23.78), ( 00.00, 25.00), (-07.73, 23.78),
                  (-14.69, 20.23), (-20.23, 14.69), (-23.78, 07.73),
                  (-25.00, 00.00), (-23.78,-07.73), (-20.23,-14.69),
                  (-14.69,-20.23), (-07.73,-23.78),)
        shape = Shape('compound')
        shape.addcomponent(circle, '', color)
        self.screen.register_shape('o marker', shape)

    def draw_line(self, x: float, y: float, heading: float, length: float) -> None:
        """Draws a line on the game board.

        Args:
            x, y: The coordinates where the line starts.
            heading: The angle of the line.
            length: The length of the line.
        """
        self.board.setheading(heading)

        self.board.penup()
        self.board.goto(x, y)

        self.board.pendown()
        self.board.forward(length)

    def draw_board(self) -> None:
        """Draws the game board centered on the point (0,0)."""
        # Each horizontal line will have a common starting x coordinate.
        # Each vertical line will have a common starting y coordinate.
        # These coordinates are equal to each other.
        anchor = self.board_size / 2

        # The y-coordinates of horizontal lines and the x-coordinates of
        # vertical lines begin equal to each other and increment equally
        increments = list(
            anchor - i * self.grid_line_spacing
            for i in range(1, self.grid_size)
        )

        for i in increments:
            self.draw_line(i, anchor, 270, self.board_size)
            self.draw_line(anchor, i, 180, self.board_size)

    def mark_play(self, player: int, space: List[int]) -> None:
        """Marks a play on the game board.

        Args:
            player: The player to mark, based on play order, starting at 1.
            space: The space to be marked. The bottom-left space is (0,0).
        """
        # Offset the space coordinates so that (0,0) becomes the center space
        space = [s - self.grid_size // 2 for s in space]

        # Calculate the pixel offset between spaces on the game board
        space_offset = self.board_size / self.grid_size

        # Find the screen coordinates of the center of the selected space on
        # the game board.
        center = [space_offset * s for s in space]

        current_player = self.players[player - 1]
        current_player.goto(*center)
        current_player.stamp()

    def mouse_click(self, x: float, y: float) -> None:
        """Handles mouse click actions."""
        # Ignore all clicks outside of the game board area
        extent = self.board_size / 2
        if not (-extent < x < extent and -extent < y < extent):
            return

        # Find the space on the board in which the mose was clicked
        # The bottom-left square is space (0,0).
        space = [round(c / self.grid_line_spacing) + self.grid_size // 2
                 for c in [x, y]]

        # Ask the controller to make a play in this space
        player = self.controller.make_play(space)

        # If the play was successful, the controller will return the player
        # who made the play
        if player:
            # Mark the play on the board
            self.mark_play(player, space)

    def resize_screen(self, width: int, height: int) -> None:
        """Resizes the screen."""
        self.screen.setup(width, height)

    @staticmethod
    def new_turtle(
        shape: Optional[str] = None,
        scale: float = 1.0,
        lineweight: float = 1.0
    ) -> Turtle:
        """Creates a new turtle and hides it.

        Args:
            shape: A valid shapename. See TurtleScreen documentation.
            scale: A factor to scale the size the turtle.
            lineweight: The thickness of the lines composing the shape.

        Yields:
            TurtleGraphicsError: For invalid shape names.
        """
        t = Turtle()
        t.shape(shape)
        t.shapesize(scale, scale, lineweight)
        t.penup()
        t.hideturtle()
        return t

