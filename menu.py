import pygame
from maze import COLS, ROWS, TILE_SIZE

BG_COLOR = (0, 0, 0)

def draw_text(win, message, color, size, y_offset=0):
    font = pygame.font.SysFont("Arial", size)
    text = font.render(message, True, color)
    rect = text.get_rect(center=(COLS * TILE_SIZE // 2, ROWS * TILE_SIZE // 2 + y_offset))
    win.blit(text, rect)

def show_menu(win):
    win.fill(BG_COLOR)
    draw_text(win, "PAC-MAN STYLE CHASE", (255, 255, 0), 40, -40)
    draw_text(win, "Press SPACE to Start", (255, 255, 255), 30, 20)
    pygame.display.update()

def show_game_over(win):
    win.fill(BG_COLOR)
    draw_text(win, "Game Over! The ghost caught you.", (255, 0, 0), 30, -20)
    draw_text(win, "Press R to Retry or Q to Quit", (255, 255, 255), 25, 30)
    pygame.display.update()
