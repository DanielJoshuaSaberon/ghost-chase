import pygame
from maze import TILE_SIZE, draw_maze, ROWS, COLS
from player import Player
from ghost import Ghost
from menu import show_menu, show_game_over

# Frames per second (FPS) controls game speed and update rate
FPS = 30

# Define possible game states as constants
MENU = "menu"
GAME = "game"

def game_loop(win):
    """
    Main game loop where all the game logic runs:
    - Handles player input (arrow keys)
    - Updates ghost movement using A* pathfinding
    - Detects collisions between player and ghost or time running out
    - Draws the maze, player, ghost, timer, and UI elements
    - Handles the game over screen and restart/quit options

    Args:
        win (pygame.Surface): The pygame window surface to draw on

    Returns:
        str: Next game state ("game" to restart, or "menu" to quit)
    """
    clock = pygame.time.Clock()  # Clock to control FPS
    player = Player(1, 1)  # Initialize player
    ghost = Ghost(ROWS - 2, COLS - 2)  # Initialize ghost
    frame_count = 0
    ghost_move_delay = 4  # Increased delay to slow down ghost movement
    player_move_delay = 3  # New delay for slowing down player movement
    last_player_move_frame = 0
    game_over = False
    reason = "caught"  # Default reason for game over
    escaped = False  # Flag to track if player escaped

    # Timer setup: 20 seconds countdown
    total_time = 20  # seconds
    start_ticks = pygame.time.get_ticks()  # Start time in milliseconds

    font = pygame.font.SysFont("Arial", 24)  # Font for displaying timer

    while True:
        clock.tick(FPS)
        frame_count += 1

        # Calculate remaining time
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, total_time - seconds_passed)

        # Game over if time runs out
        if time_left == 0 and not game_over:
            game_over = True
            reason = "escaped"  # Player survived
            escaped = True  # Set escaped flag to True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("public/victory.mp3")  # Optional: use a win sound
            pygame.mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MENU

        keys = pygame.key.get_pressed()
        if not game_over:
            # Slow down player movement
            if frame_count - last_player_move_frame >= player_move_delay:
                if keys[pygame.K_UP]:
                    player.move(-1, 0)
                    last_player_move_frame = frame_count
                elif keys[pygame.K_DOWN]:
                    player.move(1, 0)
                    last_player_move_frame = frame_count
                elif keys[pygame.K_LEFT]:
                    player.move(0, -1)
                    last_player_move_frame = frame_count
                elif keys[pygame.K_RIGHT]:
                    player.move(0, 1)
                    last_player_move_frame = frame_count

            # Slow down ghost movement
            if frame_count % ghost_move_delay == 0:
                ghost.update(player)

            if ghost.row == player.row and ghost.col == player.col:
                game_over = True
                reason = "caught"  # Player was caught
                escaped = False  # Set escaped flag to False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("public/gameover.wav")
                pygame.mixer.music.play()

        win.fill((0, 0, 0))
        draw_maze(win)
        player.draw(win)
        ghost.draw(win)

        # Draw countdown timer at top-left
        timer_text = font.render(f"Time Left: {time_left}s", True, (255, 255, 0))
        win.blit(timer_text, (10, 10))

        # If the game is over, show game over screen with reason
        if game_over:
            choice = show_game_over(win, escaped)  # Pass reason to determine message
            pygame.mixer.music.stop()
            pygame.mixer.music.load("public/bgMusic.mp3")
            pygame.mixer.music.play(-1)

            if choice == "Retry":
                return GAME
            elif choice == "Quit to Menu":
                return MENU

        pygame.display.update()


def main():
    """
    Entry point of the game:
    - Initializes pygame and window
    - Sets game window icon and title
    - Controls game state flow between menu and gameplay
    """
    pygame.init()  # Initialize all pygame modules

    pygame.mixer.init()
    pygame.mixer.music.load("public/bgMusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

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