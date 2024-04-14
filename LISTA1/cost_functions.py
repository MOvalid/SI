from utils import time_diff, has_direct_connection

MPK_TRANSFER_COST = 100
TIME_DELTA = 15
MAX_NO_TRANSFER_TIME_DELTA = 2

def get_time_cost(curr_time, curr_line, new_edge):
    
    cost = float('inf') if curr_time - new_edge.start_time < 0 else curr_time - new_edge.end_time

    if (curr_line != None and curr_line != new_edge.line and curr_time <= new_edge.start_time):
        cost = float('inf')
    
    return cost


def get_transfer_cost(new_edge, current_line, current_time, goal_station, graph):
    if current_line == None:
        if time_diff(current_time, new_edge.start_time) < 0:
            cost = float('inf')
        elif time_diff(current_time, new_edge.start_time) > TIME_DELTA:
            cost = float('inf')
        elif has_direct_connection(new_edge, goal_station, graph, current_time, TIME_DELTA):
            cost = 0
        else:
            cost = MPK_TRANSFER_COST
    elif current_line != new_edge.line:
        if time_diff(current_time - 1, new_edge.start_time) < 0:
            cost = float('inf')
        elif time_diff(current_time - 1, new_edge.start_time) > TIME_DELTA:
            cost = float('inf')
        else:
            cost = 1
    elif time_diff(current_time, new_edge.start_time) >= 0 and time_diff(current_time, new_edge.start_time) <= MAX_NO_TRANSFER_TIME_DELTA:
        cost = 0
    else:
        cost = MPK_TRANSFER_COST
    return cost

