import sys

from GUI import *
from player import *
from menu import *
from helpers import *
from my_agent import *


class Chess:
    def __init__(self, white_type, black_type):
        # initialize board with empty tiles
        self.board = [[None for _ in range(size_x)] for _ in range(size_y)]

        # player white pieces
        ppw = [Pawn((i, 6), P_WHITE) for i in range(size_x)]
        r1pw = Rook((0, 7), P_WHITE)
        r2pw = Rook((7, 7), P_WHITE)
        k1pw = Knight((1, 7), P_WHITE)
        k2pw = Knight((6, 7), P_WHITE)
        b1pw = Bishop((2, 7), P_WHITE)
        b2pw = Bishop((5, 7), P_WHITE)
        qpw = Queen((3, 7), P_WHITE)
        kpw = King((4, 7), P_WHITE)

        self.board[0][7] = r1pw
        self.board[7][7] = r2pw
        self.board[1][7] = k1pw
        self.board[6][7] = k2pw
        self.board[2][7] = b1pw
        self.board[5][7] = b2pw
        self.board[3][7] = qpw
        self.board[4][7] = kpw
        for i in range(size_x):
            self.board[i][6] = ppw[i]
        if white_type == IA:
            pw = MyAgent(P_WHITE, white_type, ppw, [r1pw, r2pw], [k1pw, k2pw], [b1pw, b2pw], [qpw], kpw)
        else:
            pw = Player(P_WHITE, white_type, ppw, [r1pw, r2pw], [k1pw, k2pw], [b1pw, b2pw], [qpw], kpw)

        # player black pieces
        ppb = [Pawn((i, 1), P_BLACK) for i in range(size_x)]
        r1pb = Rook((0, 0), P_BLACK)
        r2pb = Rook((7, 0), P_BLACK)
        k1pb = Knight((1, 0), P_BLACK)
        k2pb = Knight((6, 0), P_BLACK)
        b1pb = Bishop((2, 0), P_BLACK)
        b2pb = Bishop((5, 0), P_BLACK)
        qpb = Queen((3, 0), P_BLACK)
        kpb = King((4, 0), P_BLACK)

        self.board[0][0] = r1pb
        self.board[7][0] = r2pb
        self.board[1][0] = k1pb
        self.board[6][0] = k2pb
        self.board[2][0] = b1pb
        self.board[5][0] = b2pb
        self.board[3][0] = qpb
        self.board[4][0] = kpb
        for i in range(size_x):
            self.board[i][1] = ppb[i]
        if black_type == IA:
            pb = MyAgent(P_BLACK, black_type, ppb, [r1pb, r2pb], [k1pb, k2pb], [b1pb, b2pb], [qpb], kpb)
        else:
            pb = Player(P_BLACK, black_type, ppb, [r1pb, r2pb], [k1pb, k2pb], [b1pb, b2pb], [qpb], kpb)

        self.players = [pb, pw]
        self.sx, self.sy = UNSELECTED
        self.selected_moves = None
        self.turn = P_WHITE
        self.last_move = []
        self.menu = Menu(["Queen", "Rook", "Knight", "Bishop"])

    def click_at(self, pos):
        x, y = pos
        x, y = int(x / size_case), int(y / size_case)
        if (self.sx, self.sy) == UNSELECTED and self.board[x][y] is not None and self.board[x][y].player_id == self.turn:
            self.select((x, y))
        elif (self.sx, self.sy) != UNSELECTED:
            if (x, y) in self.selected_moves:
                selected_piece = self.board[self.sx][self.sy]
                # check for pawn promotion
                if isinstance(selected_piece, Pawn) and ((selected_piece.player_id == P_WHITE and y == 0)
                                                         or (selected_piece.player_id == P_BLACK and y == size_y-1)):
                    self.menu.show()
                    self.draw()
                    while self.menu.is_visible():
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                button_clicked = self.menu.collide(pos)
                                if button_clicked is not None:
                                    self.apply_move(selected_piece, (x, y, button_clicked.text))
                                    self.menu.hide()
                else:
                    self.apply_move(selected_piece, (x, y))
                self.last_move = [(self.sx, self.sy), (x, y)]
                self.unselect()
            else:
                if self.board[x][y] is not None and self.board[x][y].player_id == self.turn:
                    self.select((x, y))
                else:
                    self.unselect()

    def select(self, pos):
        self.sx, self.sy = pos
        piece_selected = self.board[self.sx][self.sy]
        self.selected_moves = self.filter_moves(piece_selected, piece_selected.get_moves(self))

    def unselect(self):
        self.sx, self.sy = UNSELECTED
        self.selected_moves = None

    def change_turn(self):
        self.turn = (self.turn+1) % 2

    def is_checked(self, player_id):
        kx, ky = self.players[player_id].king.get_pos()

        # right
        cur_x, cur_y, skip_loop = kx+1, ky, False
        if cur_x < size_x and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King):
                return True
        if not skip_loop:
            while cur_x < size_x and self.board[cur_x][cur_y] is None:
                cur_x += 1
            if cur_x < size_x and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen)):
                return True

        # left
        cur_x, cur_y, skip_loop = kx-1, ky, False
        if cur_x >= 0 and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King):
                return True
        if not skip_loop:
            while cur_x >= 0 and self.board[cur_x][cur_y] is None:
                cur_x -= 1
            if cur_x >= 0 and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen)):
                return True

        # down
        cur_x, cur_y, skip_loop = kx, ky+1, False
        if cur_y < size_y and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King):
                return True
        if not skip_loop:
            while cur_y < size_y and self.board[cur_x][cur_y] is None:
                cur_y += 1
            if cur_y < size_y and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen)):
                return True

        # up
        cur_x, cur_y, skip_loop = kx, ky-1, False
        if cur_y >= 0 and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King):
                return True
        if not skip_loop:
            while cur_y >= 0 and self.board[cur_x][cur_y] is None:
                cur_y -= 1
            if cur_y >= 0 and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Rook) or isinstance(self.board[cur_x][cur_y], Queen)):
                return True

        # up right
        cur_x, cur_y, skip_loop = kx+1, ky-1, False
        if cur_x < size_x and cur_y >= 0 and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King) or \
                    (isinstance(self.board[cur_x][cur_y], Pawn) and self.board[cur_x][cur_y].player_id == P_BLACK):
                return True
        if not skip_loop:
            while cur_x < size_x and cur_y >= 0 and self.board[cur_x][cur_y] is None:
                cur_x += 1
                cur_y -= 1
            if cur_x < size_x and cur_y >= 0 and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y], Queen)):
                return True

        # up left
        cur_x, cur_y, skip_loop = kx-1, ky-1, False
        if cur_x >= 0 and cur_y >= 0 and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King) or \
                    (isinstance(self.board[cur_x][cur_y], Pawn) and self.board[cur_x][cur_y].player_id == P_BLACK):
                return True
        if not skip_loop:
            while cur_x >= 0 and cur_y >= 0 and self.board[cur_x][cur_y] is None:
                cur_x -= 1
                cur_y -= 1
            if cur_x >= 0 and cur_y >= 0 and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y],Queen)):
                return True

        # down right
        cur_x, cur_y, skip_loop = kx+1, ky+1, False
        if cur_x < size_x and cur_y < size_y and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King) or \
                    (isinstance(self.board[cur_x][cur_y], Pawn) and self.board[cur_x][cur_y].player_id == P_WHITE):
                return True
        if not skip_loop:
            while cur_x < size_x and cur_y < size_y and self.board[cur_x][cur_y] is None:
                cur_x += 1
                cur_y += 1
            if cur_x < size_x and cur_y < size_y and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y], Queen)):
                return True

        # down left
        cur_x, cur_y, skip_loop = kx-1, ky+1, False
        if cur_x >= 0 and cur_y < size_y and self.board[cur_x][cur_y] is not None:
            if self.board[cur_x][cur_y].player_id == player_id:
                skip_loop = True
            elif isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y], Queen) or \
                    isinstance(self.board[cur_x][cur_y], King) or \
                    (isinstance(self.board[cur_x][cur_y], Pawn) and self.board[cur_x][cur_y].player_id == P_WHITE):
                return True
        if not skip_loop:
            while cur_x >= 0 and cur_y < size_y and self.board[cur_x][cur_y] is None:
                cur_x -= 1
                cur_y += 1
            if cur_x >= 0 and cur_y < size_y and self.board[cur_x][cur_y].player_id != player_id and \
                    (isinstance(self.board[cur_x][cur_y], Bishop) or isinstance(self.board[cur_x][cur_y], Queen)):
                return True

        # knights
        directions = [(-1, -2), (-2, -1), (1, -2), (2, -1), (-1, 2), (-2, 1), (1, 2), (2, 1)]
        for (dx, dy) in directions:
            cur_x, cur_y = kx+dx, ky+dy
            if 0 <= cur_x < size_x and 0 <= cur_y < size_y and self.board[cur_x][cur_y] is not None \
                    and isinstance(self.board[cur_x][cur_y], Knight) and self.board[cur_x][cur_y].player_id != player_id:
                return True

        return False

    def apply_move(self, piece, move):
        px, py = piece.get_pos()
        if len(move) > 2:
            mx, my, _ = move
        else:
            mx, my = move
        piece_taken = None
        if self.board[mx][my] is not None:
            self.players[other_player(self.turn)].remove(self.board[mx][my])
            piece_taken = self.board[mx][my]
        # check castling
        if isinstance(piece, King) and abs(px-mx) > 1:
            # move the rook to the correct position
            if mx == 2:
                self.board[0][py].move((3, py))
                self.board[3][py] = self.board[0][py]
                self.board[0][py] = None
            if mx == 6:
                self.board[7][py].move((5, py))
                self.board[5][py] = self.board[7][py]
                self.board[7][py] = None
        piece.move((mx, my))
        piece.has_moved = True
        self.board[mx][my] = self.board[px][py]
        self.board[px][py] = None
        if len(move) > 2:
            self.pawn_promotion(move[2], piece)
        self.change_turn()
        return piece_taken

    def undo_move(self, piece, old_pos, old_has_moved, piece_taken):
        old_x, old_y = old_pos
        mx, my = piece.get_pos()
        # undo castling if necessary
        if isinstance(piece, King) and abs(old_x-mx) > 1:
            # move the rook back to its old position
            if mx == 2:
                self.board[3][old_y].move((0, old_y))
                self.board[0][old_y] = self.board[3][old_y]
                self.board[3][old_y] = None
            if mx == 6:
                self.board[5][old_y].move((7, old_y))
                self.board[7][old_y] = self.board[5][old_y]
                self.board[5][old_y] = None
        # undo pawn promotion
        if isinstance(piece, Pawn) and ((piece.player_id == P_WHITE and my == 0)
                                        or (piece.player_id == P_BLACK and my == size_y-1)):
            # put the pawn back to the player and remove the upgraded piece
            self.players[piece.player_id].add(piece)
            self.players[piece.player_id].remove(self.board[mx][my])

        piece.has_moved = old_has_moved
        if piece_taken is not None:
            self.players[piece_taken.player_id].add(piece_taken)
        piece.move(old_pos)
        self.board[mx][my] = piece_taken
        self.board[old_x][old_y] = piece
        self.change_turn()

    def filter_moves(self, piece, moves):
        filtered_moves = []
        for move in moves:
            # simulate move and check if the player is checked
            old_pos = piece.get_pos()
            old_has_moved = piece.has_moved
            piece_taken = self.apply_move(piece, move)
            if not self.is_checked(piece.player_id):
                filtered_moves.append(move)
            # restore old state
            self.undo_move(piece, old_pos, old_has_moved, piece_taken)
        return filtered_moves

    def pawn_promotion(self, type, pawn):
        px, py = pawn.get_pos()
        new_piece = None
        if type == "Queen":
            new_piece = Queen(pawn.get_pos(), pawn.player_id)
        elif type == "Rook":
            new_piece = Rook(pawn.get_pos(), pawn.player_id)
        elif type == "Knight":
            new_piece = Knight(pawn.get_pos(), pawn.player_id)
        elif type == "Bishop":
            new_piece = Bishop(pawn.get_pos(), pawn.player_id)
        new_piece.has_moved = True
        self.players[pawn.player_id].add(new_piece)
        self.players[pawn.player_id].remove(pawn)
        self.board[px][py] = new_piece

    def get_current_player_actions(self):
        actions = []
        player = self.players[self.turn]
        last_pawn = None
        for pawn in player.pawns:
            # need to check if we aren't checking the same pawn again which might happen in case of pawn promotion
            # when removing and adding back the pawn
            if pawn != last_pawn:
                last_pawn = pawn
                for move in self.filter_moves(pawn, pawn.get_moves(self)):
                    mx, my = move
                    if (pawn.player_id == P_WHITE and my == 0) or (pawn.player_id == P_BLACK and my == size_y-1):
                        actions.append((pawn, (mx, my, "Queen")))
                        actions.append((pawn, (mx, my, "Rook")))
                        actions.append((pawn, (mx, my, "Knight")))
                        actions.append((pawn, (mx, my, "Bishop")))
                    else:
                        actions.append((pawn, move))
        for rook in player.rooks:
            for move in self.filter_moves(rook, rook.get_moves(self)):
                actions.append((rook, move))
        for knight in player.knights:
            for move in self.filter_moves(knight, knight.get_moves(self)):
                actions.append((knight, move))
        for bishop in player.bishops:
            for move in self.filter_moves(bishop, bishop.get_moves(self)):
                actions.append((bishop, move))
        for queen in player.queens:
            for move in self.filter_moves(queen, queen.get_moves(self)):
                actions.append((queen, move))
        for move in self.filter_moves(player.king, player.king.get_moves(self)):
            actions.append((player.king, move))
        return actions

    def get_winner(self):
        for piece in self.players[self.turn].get_pieces():
            if len(self.filter_moves(piece, piece.get_moves(self))) > 0:
                return None
        if self.is_checked(self.turn):
            return other_player(self.turn)
        else:
            return PAT

    def check_winner(self):
        winner = self.get_winner()
        if winner is not None:
            if winner == PAT:
                print("Pat !")
            else:
                print("The player "+str(get_color(winner))+" has won !")
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def draw(self):
        # clear previous frame
        display.fill(BLACK)
        # draw board tiles
        draw_board()
        # highlights
        thickness = round(size_case * HL_THICKNESS)
        for pos in self.last_move:
            draw_highlight(pos, HL_LAST_MOVE, thickness)
        if self.is_checked(self.turn):
            king_pos = self.players[self.turn].king.get_pos()
            draw_highlight(king_pos, HL_CHECK, thickness)
        if (self.sx, self.sy) != UNSELECTED:
            draw_highlight((self.sx, self.sy), HL_SELECTED, thickness)
            if HIGHLIGHT_ON:
                for pos in self.selected_moves:
                    draw_highlight(pos, HL_MOVES, thickness)
        # draw pieces
        for player in self.players:
            for piece in player.get_pieces():
                piece.draw()
        # draw menu
        self.menu.draw()
        pygame.display.update()

    def __str__(self):
        s = ""
        for j in range(size_y):
            for i in range(size_x):
                if self.board[i][j] is None:
                    s += "  "
                else:
                    if isinstance(self.board[i][j], Rook):
                        s += "R "
                    elif isinstance(self.board[i][j], Knight):
                        s += "C "
                    elif isinstance(self.board[i][j], Bishop):
                        s += "B "
                    elif isinstance(self.board[i][j], Queen):
                        s += "Q "
                    elif isinstance(self.board[i][j], King):
                        s += "K "
                    elif isinstance(self.board[i][j], Pawn):
                        s += "P "
            s += "\n"
        s += "---------------"
        return s
