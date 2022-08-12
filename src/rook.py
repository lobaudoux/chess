from piece import *
from GUI import *


class Rook(Piece):
    def draw(self):
        draw_piece(self.get_pos(), (2, self.player_id))

    def get_moves(self, game):
        moves = []

        # right
        cur_x = self.x+1
        while cur_x < size_x and game.board[cur_x][self.y] is None:
            moves.append((cur_x, self.y))
            cur_x += 1
        if cur_x < size_x and game.board[cur_x][self.y].player_id != self.player_id:
            moves.append((cur_x, self.y))

        # left
        cur_x = self.x-1
        while cur_x >= 0 and game.board[cur_x][self.y] is None:
            moves.append((cur_x, self.y))
            cur_x -= 1
        if cur_x >= 0 and game.board[cur_x][self.y].player_id != self.player_id:
            moves.append((cur_x, self.y))

        # down
        cur_y = self.y+1
        while cur_y < size_y and game.board[self.x][cur_y] is None:
            moves.append((self.x, cur_y))
            cur_y += 1
        if cur_y < size_y and game.board[self.x][cur_y].player_id != self.player_id:
            moves.append((self.x, cur_y))

        # up
        cur_y = self.y-1
        while cur_y >= 0 and game.board[self.x][cur_y] is None:
            moves.append((self.x, cur_y))
            cur_y -= 1
        if cur_y >= 0 and game.board[self.x][cur_y].player_id != self.player_id:
            moves.append((self.x, cur_y))
        return moves
