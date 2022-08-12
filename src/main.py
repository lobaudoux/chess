import sys

import pygame

from my_agent import *
from chess import Chess


def main(white_type, black_type):
    game = Chess(white_type, black_type)
    game.draw()
    while True:
        cur_player = game.players[game.turn]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and cur_player.type == HUMAN:
                pos = pygame.mouse.get_pos()
                game.click_at(pos)
                game.draw()
                game.check_winner()
        if cur_player.type == IA:
            piece, move = cur_player.get_action(game)
            if len(move) > 2:
                game.last_move = [piece.get_pos(), (move[0], move[1])]
            else:
                game.last_move = [piece.get_pos(), move]
            game.apply_move(piece, move)
            game.draw()
            game.check_winner()
        pygame.time.Clock().tick(FPS)


if __name__ == "__main__":
    if sys.argv == 3:
        main(HUMAN if sys.argv[1] == "HUMAN" else IA, HUMAN if sys.argv[2] == "HUMAN" else IA)
    else:
        main(HUMAN, IA)
