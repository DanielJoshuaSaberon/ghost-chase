import pygame
from maze import COLS, ROWS, TILE_SIZE

BG_COLOR = (6, 7, 15)

def draw_text(win, message, color, size, y_offset=0):
    font = pygame.font.SysFont("Arial", size)
    text = font.render(message, True, color)
    rect = text.get_rect(center=(COLS * TILE_SIZE // 2, ROWS * TILE_SIZE // 2 + y_offset))
    win.blit(text, rect)

def show_menu(win):
    clock = pygame.time.Clock()
    blink = True
    blink_timer = 0

    # Load title image
    title_img = pygame.image.load("public/title.png").convert_alpha()
    title_img = pygame.transform.scale(title_img, (500, 500))
    img_rect = title_img.get_rect(center=(COLS * TILE_SIZE // 2, ROWS * TILE_SIZE // 2 - 60))

    running = True
    while running:
        win.fill(BG_COLOR)
        win.blit(title_img, img_rect)

        # Blink logic: toggle every 500ms
        blink_timer += clock.get_time()
        if blink_timer >= 500:
            blink = not blink
            blink_timer = 0

        if blink:
            draw_text(win, "Press SPACE twice to Start", (255, 255, 255), 30, 100)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False  # Exit the menu loop


def show_game_over(win):
    """
    Displays the game over screen with selectable options.
    Allows the player to choose between retrying the game or quitting to the menu.

    Args:
        win (pygame.Surface): The pygame window surface to draw on

    Returns:
        str: The selected option ("Retry" or "Quit to Menu")
    """
    from maze import TILE_SIZE, COLS, ROWS
    BG_COLOR = (6, 7, 15)  # Background color
    options = ["Retry", "Quit to Menu"]  # Menu options
    selected = 0  # Currently selected option index
    clock = pygame.time.Clock()

    def draw_text(win, message, color, size, y_offset=0):
        """
        Helper function to draw centered text with vertical offset
        """
        font = pygame.font.SysFont("Arial", size)
        text = font.render(message, True, color)
        rect = text.get_rect(center=(COLS * TILE_SIZE // 2, ROWS * TILE_SIZE // 2 + y_offset))
        win.blit(text, rect)

    # Game over menu loop
    while True:
        win.fill(BG_COLOR)  # Clear screen
        draw_text(win, "Game Over! The ghost caught you.", (255, 0, 0), 30, -60)  # Title message

        # Draw all menu options, highlighting the selected one
        for i, option in enumerate(options):
            color = (0, 102, 204) if i == selected else (255, 255, 255)  # Blue highlight
            draw_text(win, option, color, 26, 20 + i * 40)

        pygame.display.update()  # Refresh display
        clock.tick(60)  # Cap at 60 FPS

        # Handle user input for navigating and selecting options
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)  # Move selection up
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)  # Move selection down
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return options[selected]  # Return selected option
