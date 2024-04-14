import heapq

from graph import *
from utils import *
from cost_functions import *
from heuristic_functions import *



def astar(start, goal, neighbors_fn, heuristic_fn):
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while front:
        _, current = heapq.heappop(front)

        if current == goal:
            break

        for neighbor in neighbors_fn(current):
            new_cost = cost_so_far[current]
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic_fn(goal, neighbor)
                heapq.heappush(front, (priority, neighbor))
                came_from[neighbor] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, cost_so_far[goal]



def astar_time(graph, start_station, goal_station, start_time, heuristic_fn):
    costs = {node: float('inf') for node in graph.graph_dict}
    edges = {node: None for node in graph.graph_dict}
    costs[start_station] = 0
    pq = [(0, start_station)]
    prev_nodes = {node: None for node in graph.graph_dict}
    while pq:
        _, current_station = heapq.heappop(pq)
        
        if current_station == goal_station:
            break

        if not current_station in graph.graph_dict:
            continue
        
        current_time = convert_hour(start_time) if edges[current_station] is None else edges[current_station].end_time
        current_line = None if edges[current_station] is None else edges[current_station].line

        for edge in graph.get_all_edges(current_station):
            
            neighbor = edge.end_station
        
            new_cost = costs[current_station] + get_time_cost(current_time, current_line, edge)

            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                edges[neighbor] = edge
                prev_nodes[neighbor] = current_station
                new_cost = new_cost + distance_heuristic_fn(
                    goal_station,
                    neighbor,
                    heuristic_fn
                )
                heapq.heappush(pq, (new_cost, neighbor))

    the_best_cost = costs[goal_station]

    # Searching for the nearest stop to an unavailable stop
    if the_best_cost == float('inf'):
        min_distances = get_sorted_min_distances(goal_station, edges)
        for station, distance in min_distances.items():
            if costs[station] != float('inf'):
                edges[goal_station] = prepare_P_line_edge(start_station, goal_station, edges[station], distance)
                prev_nodes[goal_station] = station
                the_best_cost = convert_hour(start_time) - edges[goal_station].end_time
                break


    return the_best_cost, create_path(goal_station, edges, prev_nodes)



def astar_transfers(graph, start_station, goal_station, start_time, heuristic_fn):

    costs = {start_station: 0}
    edges = {node: None for node in graph.graph_dict}
    pq = [(0, start_station, convert_hour(start_time))]
    prev_nodes = {node: None for node in graph.graph_dict}
    while pq:
        _, current_station, current_time = heapq.heappop(pq)
        
        if current_station == goal_station:
            break

        if not current_station in graph.graph_dict:
            continue
      
        current_line = None if edges[current_station] is None else edges[current_station].line

        for edge in graph.get_all_edges(current_station):
            neighbor = edge.end_station

            cost = get_transfer_cost(edge, current_line, current_time, goal_station, graph)
            new_cost = costs[current_station] + cost

            if neighbor not in costs or new_cost < costs[neighbor]:

                costs[neighbor] = new_cost
                edges[neighbor] = edge
                prev_nodes[neighbor] = current_station
                priority = new_cost + transfer_heuristic_fn(
                    neighbor,
                    goal_station,
                    cost > 0,
                    graph,
                    current_time,
                    heuristic_fn,
                    new_cost,
                    edge
                )
                
                heapq.heappush(pq, (priority, neighbor, edge.end_time))

    return costs[goal_station], create_path(goal_station, edges, prev_nodes)

