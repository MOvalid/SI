from utils import reverse_matrix

SIZE_OF_BOARD = 16
NUMBER_OF_PLAYER_DISCS = 19
FREE_CELL = 0
BLACK_PLAYER_CELL = 1
WHITE_PLAYER_CELL = 2

BLACK_BASE_CONDITION_1 = lambda x, y : x < 5 and y < 5
BLACK_BASE_CONDITION_2 = lambda x, y : x + y < 6

WHITE_BASE_CONDITION_1 = lambda x, y: x > 10 and y > 10
WHITE_BASE_CONDITION_2 = lambda x, y : x + y > 24

JUMP_POSSIBILITIES = [-2, 0, 2]
MOVE_POSSIBILITIES = range(-1, 2)


BLACK_TARGET_CELL = (15,15)
WHITE_TARGET_CELL = (0,0)

BLACK_TARGET_CELLS = [BLACK_TARGET_CELL ]
WHITE_TARGET_CELLS = [WHITE_TARGET_CELL]




CENTER_CELLS = [(x, y) for x in range(7, 9) for y in range(7, 9)]

MAX_DTREE_DEPTH = 3

MAX = float('inf')
MIN = -1 * float('inf')

AI_CELL_TYPE = BLACK_PLAYER_CELL
USER_CELL_TYPE = WHITE_PLAYER_CELL

MINIMAX = 101
ALPHA_BETA = 102

ENDGAME_RATING_TABLE_WHITE =  [[-100 for _ in range(SIZE_OF_BOARD)] for _ in range(SIZE_OF_BOARD)]
        
ENDGAME_RATING_TABLE_WHITE[0][:8] = [100, 75, 50, 25, 10, 0, -5, -10]
ENDGAME_RATING_TABLE_WHITE[1][:8] = [75, 75, 50, 25, 10, 0, -5, -10]
ENDGAME_RATING_TABLE_WHITE[2][:8] = [50, 50, 50, 10, 0, -5, -10, -15]
ENDGAME_RATING_TABLE_WHITE[3][:8] = [25, 25, 10, 0, -5, -10, -15, -20]
ENDGAME_RATING_TABLE_WHITE[4][:8] = [10, 10, 0, -5, -10, -15, -20, -25]
ENDGAME_RATING_TABLE_WHITE[5][:8] = [0, 0, -5, -10, -15, -20, -25, -30]
ENDGAME_RATING_TABLE_WHITE[6][:8] = [-5, -5, -10, -15, -20, -25, -30, -35]
ENDGAME_RATING_TABLE_WHITE[7][:8] = [-10, -10, -15, -20, -25, -30, -35, -40]

ENDGAME_RATING_TABLE_BLACK =  reverse_matrix(ENDGAME_RATING_TABLE_WHITE)


WHITE_PLAYER_BASE_CELLS = [
    (11,15), (12,15), (13,15), (14,15), (15,15),
    (11,14), (12,14), (13,14), (14,14), (15,14),
    (12,13), (13,13), (14,13), (15,13),
    (13,12), (14,12), (15,12),
    (14,11), (15,11)
]

BLACK_PLAYER_BASE_CELLS = [
    (0,0), (1,0), (2,0), (3,0), (4,0),
    (0,1), (1,1), (2,1), (3,1), (4,1),
    (0,2), (1,2), (2,2), (3,2), 
    (0,3), (1,3), (2,3),
    (0,4), (1,4)
]


DIAGONAL_RATING_TABLE_WHITE = [[0 for _ in range(SIZE_OF_BOARD)] for _ in range(SIZE_OF_BOARD)]