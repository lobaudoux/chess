from piece import *
from GUI import *


class King(Piece):
    def draw(self):
        draw_piece(self.get_pos(), (0, self.player_id))

    def get_moves(self, game):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1)]
        for (dx, dy) in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < size_x and 0 <= ny < size_y \
                    and (game.board[nx][ny] is None or game.board[nx][ny].player_id != self.player_id):
                moves.append((nx, ny))
        # castling
        if not self.has_moved and game.board[0][self.y] is not None and not game.board[0][self.y].has_moved \
                and game.board[1][self.y] is None and game.board[2][self.y] is None and game.board[3][self.y] is None\
                and not game.is_checked(self.player_id):
            moves.append((2, self.y))
        if not self.has_moved and game.board[size_x-1][self.y] is not None and not game.board[size_x-1][self.y].has_moved \
                and game.board[5][self.y] is None and game.board[6][self.y] is None and not game.is_checked(self.player_id):
            moves.append((6, self.y))
        return moves
