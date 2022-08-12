from piece import *
from GUI import *


class Bishop(Piece):
    def draw(self):
        draw_piece(self.get_pos(), (4, self.player_id))

    def get_moves(self, game):
        moves = []

        # up right
        cur_x = self.x+1
        cur_y = self.y+1
        while cur_x < size_x and cur_y < size_y and game.board[cur_x][cur_y] is None:
            moves.append((cur_x, cur_y))
            cur_x += 1
            cur_y += 1
        if cur_x < size_x and cur_y < size_y and game.board[cur_x][cur_y].player_id != self.player_id:
            moves.append((cur_x, cur_y))

        # up left
        cur_x = self.x-1
        cur_y = self.y+1
        while cur_x >= 0 and cur_y < size_y and game.board[cur_x][cur_y] is None:
            moves.append((cur_x, cur_y))
            cur_x -= 1
            cur_y += 1
        if cur_x >= 0 and cur_y < size_y and game.board[cur_x][cur_y].player_id != self.player_id:
            moves.append((cur_x, cur_y))

        # down right
        cur_x = self.x+1
        cur_y = self.y-1
        while cur_x < size_x and cur_y >= 0 and game.board[cur_x][cur_y] is None:
            moves.append((cur_x, cur_y))
            cur_x += 1
            cur_y -= 1
        if cur_x < size_x and cur_y >= 0 and game.board[cur_x][cur_y].player_id != self.player_id:
            moves.append((cur_x, cur_y))

        # down left
        cur_x = self.x-1
        cur_y = self.y-1
        while cur_x >= 0 and cur_y >= 0 and game.board[cur_x][cur_y] is None:
            moves.append((cur_x, cur_y))
            cur_x -= 1
            cur_y -= 1
        if cur_x >= 0 and cur_y >= 0 and game.board[cur_x][cur_y].player_id != self.player_id:
            moves.append((cur_x, cur_y))
        return moves
