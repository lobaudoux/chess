from constants import *


def get_color(player_id):
    if player_id == P_BLACK:
        return "black"
    else:
        return "white"


def other_player(player_id):
    return (player_id+1) % 2
