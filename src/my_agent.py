import minimax
from player import *

PIECES_SCORE = (1, 5.1, 3.2, 3.33, 8.8)


class MyAgent(Player):
    def __init__(self, player_id, type, pawns, rooks, knights, bishops, queens, king):
        super().__init__(player_id, type, pawns, rooks, knights, bishops, queens, king)
        self.max_depth = 4

    def get_action(self, game):
        return minimax.search(game, self)

    def successors(self, game):
        for action in game.get_current_player_actions():
            yield action

    def cutoff(self, game, depth):
        if depth == self.max_depth or game.get_winner() is not None:
            return True
        else:
            return False

    def evaluate(self, game):
        winner = game.get_winner()
        if winner is None:
            return game.players[self.player_id].value(PIECES_SCORE)-game.players[other_player(self.player_id)].value(PIECES_SCORE)
        elif winner == self.player_id:
            return 1000
        elif winner == other_player(self.player_id):
            return -1000
        elif winner == PAT:
            return game.players[other_player(self.player_id)].value(PIECES_SCORE)-game.players[self.player_id].value(PIECES_SCORE)
