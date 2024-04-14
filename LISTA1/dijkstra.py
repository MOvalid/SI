import heapq
from graph import convert_hour
from cost_functions import get_time_cost
from utils import create_path

def dijkstra(graph_dict, start):
    distances = {node: float('inf') for node in graph_dict.keys()}
    distances[start] = 0
    pq = [(0, start)]
    prev_nodes = {node: None for node in graph_dict}
    while pq:

        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        if not curr_node in graph_dict:
            continue
        for edge in graph_dict[curr_node]:
            neighbor = edge.end_station
            weight = edge.weight
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev_nodes[neighbor] = curr_node
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, prev_nodes

def dijkstra_with_time(graph, start_station, goal_station, start_time):
    costs = {node: float('inf') for node in graph.graph_dict}
    edges = {node: None for node in graph.graph_dict}
    costs[start_station] = 0
    pq = [(0, start_station, convert_hour(start_time))]
    prev_nodes = {node: None for node in graph.graph_dict}
    while pq:
        current_cost, current_station, current_time = heapq.heappop(pq)
        
        if current_cost > costs[current_station]:
            continue
        if not current_station in graph.graph_dict:
            continue

        for edge in graph.get_all_edges(current_station):
            neighbor = edge.end_station
            current_line = None if edges[current_station] is None else edges[current_station].line
            new_cost = current_cost + get_time_cost(current_time, current_line, edge)

            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                edges[neighbor] = edge
                prev_nodes[neighbor] = current_station
                heapq.heappush(pq, (new_cost, neighbor, edge.end_time))

    return costs[goal_station], create_path(goal_station, edges, prev_nodes)





