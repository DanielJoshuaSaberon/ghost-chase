import pygame
from maze import TILE_SIZE, MAZE, ROWS, COLS

PLAYER_COLOR = (255, 255, 0)  # Bright yellow for player (used only if fallback drawing needed)

class Player:
    def __init__(self, row, col, image_path="public/player.png"):
        """
        Initialize the Player at the specified grid position.

        Args:
            row (int): The row index on the grid.
            col (int): The column index on the grid.
            image_path (str): Path to the player sprite image file.
        """
        # Player's position on the grid (row, col)
        self.row = row
        self.col = col

        # Load the player image and scale it to the tile size for proper fit
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except pygame.error:
            # In case the image file is missing or can't be loaded,
            # set image to None and fallback to drawing a circle
            print(f"Warning: Could not load image at path: {image_path}")
            self.image = None

    def move(self, dr, dc):
        """
        Attempt to move the player by (dr, dc) tiles.

        Parameters:
            dr (int): Change in row (negative = up, positive = down)
            dc (int): Change in column (negative = left, positive = right)

        Movement only succeeds if the new position is within maze boundaries
        and the target tile is not a wall (represented by 1).
        """
        new_row = self.row + dr
        new_col = self.col + dc

        # Check if new position is inside maze bounds
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            # Check if new position is not a wall (assuming 0 is empty space)
            if MAZE[new_row][new_col] == 0:
                self.row = new_row
                self.col = new_col

    def draw(self, win):
        """
        Draw the player on the game window at its current position.

        If an image is loaded, draw the image aligned to the tile.
        Otherwise, fallback to drawing a yellow circle.
        """
        # Calculate pixel position for the top-left corner of the tile
        px = self.col * TILE_SIZE
        py = self.row * TILE_SIZE

        if self.image:
            # Draw the player image at the calculated position
            win.blit(self.image, (px, py))
        else:
            # Fallback: draw a yellow circle centered in the tile
            center_x = px + TILE_SIZE // 2
            center_y = py + TILE_SIZE // 2
            pygame.draw.circle(win, PLAYER_COLOR, (center_x, center_y), TILE_SIZE // 3)
