import pygame

pygame.init()

size_case = 64
size_x = 8
size_y = 8
board_x, board_y = (size_case*size_x, size_case*size_y)
res_x, res_y = (board_x, board_y)

HIGHLIGHT_ON = False
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HL_SELECTED = (0, 0, 255)
HL_MOVES = (255, 255, 0)
HL_LAST_MOVE = (0, 255, 0)
HL_CHECK = (255, 0, 0)
HL_THICKNESS = 0.0625
MENU_BACKGROUND = (150, 150, 150)
MENU_BACKGROUND_ALPHA = 200
MENU_OFFSET = 4                 # set the distance between the options, should be an even number
BUTTON_BACKGROUND = (100, 100, 100)
BUTTON_OUTSIDE = (200, 200, 200)
BUTTON_FONT = pygame.font.SysFont("monospace", round(15*size_case/64))
BUTTON_TEXT_COLOR = WHITE
BUTTON_WIDTH = 100*board_x/512
BUTTON_HEIGHT = 30*board_y/512

P_BLACK = 0
P_WHITE = 1
HUMAN = 0
IA = 1
PAT = 2
UNSELECTED = (-1, -1)
