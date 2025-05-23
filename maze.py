import pygame

# Size of each tile in pixels (width and height of each maze cell)
TILE_SIZE = 40

# Colors used for drawing the maze tiles
BG_COLOR = (0, 0, 0)  # Black color for empty spaces where player and ghost can move
WALL_COLOR = (0, 0, 255)  # Blue color for walls that block movement

# Maze dimensions: 15 rows and 15 columns, making it a 15x15 grid
ROWS, COLS = 20, 20

# Maze layout as a 2D list (15 rows x 15 columns)
# 1 represents a wall (impassable tile)
# 0 represents a path (walkable tile)
# 20X20
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#15X15
# MAZE = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
#     [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
#     [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
#     [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
#     [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
#     [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]

# 10x10
# MAZE = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
#     [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
#     [1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
#     [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
#     [1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]

def draw_maze(win):
    """
    Draw the maze grid on the pygame window.
    Each cell is drawn as a rectangle:
    - Blue if it is a wall (1)
    - Black if it is an empty path (0)

    Parameters:
    - win: pygame Surface on which to draw the maze
    """
    for row in range(ROWS):  # Iterate over every row in the maze
        for col in range(COLS):  # Iterate over every column in the maze
            # Choose the color for the tile:
            # WALL_COLOR if tile is 1 (wall), else BG_COLOR (empty space)
            color = WALL_COLOR if MAZE[row][col] == 1 else BG_COLOR

            # Calculate the position and size of the rectangle to draw
            # X position is column index times tile width
            # Y position is row index times tile height
            rectangle = pygame.Rect(
                col * TILE_SIZE,  # x coordinate on screen
                row * TILE_SIZE,  # y coordinate on screen
                TILE_SIZE,  # width of the tile
                TILE_SIZE  # height of the tile
            )

            # Draw the rectangle (tile) with the chosen color onto the window
            pygame.draw.rect(win, color, rectangle)