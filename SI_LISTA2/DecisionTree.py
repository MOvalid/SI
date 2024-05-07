from consts import MAX_DTREE_DEPTH, BLACK_PLAYER_CELL, WHITE_PLAYER_CELL, MIN, MAX
from heuristic_functions import calculate_penalty_for_staying_in_base
from HalmaBoard import HalmaBoard
from copy import deepcopy
from utils import get_opponent_player_type
import random

class DTNode:

    def __init__(self, game, start_cell, end_cell):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.game_state = game
        if start_cell is not None:
            self.move = (end_cell[0] - start_cell[0], end_cell[1] - start_cell[1])
            self.game_state.make_move_on_board(start_cell[0], start_cell[1], self.end_cell[0], self.end_cell[1])

        self.rate = -1
        self.children = []

    def get_rate(self, player_type, heuristic_fn, distance_fn, base_penalty = True, reset = False):
        if reset or self.rate == -1:
            self.rate = heuristic_fn(self.game_state, player_type, distance_fn, self.start_cell, self.end_cell)
            if base_penalty: self.rate -= calculate_penalty_for_staying_in_base(self.game_state, player_type,distance_fn, self.start_cell, self.end_cell)
        return self.rate
    
    def add_child(self, new_child):
        self.children.append(new_child)
    


class DTree:

    def __init__(self, game, player_type, heuristic_fn, distance_fn, base_penalty = True, root = None):
        
        self.heuristic_fn = heuristic_fn
        self.distance_fn = distance_fn
        self.player_type = player_type
        self.base_penalty = base_penalty
        if root is None:
            self.root = DTNode(game, None, None)
            self.build_dtree(self.root, self.player_type, 1)
        else:
            self.root = root

    def get_full_move(self, child_index):
        return self.root.children[child_index].start_cell, self.root.children[child_index].end_cell

    def build_dtree(self, node, player_type, curr_depth):
        if curr_depth < MAX_DTREE_DEPTH:
            for cell in node.game_state.get_all_player_discs(player_type):
                for move in node.game_state.generate_all_possible_moves(cell[0], cell[1]):
                    # new_game = HalmaBoard()
                    # new_game.turn_player = (player_type % 2) + 1
                    # new_game.board = deepcopy(node.game_state.board)
                    # new_child = DTNode(new_game, cell, move)
                    new_child = self.generate_child(node, cell, move)
                    node.add_child(new_child)
                    self.build_dtree(new_child, get_opponent_player_type(player_type), curr_depth + 1)
            
    
    def minimax(self, init_depth = 1):
        # base case : targetDepth reached
        def inside_minimax(node, maxTurn, depth):
            if depth == MAX_DTREE_DEPTH:
                player_type = self.player_type if maxTurn else get_opponent_player_type(self.player_type)
                return (-1, node.get_rate(player_type, self.heuristic_fn, self.distance_fn))
            
            if (maxTurn):
                return max([(index, inside_minimax(child, not maxTurn, depth + 1)[1]) for index, child in enumerate(node.children)], key=lambda x: x[1])
            else:
                return min([(index, inside_minimax(child, not maxTurn, depth + 1)[1]) for index, child in enumerate(node.children)], key=lambda x: x[1])

        return inside_minimax(self.root, True, init_depth)
    
    def get_children(self, node, player_type):
        children = []
        for cell in node.game_state.get_all_player_discs(player_type):
            for move in node.game_state.generate_all_possible_moves(cell[0], cell[1]):
                children.append(self.generate_child(node, cell, move))
        return children

    # def minimax2(self, root_node, player_type, heuristic_fn, distance_fn, init_depth = 1):
    #     # base case : targetDepth reached
    #     def inside_minimax2(node, maxTurn, depth):

    #         curr_player_type = player_type if maxTurn else get_opponent_player_type(player_type)

    #         if depth == MAX_DTREE_DEPTH:
                
    #             return (node, get_rate(node, player_type, heuristic_fn, distance_fn))
            
    #         children = get_children(node, curr_player_type,)
            
    #         if (maxTurn):
    #             return max([(node, inside_minimax2(child, True, depth + 1)[1]) for child in children], key=lambda x: x[1])
    #         else:
    #             return min([(node, inside_minimax2(child, True, depth + 1)[1]) for child in children], key=lambda x: x[1])

    #     return inside_minimax2(root_node, True, init_depth)
    
    
    def alpha_beta(self, init_depth = 1):
        
        def inside_alpha_beta(node, maxTurn, depth, alpha, beta):
            # if node.children == []:
            if depth == MAX_DTREE_DEPTH:
                # player_type = get_opponent_player_type(self.player_type) if maxTurn else self.player_type
                player_type = get_opponent_player_type(self.player_type) if not maxTurn else self.player_type
               
                return (-1, node.get_rate(player_type, self.heuristic_fn, self.distance_fn))
            
            if (maxTurn):
                best = MIN
                node_index = 0
                for index, child in enumerate(node.children):
                    val = inside_alpha_beta(child, not maxTurn, depth + 1, alpha, beta)[1]

                    if val > best:
                        best = val
                        node_index = index
                    elif val == best:
                        if random.choice([0,1]) == 0:
                            best = val
                            node_index = index

                    alpha = max(alpha, best)

                    if beta <= alpha:
                        break

                return (node_index, best)
            
            else:
                best = MAX
                node_index = 0

                for index, child in enumerate(node.children):
                    val = inside_alpha_beta(child, not maxTurn, depth + 1, alpha, beta)[1]
                    # best = max(best, val)
                    if val < best:
                        best = val
                        node_index = index

                    elif val == best:
                        if random.choice([0,1]) == 0:
                            best = val
                            node_index = index

                    beta = max(beta, best)

                    if beta <= alpha:
                        break

                return (node_index, best)
            
        return inside_alpha_beta(self.root, True, init_depth, MIN, MAX)

    
    def generate_child(self, node, cell, move):
        new_game = HalmaBoard()
        new_game.turn_player = (node.game_state.turn_player % 2) + 1
        new_game.board = deepcopy(node.game_state.board)
        return DTNode(new_game, cell, move)
    
    def random_next_move(self):
        return random.randint(0, len(self.root.children)), -1
    

    def make_tree_from_child(self, child_index):
        child_tree = DTree(
            None, self.heuristic_fn, 
            self.distance_fn,
            self.root.children[child_index]
        )
        child_tree.extend_tree()
        return child_tree

    
    def extend_tree(self):
        def extend(node):
            if node.children != []:
                (extend(child) for child in node.children)
            else:
                for cell in node.game_state.get_all_player_discs(node.game_state.turn_player):
                    for move in node.game_state.generate_all_possible_moves(cell[0], cell[1]):
                        new_child = self.generate_child(node, cell, move)
                        node.add_child(new_child)

        extend(self.root)

    # def rate_current_game_state_minimax(self): 
    #     return self.minimax(MAX_DTREE_DEPTH - 1)

    # def rate_current_game_state_alpha_beta(self):
    #     return self.alpha_beta(MAX_DTREE_DEPTH - 1)

    def rate_current_game_state(self):
        return max([(index, child.get_rate(self.player_type, self.heuristic_fn, self.distance_fn)) for index, child in enumerate(self.root.children)], key=lambda x: x[1])
    
