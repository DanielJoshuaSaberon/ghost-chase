import pygame
from maze import TILE_SIZE, draw_maze, ROWS, COLS
from player import Player
from ghost import Ghost
from menu import show_menu, show_game_over

# Frames per second (FPS) controls game speed and update rate
FPS = 20

# Define possible game states as constants
MENU = "menu"
GAME = "game"


def game_loop(win):
    """
    Main game loop where all the game logic runs:
    - Handles player input (arrow keys)
    - Updates ghost movement using A* pathfinding
    - Detects collisions between player and ghost
    - Draws the maze, player, ghost, and UI elements
    - Handles the game over screen and restart/quit options

    Args:
        win (pygame.Surface): The pygame window surface to draw on

    Returns:
        str: Next game state ("game" to restart, or "menu" to quit)
    """
    clock = pygame.time.Clock()  # Clock to control FPS
    player = Player(1, 1)  # Initialize player near top-left corner (row=1, col=1)
    ghost = Ghost(ROWS - 2, COLS - 2)  # Initialize ghost near bottom-right corner
    frame_count = 0  # Frame counter to control ghost movement speed
    ghost_move_delay = 3  # Ghost moves once every 3 frames to slow it down
    game_over = False  # Flag to track if the player is caught by ghost

    # Main game loop (runs every frame)
    while True:
        clock.tick(FPS)  # Limit loop to run at FPS times per second
        frame_count += 1  # Increment frame counter

        # Event handling loop: processes system and user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Player clicked window close button -> return to menu to exit game
                return MENU

        # Handle player input only if game is not over
        keys = pygame.key.get_pressed()  # Get current key states
        if not game_over:
            # Check arrow keys and move player accordingly
            if keys[pygame.K_UP]:
                player.move(-1, 0)  # Move player one tile up
            elif keys[pygame.K_DOWN]:
                player.move(1, 0)   # Move player one tile down
            elif keys[pygame.K_LEFT]:
                player.move(0, -1)  # Move player one tile left
            elif keys[pygame.K_RIGHT]:
                player.move(0, 1)   # Move player one tile right

            # Update ghost movement only every 'ghost_move_delay' frames for pacing
            if frame_count % ghost_move_delay == 0:
                ghost.update(player)  # Ghost finds path and moves toward player

            # Check collision: if ghost occupies same grid tile as player
            if ghost.row == player.row and ghost.col == player.col:
                game_over = True  # Set game over flag

        # Drawing section — render everything on screen
        win.fill((0, 0, 0))    # Clear the screen to black before drawing new frame
        draw_maze(win)         # Draw maze walls and paths
        player.draw(win)       # Draw player sprite or shape
        ghost.draw(win)        # Draw ghost sprite or shape

        # If the game is over, show the game over screen and wait for user input
        if game_over:
            show_game_over(win)  # Display game over message/instructions
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return MENU  # Player closes window, return to menu
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return GAME  # Restart game on pressing 'r'
                        elif event.key == pygame.K_q:
                            return MENU  # Quit to menu on pressing 'q'

        # Update the full display surface to the screen
        pygame.display.update()


def main():
    """
    Entry point of the game:
    - Initializes pygame and window
    - Sets game window icon and title
    - Controls game state flow between menu and gameplay
    """
    pygame.init()  # Initialize all pygame modules

    # Load and set game window icon (small image displayed on the window)
    icon = pygame.image.load("public/ghostChaseLogo.png")
    pygame.display.set_icon(icon)

    # Create the game window with size based on maze grid dimensions
    Window = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE))
    pygame.display.set_caption("GHOST CHASE!!")  # Set window title

    state = MENU  # Start in the menu state

    # Main application loop controlling state transitions
    while True:
        if state == MENU:
            show_menu(Window)  # Show the start menu screen

            # Menu input loop - waits for player to start or quit
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # Cleanly exit pygame
                        return          # Quit the program

                    # If spacebar pressed, start the game
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        state = GAME
                        break  # Exit menu loop and start gameplay
                if state == GAME:
                    break

        elif state == GAME:
            # Run the game loop and update the game state based on return value
            state = game_loop(Window)


if __name__ == "__main__":
    main()  # Run the main function when script is executed
