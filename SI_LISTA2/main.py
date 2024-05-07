from HalmaBoard import HalmaBoard
from DecisionTree import DTree
from heuristic_functions import *
from distance_functions import euclidean_distance, manhattan_distance
from consts import WHITE_PLAYER_CELL, BLACK_PLAYER_CELL, BLACK_BASE_CONDITION_1, BLACK_BASE_CONDITION_2, MINIMAX, ALPHA_BETA
from ai_controller import AIsGameController, Player


def main():
    # x = HalmaBoard()
    # print(x)
    # x.print_all_possible_moves(BLACK_PLAYER_CELL)
    # print('-' * 20)
    # x.print_all_possible_moves(WHITE_PLAYER_CELL)


    # print(x.can_make_move(0,0,1,1))
    # print(x.can_make_move(0,4,1,1))
    # print(x.can_make_move(0,4,0,5))
    # print(x.can_make_move(0,4,-1,4))

    # print('-' * 20)

    # print(x.has_player_won(BLACK_PLAYER_CELL))
    # print(x.has_player_won(WHITE_PLAYER_CELL))

    # print('-' * 20)

    # # print(x.generate_all_possible_moves(0,0))
    # # print(x.generate_all_possible_moves(0,0))
    # print(x.generate_all_possible_moves(0,4))
    # print('-' * 20)
    # print(x.generate_all_possible_moves(3,1))

    # print('-' * 20)

    # print(x.find_the_longest_jump_seq(4, 0))

    # print('-' * 20)

    # print(distance_of_target_base(x, WHITE_PLAYER_CELL, euclidean_distance))
    # print('-' * 20)
    # print(control_of_the_board_centre(x, WHITE_PLAYER_CELL, euclidean_distance))


    # print('-' * 20)

    # x.board = [[0] * 16 for _ in range(16)]
    # x.board[0][:6] = [1,2,0,2,0,2]
    # x.board[1][:4] = [2,0,0,2]
    
    # print(distance_of_target_base(x, WHITE_PLAYER_CELL, manhattan_distance))

    # print('-' * 20)

    # x.board = [[0] * 16 for _ in range(16)]
    # x.board[0] = [2,2,0,1,0,2,0,1,0,2,0,1,0,2,0,0]
    # x.board[1] = [2,0,1,2,1,2,1,1,2,2,1,1,1,2,2,1]
    # print(x)

    # x.print_all_possible_moves(BLACK_PLAYER_CELL)
    # print('-' * 20)
    # x.print_all_possible_moves(WHITE_PLAYER_CELL)

    # print(x)
    # print(x.generate_all_possible_moves(0,0))
    # game = HalmaBoard()
    # game.board = [
    #     [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,2,2,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,2,2,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,2,2,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,2,0,0,2,0,0,0,2,0],
    #     [0,0,0,0,0,1,0,0,2,0,0,2,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,2,2,0,0,2,0,0,0],
    #     [0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,2,2,0,2,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
    # ]
    # dtree = DTree(game, BLACK_PLAYER_CELL, distance_of_target_base, euclidean_distance)

    # for child in dtree.root.children:
    #     print(child.game_state)
    #     print(child.get_rate(BLACK_PLAYER_CELL, distance_of_target_base, euclidean_distance))
    #     print('\n\n')
        
    # print('#' * 40)

    # print(dtree.minimax())


    # print(dtree.rate_current_game_state_alpha_beta())
    # print(dtree.rate_current_game_state_minimax())
    # print(dtree.root.children[0].children[3].game_state)
    # print(dtree.root.get_rate(WHITE_PLAYER_CELL, distance_of_target_base, manhattan_distance))
    # rate = distance_of_target_base(game, BLACK_PLAYER_CELL, euclidean_distance)
    # print(f'{rate}')
    # print('-' * 30)

    # game.board = [
    #     [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    #     [0,0,2,2,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,2,2,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,2,2,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,2,0,0,2,0,0,0,2,0],
    #     [0,0,0,0,0,1,0,0,2,0,0,2,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,2,2,0,0,2,0,0,0],
    #     [0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,2,2,0,2,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
    # ]

    # rate = distance_of_target_base(game, BLACK_PLAYER_CELL, manhattan_distance)
    # print(f'{rate}')
    # print('-' * 30)
    # node_index, rate = dtree.minimax()
    # print(f'{node_index}: {rate}')
    # print('-' * 30)
    # dtree.player_type = WHITE_PLAYER_CELL
    # node_index, rate = dtree.minimax()
    # print(f'{node_index}: {rate}')

    # print(dtree.root.children[node_index].game_state)
    # print(rate)
    # print(dtree.root.game_state)
    # print(distance_of_target_base(dtree.root.game_state, WHITE_PLAYER_CELL, manhattan_distance))

    # print('-' * 20)

    # child_tree = dtree.make_tree_from_child(node_index)
    # print(child_tree.root.game_state)

    # print('-' * 20)

    # node_index, rate = dtree.alpha_beta()
    # print(dtree.root.children[node_index].game_state)
    # print(rate)
 





    # p1 = Player(follow_as_close_to_the_diagonal, euclidean_distance, False, ALPHA_BETA)
    # p1 = Player(move_of_the_farthest_cell_as_far_as_possible, euclidean_distance, False, ALPHA_BETA)
    p1 = Player(random_rate_but_closer_to_base, euclidean_distance, False, ALPHA_BETA)
    # p2 = Player(follow_as_close_to_the_diagonal, manhattan_distance, False, ALPHA_BETA)
    # p2 = Player(random_rate_but_closer_to_base, manhattan_distance, False, ALPHA_BETA)

    new_game = HalmaBoard()
    # ai_controller = AIsGameController(new_game, p1, p2, 0)
    # ai_controller.start_the_game()
    p1.make_one_move(new_game.board, BLACK_PLAYER_CELL)








    # x = HalmaBoard()
    # x.board = [[0] * 16 for _ in range(16)]
    # x.board[11][13:] = [1,0,1]
    # x.board[12][13:] = [1,1,1]
    # x.board[13][12:] = [1,1,1,1]
    # x.board[14][11:] = [1,1,1,1,1]
    # x.board[15][11:] = [1,1,1,1,1]
    # print(x)
    # print(x.has_player_won(BLACK_PLAYER_CELL))
    
    # game = HalmaBoard()
    # dtree = DTree(game, BLACK_PLAYER_CELL, distance_of_target_base, euclidean_distance)

    # print(dtree.root.game_state)
    # print(dtree.root.children[0].game_state)
    # print(dtree.root.children[0].children[0].game_state)


if __name__ == '__main__':
    main()