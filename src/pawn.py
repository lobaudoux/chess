from piece import *
from GUI import *


class Pawn(Piece):
    def draw(self):
        draw_piece(self.get_pos(), (5, self.player_id))

    def get_moves(self, game):
        moves = []
        if self.player_id == P_BLACK:
            direction = 1
        else:
            direction = -1
        if not self.has_moved and game.board[self.x][self.y+direction] is None \
                and game.board[self.x][self.y+(direction*2)] is None:
            moves.append((self.x, self.y+(direction*2)))
        if 0 <= self.y+direction < size_y:
            if game.board[self.x][self.y+direction] is None:
                moves.append((self.x, self.y+direction))
            if self.x-1 >= 0 and game.board[self.x-1][self.y+direction] is not None \
                    and game.board[self.x-1][self.y+direction].player_id != self.player_id:
                moves.append((self.x-1, self.y + direction))
            if self.x+1 < size_x and game.board[self.x+1][self.y+direction] is not None \
                    and game.board[self.x+1][self.y+direction].player_id != self.player_id:
                moves.append((self.x+1, self.y + direction))
        return moves
