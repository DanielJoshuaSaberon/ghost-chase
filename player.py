import pygame
from maze import TILE_SIZE, MAZE, ROWS, COLS

PLAYER_COLOR = (255, 255, 0)  # Bright yellow for player

class Player:
    def __init__(self, row, col):
        # Player's position in terms of grid coordinates (row and column)
        self.row = row
        self.col = col

    def move(self, dr, dc):
        """
        Attempt to move the player by (dr, dc).
        For example, dr=-1 means move up by one tile.
        Only move if the destination is inside the grid and not a wall.
        """
        new_row = self.row + dr
        new_col = self.col + dc

        # Check if inside maze bounds
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            # Check if destination is an empty space (not a wall)
            if MAZE[new_row][new_col] == 0:
                self.row = new_row
                self.col = new_col

    def draw(self, win):
        """
        Draw the player on the window.
        Player is drawn as a circle centered inside its grid tile.
        """
        # Calculate pixel position: center of the tile
        px = self.col * TILE_SIZE + TILE_SIZE // 2
        py = self.row * TILE_SIZE + TILE_SIZE // 2

        # Draw circle with radius roughly 1/3 of the tile size
        pygame.draw.circle(win, PLAYER_COLOR, (px, py), TILE_SIZE // 3)
