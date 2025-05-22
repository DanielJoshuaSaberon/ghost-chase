import pygame
from maze import ROWS, COLS, TILE_SIZE, draw_maze, ROWS, COLS
from player import Player
from ghost import Ghost
from menu import show_menu, show_game_over

# Set frame rate for the game
FPS = 5

# Game states
MENU = "menu"
GAME = "game"


def game_loop(win):
    """
    Main game loop where the player and ghost move and interact.
    Handles input, game logic, rendering, and game over state.

    Returns:
    - GAME: if the player chooses to retry after losing.
    - MENU: if the player quits to menu.
    """
    clock = pygame.time.Clock()
    player = Player(1, 1)  # Starting position of the player
    ghost = Ghost(ROWS-2 , COLS-2)  # Starting position of the ghost
    frame_count = 0
    ghost_move_delay = 3  # Delay ghost movement every few frames
    game_over = False

    while True:
        clock.tick(FPS)
        frame_count += 1

        # Handle quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MENU

        # Handle player input (arrow keys) only if not game over
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_UP]:
                player.move(-1, 0)
            elif keys[pygame.K_DOWN]:
                player.move(1, 0)
            elif keys[pygame.K_LEFT]:
                player.move(0, -1)
            elif keys[pygame.K_RIGHT]:
                player.move(0, 1)

            # Update ghost pathfinding only every few frames
            if frame_count % ghost_move_delay == 0:
                ghost.update(player)

            # Check for collision between player and ghost
            if ghost.row == player.row and ghost.col == player.col:
                game_over = True

        # Draw everything
        win.fill((0, 0, 0))  # Clear the screen
        draw_maze(win)  # Draw maze walls
        player.draw(win)  # Draw player
        ghost.draw(win)  # Draw ghost

        # Handle game over UI
        if game_over:
            show_game_over(win)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return MENU
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return GAME  # Restart game
                        elif event.key == pygame.K_q:
                            return MENU  # Return to menu

        pygame.display.update()


def main():
    """
    Main function that controls the game state.
    Starts with menu, then enters the game loop.
    """
    pygame.init()
    Window = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE))
    pygame.display.set_caption("Pac-Man Style Chase")

    state = MENU  # Initial state is the main menu

    while True:
        if state == MENU:
            show_menu(Window)  # Display the menu screen
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # If a key is pressed and if space Key is pressed
                        state = GAME
                        break  # Exit menu loop and start game
                if state == GAME:
                    break

        elif state == GAME:
            state = game_loop(Window)  # Play game and return new state


if __name__ == "__main__":
    main()
