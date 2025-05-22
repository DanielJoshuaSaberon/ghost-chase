import pygame
from maze import TILE_SIZE
from pathfinding import a_star

class Ghost:
    def __init__(self, row, col, image_path="public/ghost.png"):
        """
        Initialize a Ghost object at a specific grid position.

        Args:
            row (int): The row index of the ghost in the grid.
            col (int): The column index of the ghost in the grid.
            image_path (str): File path to the ghost image.
        """
        # Set initial grid position of the ghost
        self.row = row
        self.col = col

        # List to store the current path to the player (each element is a (row, col) tuple)
        self.path = []

        # Load the ghost image from the given file path
        # convert_alpha() is used to keep transparency if the image has any
        self.image = pygame.image.load(image_path).convert_alpha()

        # Scale the loaded image to match the tile size of the grid
        # This ensures the image fits perfectly inside one grid tile
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def update(self, target):
        """
        Update the ghost's position to move closer to the target (e.g., player).

        Uses the A* pathfinding algorithm to find the shortest path from the ghost
        to the target's current grid position, then moves the ghost one step along
        that path.

        Args:
            target: An object that has 'row' and 'col' attributes representing
                    the target's grid position.
        """
        # Current ghost position as a tuple (row, col)
        start = (self.row, self.col)

        # Target's position as a tuple (row, col)
        goal = (target.row, target.col)

        # Use the A* algorithm to calculate the shortest path from ghost to target
        # The returned path is a list of grid coordinates from start to goal
        self.path = a_star(start, goal)

        # If the path exists and is longer than 1 step (meaning the ghost is not
        # already on the target), move the ghost to the next node on the path
        if len(self.path) > 1:
            next_node = self.path[1]  # path[0] is current position, so path[1] is next step
            self.row, self.col = next_node

    def draw(self, win):
        """
        Draw the ghost's image on the game window at its current position.

        Args:
            win (pygame.Surface): The surface (window) to draw the ghost image on.
        """
        # Calculate the pixel position (top-left corner) of the ghost based on
        # its grid coordinates and the tile size. Multiplying col by TILE_SIZE
        # gives the x position, and row by TILE_SIZE gives the y position.
        px = self.col * TILE_SIZE
        py = self.row * TILE_SIZE

        # Draw (blit) the ghost image onto the window surface at the calculated position
        win.blit(self.image, (px, py))
