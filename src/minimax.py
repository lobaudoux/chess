inf = float("inf")


def search(game, player, prune=True):

    def max_value(game, alpha, beta, depth):
        if player.cutoff(game, depth):
            return player.evaluate(game), None
        val = -inf
        action = None
        for a in player.successors(game):
            piece, move = a
            old_pos = piece.get_pos()
            old_has_moved = piece.has_moved
            piece_taken = game.apply_move(piece, move)
            v, _ = min_value(game, alpha, beta, depth+1)
            game.undo_move(piece, old_pos, old_has_moved, piece_taken)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        return val, action

    def min_value(game, alpha, beta, depth):
        if player.cutoff(game, depth):
            return player.evaluate(game), None
        val = inf
        action = None
        for a in player.successors(game):
            piece, move = a
            old_pos = piece.get_pos()
            old_has_moved = piece.has_moved
            piece_taken = game.apply_move(piece, move)
            v, _ = max_value(game, alpha, beta, depth+1)
            game.undo_move(piece, old_pos, old_has_moved, piece_taken)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    _, action = max_value(game, -inf, inf, 0)
    return action
