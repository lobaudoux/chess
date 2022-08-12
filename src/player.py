from pawn import *
from rook import *
from knight import *
from bishop import *
from queen import *
from king import *


class Player:
    def __init__(self, player_id, type, pawns, rooks, knights, bishops, queens, king):
        self.player_id = player_id
        self.type = type
        self.pawns = pawns
        self.rooks = rooks
        self.knights = knights
        self.bishops = bishops
        self.queens = queens
        self.king = king

    def get_pieces(self):
        return self.pawns + self.rooks + self.knights + self.bishops + self.queens + [self.king]

    def remove(self, piece):
        if isinstance(piece, Pawn):
            self.pawns.remove(piece)
        elif isinstance(piece, Rook):
            self.rooks.remove(piece)
        elif isinstance(piece, Knight):
            self.knights.remove(piece)
        elif isinstance(piece, Bishop):
            self.bishops.remove(piece)
        elif isinstance(piece, Queen):
            self.queens.remove(piece)

    def add(self, piece):
        if isinstance(piece, Pawn):
            self.pawns.append(piece)
        elif isinstance(piece, Rook):
            self.rooks.append(piece)
        elif isinstance(piece, Knight):
            self.knights.append(piece)
        elif isinstance(piece, Bishop):
            self.bishops.append(piece)
        elif isinstance(piece, Queen):
            self.queens.append(piece)

    def value(self, scores):

        return len(self.pawns)*scores[0]+len(self.rooks)*scores[1]+len(self.knights)*scores[2]+\
               len(self.bishops)*scores[3]+len(self.queens)*scores[4]

    def __str__(self):
        s = ""
        for piece in self.get_pieces():
            s += str(piece)+"\n"
        return s