def rate_current_game_state2(node, player_type, heuristic_fn, distance_fn):
    return max([(child, child.get_rate(player_type, heuristic_fn, distance_fn)) for child in get_children(node, player_type)], key=lambda x: x[1])
    

def minimax2(root_node, player_type, heuristic_fn, distance_fn, init_depth = 1):
    # base case : targetDepth reached
    def inside_minimax2(node, maxTurn, depth):

        curr_player_type = player_type if maxTurn else get_opponent_player_type(player_type)

        if depth == MAX_DTREE_DEPTH:
            
            return (node, node.get_rate(player_type, heuristic_fn, distance_fn))
        
        children = get_children(node, curr_player_type)
        
        if (maxTurn):
            return max([(child, inside_minimax2(child, False, depth + 1)[1]) for child in children], key=lambda x: x[1])
        else:
            return min([(child, inside_minimax2(child, True, depth + 1)[1]) for child in children], key=lambda x: x[1])

    return inside_minimax2(root_node, True, init_depth)

def alpha_beta2(root_node, player_type, heuristic_fn, distance_fn, init_depth = 1):
    
    def inside_alpha_beta(node, maxTurn, depth, alpha, beta):
        # if node.children == []:

        curr_player_type = get_opponent_player_type(player_type) if not maxTurn else player_type
        
        if depth == MAX_DTREE_DEPTH:
            return (node, node.get_rate(player_type, heuristic_fn, distance_fn))
        
        children = get_children(node, curr_player_type)
        
        if (maxTurn):
            best = MIN
            best_node = None
            for child in children:
                val = inside_alpha_beta(child, not maxTurn, depth + 1, alpha, beta)[1]

                if val > best:
                    best = val
                    best_node = child
                elif val == best:
                    if random.choice([0,1]) == 0:
                        best = val
                        best_node = child

                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return (best_node, best)
        
        else:
            best = MAX
            best_node = None

            for child in children:
                val = inside_alpha_beta(child, not maxTurn, depth + 1, alpha, beta)[1]
                # best = max(best, val)
                if val < best:
                    best = val
                    best_node = child

                elif val == best:
                    if random.choice([0,1]) == 0:
                        best = val
                        best_node = child

                beta = max(beta, best)

                if beta <= alpha:
                    break

            return (best_node, best)
        
    return inside_alpha_beta(root_node, True, init_depth, MIN, MAX)

def get_children(node, player_type):
    children = []
    for cell in node.game_state.get_all_player_discs(player_type):
        for move in node.game_state.generate_all_possible_moves(cell[0], cell[1]):
            children.append(generate_child(node, cell, move))
    return children

def generate_child(node, cell, move):
    new_game = HalmaBoard()
    new_game.turn_player = (node.game_state.turn_player % 2) + 1
    new_game.board = deepcopy(node.game_state.board)
    return DTNode(new_game, cell, move)

