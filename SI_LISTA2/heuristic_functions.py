from consts import *
import random


def mobility_of_discs(game, player_type, *_):
    return sum(
        len(game.generate_all_possible_moves(x, y)) 
        for x in range(SIZE_OF_BOARD)
        for y in range (SIZE_OF_BOARD)
        if game.board[x][y] == player_type
    )

def random_rate(*_):
    return random.randrange(0, 100_000)

def follow_as_close_to_the_diagonal(game, player_type, distance_fn, start_cell, end_cell):
    score = 0
    x1, y1 = start_cell
    score += 0 if game.is_disc_in_home_base(player_type, start_cell) else 100 - abs(x1 - y1) * 10
    x2, y2 = end_cell 
    score += 100 - abs(x2 - y2) * 10
    score += distance_fn(start_cell, end_cell)
    return score + distance_of_target_base(game, player_type, distance_fn, start_cell, end_cell)# czy coś jeszcze????

def random_rate_but_closer_to_base(_, player_type, distance_fn, start_cell, end_cell):
    target_cells = WHITE_TARGET_CELLS if player_type == WHITE_PLAYER_CELL else BLACK_TARGET_CELLS
    x, y = start_cell
    start_cell_min = min(distance_fn((x, y), target_cell) for target_cell in target_cells)
    x, y = end_cell
    end_cell_min = min(distance_fn((x, y), target_cell) for target_cell in target_cells)
    distance_diff = start_cell_min - end_cell_min
    return -1 * float(('inf')) if distance_diff < 0 else random.randrange(0, 100_000)

def move_of_the_farthest_cell_as_far_as_possible(_, player_type, distance_fn, start_cell, end_cell):
    target_cell = BLACK_TARGET_CELL if player_type == BLACK_PLAYER_CELL else WHITE_TARGET_CELL
    return distance_fn(start_cell[0], start_cell[1], target_cell[0], target_cell[1]) + distance_fn(start_cell[0], start_cell[1], end_cell[0], end_cell[1])
    

def distance_of_target_base(game, player_type, distance_fn, *_):
    if player_type == WHITE_PLAYER_CELL:
        target_cells = WHITE_TARGET_CELLS
        x_condition = BLACK_BASE_CONDITION_1
        x_y_condition = BLACK_BASE_CONDITION_2
    else:
        target_cells = BLACK_TARGET_CELLS
        x_condition = WHITE_BASE_CONDITION_1
        x_y_condition = WHITE_BASE_CONDITION_2


    return -1 * get_distance_score(
        game, player_type,
        x_condition, x_y_condition,
        target_cells, distance_fn
    )

def get_distance_score(game, player_type, x_condition, x_y_condition, target_cells, distance_fn):
    score = 0
    # print(target_cells)
    # print(player_type)
    for x in range(SIZE_OF_BOARD):
        for y in range(SIZE_OF_BOARD):
            if game.board[x][y] == player_type and (not x_condition(x, y)) and (not x_y_condition(x, y)):
                _min = min(distance_fn((x, y), target_cell) for target_cell in target_cells)
                # print(_min)
                score += _min
                # print(score)
    return score


def control_of_the_board_centre(game, player_type, distance_fn, *_):
    if player_type ==  WHITE_PLAYER_CELL:
        x_condition = BLACK_BASE_CONDITION_1
        x_y_condition = BLACK_BASE_CONDITION_2
    else:
        x_condition = WHITE_BASE_CONDITION_1
        x_y_condition = WHITE_BASE_CONDITION_2
    return -1 * get_distance_score(
        game, player_type,
        x_condition, x_y_condition,
        CENTER_CELLS, distance_fn
    )

def try_to_master_the_base(game, player_type, *_):
    # if player_type == WHITE_PLAYER_CELL:
    #     checking_range = range(0,8)
        # shift = 0
    # else:
    #     checking_range = range(8,16)
        # shift = 8
    # score = 0
    # for x in checking_range:
    #     for y in checking_range:
    #         if game.board[x][y] == player_type:
    #             score += ENDGAME_RATING_TABLE[x - shift][y - shift]

    # return score
    endgame_rating_table = ENDGAME_RATING_TABLE_WHITE if player_type == WHITE_PLAYER_CELL else ENDGAME_RATING_TABLE_BLACK
    all_discs = game.get_all_player_discs(player_type)

    score = 0
    for disc in all_discs:
        x,y = disc[0], disc[1]
        score += endgame_rating_table[x][y]
    return score

def calculate_penalty_for_staying_in_base(game, player_type, distance_fn, start_cell, end_cell):
    base_cells = WHITE_PLAYER_BASE_CELLS if player_type == WHITE_PLAYER_CELL else BLACK_PLAYER_BASE_CELLS
    rating_table = ENDGAME_RATING_TABLE_WHITE if player_type == BLACK_PLAYER_CELL else ENDGAME_RATING_TABLE_BLACK
    penalty = 0
    is_start_cell_in_base, is_end_cell_in_base =  False, False
    for (x,y) in base_cells:
        if game.board[x][y] == player_type:
            penalty += rating_table[x][y]
        if (x,y) == start_cell:
            is_start_cell_in_base = True
        elif (x,y) == end_cell:
            is_end_cell_in_base = True

    if is_start_cell_in_base and not is_end_cell_in_base:
        penalty -= 100

    if not is_start_cell_in_base and is_end_cell_in_base:
        penalty += 1000

    return penalty
    