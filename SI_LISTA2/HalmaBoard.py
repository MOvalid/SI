from distance_functions import *
from utils import moves_to_str, print_matrix
from consts import *
from typing import Set
import random

class HalmaBoard:
    def __init__(self) -> None:
        self.board = self.prepare_board()
        self.turn_player = BLACK_PLAYER_CELL
        self.moves_counter = 0
    
    def __str__(self) -> str:
        result = '   |'

        for i in range(SIZE_OF_BOARD):
            result = result + ("{:02}".format(i) if i >= 10 else " {:1}".format(i)) + '|'

        for x in range(SIZE_OF_BOARD):
            result = result + "\n" + ("{:02}".format(x) if x >= 10 else " {:1}".format(x)) + ' | '
            for y in range(SIZE_OF_BOARD):
                # result = result + str(int(self.board[x][y].is_base_cell)) + ' '
                result = result + "{:1}".format(self.board[x][y]) + '  '
                
        return result + '\n'
    
    def pure_to_str(self):
        result = ''
        for x in range(SIZE_OF_BOARD):
            for y in range(SIZE_OF_BOARD):
                result += str(self.board[x][y]) + ' '
            result += '\n'
        return result

    def prepare_board(self):
        
        board = [[FREE_CELL for _ in range(SIZE_OF_BOARD)] for _ in range(SIZE_OF_BOARD)]
        
        for x in range(SIZE_OF_BOARD):
            for y in range(SIZE_OF_BOARD):
                if BLACK_BASE_CONDITION_1(x, y) and BLACK_BASE_CONDITION_2(x,y): board[x][y] = BLACK_PLAYER_CELL
                elif WHITE_BASE_CONDITION_1(x, y) and WHITE_BASE_CONDITION_2(x,y) : board[x][y] = WHITE_PLAYER_CELL

        return board
    
    def has_player_won(self, player_type):
        if player_type == WHITE_PLAYER_CELL:
            checking_range = range(0, 5)
            x_condition = BLACK_BASE_CONDITION_1
            x_y_condition = BLACK_BASE_CONDITION_2
        else:
            checking_range = range(11,16)
            x_condition = WHITE_BASE_CONDITION_1
            x_y_condition = WHITE_BASE_CONDITION_2

        for x in checking_range:
            for y in checking_range:
                if x_condition(x, y) and x_y_condition(x,y) and self.board[x][y] != player_type:
                    return False
        return True

        # while(x_condition(x, y)):
        #     while(x_condition(x,y) and x_y_condition(x,y)):
        #         if self.board[x][y] is not player_type:
        #             return False
        #         y = y + step
        #     x = x + step

        # return True;
            
    def make_move_on_board(self, x1, y1, x2, y2, to_print = False):
        player_type = self.board[x1][y1] 
        self.board[x1][y1] = FREE_CELL
        self.board[x2][y2] = player_type
        if to_print: self.print_move((x1, y1), (x2, y2))
        self.moves_counter += 1

    def can_make_move(self, x1, y1, x2, y2) -> bool:
        if x2 < 0 or y2 < 0 or x2 >= SIZE_OF_BOARD or y2 >= SIZE_OF_BOARD: return False

        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > 2 or abs(dy) > 2 : return False
        if abs(dx) + abs(dy) in [0,3]: return False

        if abs(dx) == 2 or abs(dy) == 2:
            # print(f'x1 = {x1}')
            # print(f'y1 = {y1}')
            # print(f'x2 = {x2}')
            # print(f'y2 = {y2}')

            # print(x2 + int(dx/2))
            return self.board[x2][y2] == FREE_CELL and \
               self.board[x1 + int(dx/2)][y1 + int(dy/2)] != FREE_CELL
        
        if abs(dx) + abs(dy) in [0,3]: return False

        return self.board[x2][y2] == FREE_CELL
    
    # def generate_moves_set(self, player_type):
    #     result = dict()
    #     for x in range(SIZE_OF_BOARD):
    #         for y in range(SIZE_OF_BOARD):
    #             if self.board[x][y] == player_type:
    #                 result[(x, y)] = self.generate_all_possible_moves(x, y) 

    #     return result
    
    def get_all_player_discs(self, player_type):
        discs = [(x, y) for x in range(SIZE_OF_BOARD) for y in range(SIZE_OF_BOARD) if self.board[x][y] == player_type]
        random.shuffle(discs)
        return discs
    
    def generate_all_possible_moves(self, x, y, can_move = True, visited_cells = None):
        # print(f'x = {x}, y = {y}')
        # print(visited_cells)
    
        if visited_cells is None: visited_cells = []
        if (can_move):
            for dx in MOVE_POSSIBILITIES:
                for dy in MOVE_POSSIBILITIES:
                    if self.can_make_move(x, y, x + dx, y + dy):
                    #  print((x + dx, y + dy))
                     visited_cells.append((x + dx, y + dy))
        for dx in JUMP_POSSIBILITIES:
            for dy in JUMP_POSSIBILITIES:
                if (x + dx, y + dy) not in visited_cells \
                and self.can_make_move(x, y, x + dx, y + dy):
                    visited_cells.append((x + dx, y + dy))
                    # print((x + dx, y + dy))
                    visited_cells = self.generate_all_possible_moves(x + dx, y + dy, False, visited_cells)
        random.shuffle(visited_cells)
        return visited_cells
    
    def generate_all_possible_moves_for_all_discs(self, player_type):
        all_cells = self.get_all_player_discs(player_type)
        return {
            cell: self.generate_all_possible_moves(cell[0], cell[1])
            for cell in all_cells
        }
    
    def print_move(self, start_cell, end_cell):
        print(f'{start_cell} ---> {end_cell}\n')
    
    def find_the_longest_jump_seq(self, x, y, path = []):
        # print(f'x = {x} y = {y}')
        possible_jumps = [[]]
        for dx in JUMP_POSSIBILITIES:
            for dy in JUMP_POSSIBILITIES:
                if (x + dx, y + dy) not in path and self.can_make_move(x, y, x + dx, y + dy):
                    possible_jumps.append(self.find_the_longest_jump_seq(x + dx, y + dy, path + [(x + dx, y + dy)]))
        possible_jumps.append(path)
        return max(possible_jumps, key=len)
    
    def get_random_move(self, player_type):
         all_discs = self.get_all_player_discs(player_type)
         while(True):
            random_cell = random.choice(all_discs)
            possibles_moves = self.generate_all_possible_moves(
                    random_cell[0],
                    random_cell[1]
                )
            
            if len(possibles_moves) != 0:
                break

         random_move = random.choice(possibles_moves)
         return random_cell, random_move
    
    def make_random_move(self, player_type):
        random_cell, random_move = self.get_random_move(player_type)
        self.make_move_on_board(
            random_cell[0],
            random_cell[1],
            random_move[0],
            random_move[1], True
        )

    def is_cell_movable(self, cell):
        return self.generate_all_possible_moves(cell[0], cell[1]) != []
    
    def print_all_possible_moves(self, player_type):
        possible_moves = self.generate_all_possible_moves_for_all_discs(player_type)
        number_of_all_moves = sum(len(moves) for moves in possible_moves.values())
        print(f"There is {number_of_all_moves} possible moves.")
        for cell, moves in possible_moves.items():
            if moves == []:
                print(f'{cell}: No possible moves')
            else:
                print(f'{cell}: {moves_to_str(moves)}')
        print('\n')

    def is_disc_in_home_base(self, player_type, disc):
        x, y = disc
        if self.board[x][y] != player_type: return False

        cond1, cond2 = WHITE_BASE_CONDITION_1, WHITE_BASE_CONDITION_2 if player_type == WHITE_PLAYER_CELL else BLACK_BASE_CONDITION_1, BLACK_BASE_CONDITION_2

        return cond1(x,y) and cond2(x,y)

            

def main():
    x = HalmaBoard()
    print(x.pure_to_str())

    print_matrix(ENDGAME_RATING_TABLE_WHITE)
    print('\n' + '*' * 20 + '\n')
    print_matrix(ENDGAME_RATING_TABLE_BLACK)

if __name__ == '__main__':
    main()

