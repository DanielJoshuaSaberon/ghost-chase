import pygame
from maze import TILE_SIZE
from pathfinding import a_star

GHOST_COLOR = (255, 0, 0)  # Red color for ghost

class Ghost:
    def __init__(self, row, col):
        # Ghost's grid position
        self.row = row
        self.col = col
        self.path = []  # Current path to player (list of nodes)

    def update(self, target):
        """
        Update ghost's position by finding path to the target (player).
        Moves the ghost one step closer along the path each update.
        """
        start = (self.row, self.col)
        goal = (target.row, target.col)

        # Compute shortest path using A*
        self.path = a_star(start, goal)

        # If a path exists and it has more than one step,
        # move ghost to the next position on the path.
        if len(self.path) > 1:
            next_node = self.path[1]
            self.row, self.col = next_node

    def draw(self, win):
        """
        Draw the ghost as a circle centered inside its grid tile.
        """
        px = self.col * TILE_SIZE + TILE_SIZE // 2
        py = self.row * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(win, GHOST_COLOR, (px, py), TILE_SIZE // 3)
