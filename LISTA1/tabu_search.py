import random
import math
from utils import convert_minutes_to_hourtime
from heuristic_functions import manhattan_distance_stations
from astar import astar_time

MAX_ITERATIONS = 10
STATION_NAME_MAX_LENGTH = 40
LINE_MAX_LENGTH = 5
EDGE_TIME_MAX_LENGTH = 8


def tabu_search(start_station, stations_to_visit, start_time, graph, to_print: bool = False, heuristic_fn = manhattan_distance_stations):
    aspiration_criteria = 100
    if start_station == None or stations_to_visit == []:
        return
    turns_improved = 0
    improve_thresh = 2 * math.floor(math.sqrt(MAX_ITERATIONS))
    tabu_list = []
    tabu_tenure = len(stations_to_visit)
    current_solution = [start_station] + stations_to_visit + [start_station]
    best_solution = current_solution[:]
    best_solution_cost, best_solution_edges = get_solution_cost(best_solution, start_time, graph, heuristic_fn)

    for iteration in range(MAX_ITERATIONS):
        if turns_improved > improve_thresh:
            break
        best_neighbor = None
        best_neighbor_cost = float('inf')
        best_neighbor_edges = []
        tabu_candidate = (0,0)
        for i in range(1, len(stations_to_visit) + 1):
            for j in range(i+1, len(stations_to_visit) + 1):
                neighbor = current_solution[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbor_cost, neighbor_edges = get_solution_cost(neighbor, start_time, graph, heuristic_fn)
                if (i,j) not in tabu_list or neighbor_cost < aspiration_criteria:
                    if neighbor_cost < best_neighbor_cost:
                        best_neighbor = neighbor[:]
                        best_neighbor_cost = neighbor_cost
                        best_neighbor_edges = neighbor_edges
                        tabu_candidate = (i,j)
        if best_neighbor is not None:
            current_solution = best_neighbor[:]
            tabu_list.append(tabu_candidate)

            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)

            if best_neighbor_cost < best_solution_cost:
                best_solution = best_neighbor[:]
                best_solution_cost = best_neighbor_cost
                best_solution_edges = best_neighbor_edges
                turns_improved = 0
            else:
                turns_improved = turns_improved + 1

        if to_print: print("Iteration {}: Best solution cost = {}".format(iteration, best_solution_cost))

    if to_print:
        print_best_solution(best_solution)
        print(f"Best solution cost: {best_solution_cost} minutes")
        print(f"Start time: {start_time}")
        print_formatted_edges(start_station, best_solution_edges)

    return best_neighbor_cost, best_solution, best_neighbor_edges

def print_best_solution(best_solution):
    print("Best solution: [", end='')
    for station in best_solution[:-1]:
        print(f'{station.name} - ',  end='')
    print(f'{best_solution[-1].name}]')

def print_formatted_edges(start_station, edges):
    last_line = None
    last_station = start_station
    for edge in edges:
        if edge.line != last_line: print_line_tabu_2(last_station, edge, last_station != start_station)
        print_line_tabu_1(edge)
        last_line, last_station = edge.line, edge.end_station
    print('-' * 50)

def print_line_tabu_1(edge):
    print(f'{edge.end_station.name.ljust(STATION_NAME_MAX_LENGTH)} | {edge.line.ljust(LINE_MAX_LENGTH)} | {convert_minutes_to_hourtime(edge.end_time).ljust(EDGE_TIME_MAX_LENGTH)}')

def print_line_tabu_2(station, edge, print_line=True):
    print('-' * 50)
    if print_line:
        print(f'{station.name.ljust(STATION_NAME_MAX_LENGTH)} | {edge.line.ljust(LINE_MAX_LENGTH)} | {convert_minutes_to_hourtime(edge.start_time).ljust(EDGE_TIME_MAX_LENGTH)}')
    else:
        print(f'{station.name.ljust(STATION_NAME_MAX_LENGTH)} | {" ".ljust(LINE_MAX_LENGTH)} | {convert_minutes_to_hourtime(edge.start_time).ljust(EDGE_TIME_MAX_LENGTH)}')

def get_solution_cost(solution, start_time, graph, heuristic_fn):
    fitness = 0;
    current_time = start_time
    last_line = None
    edges = []

    for i in range(len(solution) - 1):
        current_cost, path = astar_time(graph, solution[i], solution[i+1], current_time, heuristic_fn)
        edges = edges + path[1:]
        fitness = fitness + current_cost
        if path != []: current_last_edge = path[-1]
        current_last_edge = path[-1] if path != [] else None 
        if current_last_edge is not None: 
            extra_change_time = int(last_line != current_last_edge.line)
            current_time = convert_minutes_to_hourtime(current_last_edge.end_time - extra_change_time)
            fitness = fitness + extra_change_time
        if current_last_edge: last_line = current_last_edge.line
        else: last_line = None

    return fitness - 1, edges

