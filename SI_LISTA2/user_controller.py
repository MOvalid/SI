from HalmaBoard import HalmaBoard
from DecisionTree import DTree
from heuristic_functions import *
from time import time, sleep
from distance_functions import *
from utils import print_game_stats
import argparse
import re
import random

HEURISTIC_FN_CONVERTER = {
    1 : mobility_of_discs,
    2 : distance_of_target_base,
    3 : follow_as_close_to_the_diagonal,
    4 : random_rate,
    5 : random_rate_but_closer_to_base,
    6 : move_of_the_farthest_cell_as_far_as_possible
}

DISTANCE_FN_CONVERTER = {
    1 : euclidean_distance,
    2 : manhattan_distance,
    3 : chebyshev_distance
}

HEURISTIC_FN_ARG_HELP_TEXT =     f"Choose heuristic function of your enemy:\n \
        1 - {HEURISTIC_FN_CONVERTER[0].__name__}, \
        2 - {HEURISTIC_FN_CONVERTER[1].__name__}, \
        3 - {HEURISTIC_FN_CONVERTER[2].__name__}, \
        4 - {HEURISTIC_FN_CONVERTER[3].__name__}, \
        5 - {HEURISTIC_FN_CONVERTER[4].__name__}, \
        6 - {HEURISTIC_FN_CONVERTER[5].__name__}
"

DISTANCE_FN_ARG_HELP_TEXT =     "Choose distance function to apply in heuristic function:\n \
        1 - Euclidean,\
        2 - Manhattan,\
        3 - Chebyshev"


parser = argparse.ArgumentParser()
parser.add_argument('heuristic_fn', type=int, choices=range(1,7), help=HEURISTIC_FN_ARG_HELP_TEXT)
parser.add_argument('distance_fn', type=int, choices=range(1,4), help=DISTANCE_FN_ARG_HELP_TEXT)

REGEX_FORMULA = re.compile(r'^\s*([0-9]|1[0-5])\s*,\s*([0-9]|1[0-5])\s*$')

def check_user_input(user_input):
    return bool(REGEX_FORMULA.match(user_input))

def parse_user_input(user_input):
    return tuple(map(int, user_input.split(',')))

def check_disc_from_user_input(game, disc):
    (x, y) = disc
    return game.board[x][y] == WHITE_PLAYER_CELL


def start_the_game(heuristic_fn, distance_fn):

    game = HalmaBoard()
    start_time = time()

    print(game)

    moves_counter = 0

    game.make_random_move(AI_CELL_TYPE)
    
    while(True):
        moves_counter += 1
        print(game)
        print_game_stats(moves_counter, start_time)

        player_type = AI_CELL_TYPE if moves_counter % 2 == 0 else USER_CELL_TYPE
        if game.has_player_won(player_type):
            break

        if moves_counter % 2 == 1: # user move
            cell_to_move = get_user_cell_to_move(game)
            move = get_user_move(game, cell_to_move)
           
            game.make_move_on_board(
                cell_to_move[0],
                cell_to_move[1],
                move[0],
                move[1]
            )

        else:
            ai_dtree = DTree(game, heuristic_fn, distance_fn)
            child_index, _ = ai_dtree.minimax()
            ai_cell_to_move = ai_dtree.root.children[child_index].start_cell
            ai_move = ai_dtree.root.children[child_index].end_cell
            game.make_move_on_board(
                ai_cell_to_move[0],
                ai_cell_to_move[1],
                ai_move[0],
                ai_move[1]
            )
        
def get_user_cell_to_move(game):
    while(True):
        user_disc_choice = input("Choose disc to move: ")
        if not check_user_input(user_disc_choice):
            print("Invalid value! Try again :D")

        cell_to_move = parse_user_input(user_disc_choice)

        if not check_disc_from_user_input(game, cell_to_move):
            print("This is not your disc! Try again!\n")
        elif not game.is_cell_movable(cell_to_move):
            print("You can't move this cell! Try again!\n")
        else:
            return cell_to_move

def get_user_move(game, cell_to_move):
     while(True):
        user_move_choice = input("Choose cell to moving your disc: ")
        if not check_user_input(user_move_choice):
            print("Invalid value! Try again :D")
        else:
            move = parse_user_input(user_move_choice)
            if not game.can_make_move(cell_to_move[0], cell_to_move[1], move[0], move[1]):
                print("This move is invalid! Try again!\n")
            else:
                return move





if __name__ == '__main__':
    args = parser.parse_args()
    heuristic_fn = HEURISTIC_FN_CONVERTER[args.heuristic_fn]
    distance_fn = DISTANCE_FN_CONVERTER[args.distance_fn]

    start_the_game(heuristic_fn, distance_fn)