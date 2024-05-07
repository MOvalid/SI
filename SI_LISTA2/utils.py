from time import time
import copy, sys

def get_opponent_player_type(player_type):
    return (player_type % 2) + 1

def print_game_stats(moves_counter, start_time):
    print(f'Number of moves made: {moves_counter}')
    game_time = time() - start_time
    print(f'Game time: {convert_time(game_time)}')
    
def convert_time(seconds_float):
    seconds = int(seconds_float)
    milliseconds = int((seconds_float - seconds) * 1000)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    return '{:02d}:{:02d}:{:02d}.{:03d}'.format(hours, minutes, seconds, milliseconds)

def moves_to_str(moves):
    result = ''
    for move in moves:
        result += str(move) + ', '
    return result[:-2]

def reverse_matrix(matrix):
    m = copy.deepcopy(matrix)
    for row in m:
        row.reverse()
    reversed_matrix = m[::-1]
    return reversed_matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

def read_output():
    for line in sys.stdin:
        if line.startswith("Choose disc to move:"):
            print("15,11")



def test():
    board = [[100 - abs(x-y) * 10 for x in range(16)] for y in range(16)]
    print_matrix(board)


# test()
# print(test.__name__)

