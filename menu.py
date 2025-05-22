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
    win.fill(BG_COLOR)
    draw_text(win, "Game Over! The ghost caught you.", (255, 0, 0), 30, -20)
    draw_text(win, "Press R to Retry or Q to Quit", (255, 255, 255), 25, 30)
    pygame.display.update()
