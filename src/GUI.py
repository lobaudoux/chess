import os
import pygame

from constants import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
display = pygame.display.set_mode((res_x, res_y))
pygame.display.set_caption("Chess")
menu_surface = pygame.Surface((res_x, res_y))

chess_sprite = pygame.image.load("../res/chess_sprite.png")
chess_sprite = pygame.transform.scale(chess_sprite, (round(384*size_case/64), round(128*size_case/64)))


def draw_board():
    for x in range(size_x):
        for y in range(size_y):
            if (x+y) % 2 == 0:
                pygame.draw.rect(display, WHITE, (size_case * x, size_case * y, size_case, size_case))
            else:
                pygame.draw.rect(display, BLACK, (size_case * x, size_case * y, size_case, size_case))


def draw_highlight(pos, color, thickness):
    x, y = pos
    pygame.draw.rect(display, color, (size_case * x, size_case * y, size_case, thickness))
    pygame.draw.rect(display, color, (size_case * x, (size_case * (y+1)-thickness),
                                      size_case, thickness))
    pygame.draw.rect(display, color, (size_case * x, size_case * y, thickness, size_case))
    pygame.draw.rect(display, color, (size_case * (x+1)-thickness, size_case * y,
                                      thickness, size_case))


def draw_piece(pos, pict_coord):
    x, y = pos
    px, py = pict_coord
    display.blit(chess_sprite, (x * size_case, y * size_case), (px * size_case, py * size_case, size_case, size_case))


def draw_menu(menu):
    pygame.draw.rect(menu_surface, MENU_BACKGROUND, (0, 0, board_x, board_y))
    menu_surface.set_alpha(MENU_BACKGROUND_ALPHA)
    display.blit(menu_surface, (0, 0))
    for button in menu.buttons:
        button.draw()


def draw_button(button):
    cx, cy = button.center
    pygame.draw.rect(display, BUTTON_BACKGROUND, (cx-(button.w/2), cy-(button.h/2), button.w, button.h))
    pygame.draw.rect(display, BUTTON_OUTSIDE, (cx-(button.w / 2), cy-(button.h / 2), button.w, button.h), 1)
    button_text = BUTTON_FONT.render(button.text, 1, BUTTON_TEXT_COLOR)
    bx, by = button.center
    display.blit(button_text, (bx-(button_text.get_width()/2), by-(button_text.get_height()/2)))
