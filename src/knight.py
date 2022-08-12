from piece import *
from GUI import *


class Knight(Piece):
    def draw(self):
        draw_piece(self.get_pos(), (3, self.player_id))

    def get_moves(self, game):
        moves = []
        directions = [(-1, -2), (-2, -1), (1, -2), (2, -1), (-1, 2), (-2, 1), (1, 2), (2, 1)]
        for (dx, dy) in directions:
            nx, ny = self.x+dx, self.y+dy
            if 0 <= nx < size_x and 0 <= ny < size_y \
                    and (game.board[nx][ny] is None or game.board[nx][ny].player_id != self.player_id):
                moves.append((nx, ny))
        return moves
