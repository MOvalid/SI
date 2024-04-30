from DecisionTree import DTree
from consts import MINIMAX, ALPHA_BETA, BLACK_PLAYER_CELL, WHITE_PLAYER_CELL, NUMBER_OF_PLAYER_DISCS
from heuristic_functions import try_to_master_the_base
from utils import get_opponent_player_type, print_game_stats
import copy
from time import sleep, time

class Player:

    def __init__(self, heuristic_fn, distance_fn, is_looking_forward, alg_type):
        self.heuristic_fn = heuristic_fn
        self.distance_fn = distance_fn
        self.is_looking_forward = is_looking_forward
        self.alg_type = alg_type
        self.last_moves = []
        self.is_in_endgame = False

    def set_player_type(self, player_type):
        self.player_type = player_type

    def update_game(self, game):
        if self.is_in_endgame or self.is_player_in_endgame(game):
            self.is_in_endgame = True
            self.dtree = DTree(copy.deepcopy(game), self.player_type, try_to_master_the_base, self.distance_fn)
        else:
            self.dtree = DTree(copy.deepcopy(game), self.player_type, self.heuristic_fn, self.distance_fn)

    def is_player_in_endgame(self, game):
        checking_range = range(0,8) if self.player_type == WHITE_PLAYER_CELL else range(8,16)
        discs_in_endgame_area = 0
        for x in checking_range:
            for y in checking_range:
                if game.board[x][y] == self.player_type: discs_in_endgame_area += 1
        return discs_in_endgame_area == NUMBER_OF_PLAYER_DISCS
        
    def make_move(self):
        if self.is_looking_forward:
            child_index, _ = self.dtree.minimax() if self.alg_type == MINIMAX else self.dtree.alpha_beta()
        else:
            child_index, _ = self.dtree.rate_current_game_state()
        # print(f'{self.player_type}: {rate}')
        start_cell, end_cell = self.dtree.get_full_move(child_index)
        if (start_cell, end_cell) in self.last_moves or \
        (end_cell, start_cell) in self.last_moves:
            start_cell, end_cell = self.dtree.root.game_state.get_random_move(self.player_type)

        self.last_moves.append((start_cell, end_cell))
        if len(self.last_moves) > 10:
            self.last_moves.pop(0)

        return start_cell, end_cell


class AIsGameController:
    def __init__(self, game, player1, player2, move_ping = 10):
        self.game = game
        self.player1 = player1
        self.player1.set_player_type(BLACK_PLAYER_CELL)
        self.player2 = player2
        self.player2.set_player_type(WHITE_PLAYER_CELL)
        self.move_ping = move_ping

    def start_the_game(self):
        start_time = time()
        print(self.game) 
        print('\n' + '#' * 20 + '\n') 
        curr_player = self.player1

        while(True):
            curr_player.update_game(self.game)
            
            cell, move = curr_player.make_move()
            self.print_player_type(curr_player)
            self.game.print_all_possible_moves(curr_player.player_type)
            self.game.make_move_on_board(cell[0], cell[1], move[0], move[1], True)
            print(self.game)   
            print_game_stats(self.game.moves_counter, start_time)
            print('\n' + '#' * 20 + '\n') 

            if self.game.has_player_won(curr_player.player_type):
                break
            curr_player = self.change_player(curr_player)
            sleep(self.move_ping)

        print("END GAME")
        print(f'{curr_player.player_type} has won!')        

    def change_player(self, curr_player):
       return self.player2 if curr_player.player_type == BLACK_PLAYER_CELL else self.player1
    
    def print_player_type(self, curr_player):
        print(f'Player\'s turn: {curr_player.player_type}\n')