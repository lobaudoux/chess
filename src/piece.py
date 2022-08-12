from helpers import *

class Piece:
    def __init__(self, pos, player_id):
        self.x, self.y = pos
        self.player_id = player_id
        self.has_moved = False

    def move(self, pos):
        self.x, self.y = pos

    def get_pos(self):
        return self.x, self.y

    def __str__(self):
        return self.__class__.__name__+" of player "+str(get_color(self.player_id))+\
               " at position : "+str((self.x, self.y))
