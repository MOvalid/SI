import math
from graph import *
from typing import Callable
from utils import DEGREES_TO_KILOMETERS_CONVERTER, AVERAGE_VELOCITY_IN_WROCLAW, has_direct_connection
from cost_functions import TIME_DELTA





def manhattan_distance(a, b):
    return sum([abs(x - y) for x, y in zip(a, b)])

def euclidean_distance_stations(a: Station, b: Station) -> float:
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def manhattan_distance_stations(a: Station, b: Station) -> float:
    return abs(b.x - a.x) + abs(b.y - a.y)

def distance_heuristic_fn(
        a: Station,
        b: Station,
        distance_fn: Callable[[Station, Station], float]) -> float:
    return distance_fn(a, b) * DEGREES_TO_KILOMETERS_CONVERTER / AVERAGE_VELOCITY_IN_WROCLAW # t = s/v



def transfer_heuristic_fn(
        curr_station: Station,
        goal_station: Station,
        has_changed_line: bool,
        graph: Graph,
        time: int,
        distance_fn: Callable[[Station, Station], float],
        number_of_changes: int,
        curr_edge: Edge
    ) -> float:
    
    if has_direct_connection(curr_edge, goal_station, graph, time, TIME_DELTA) and has_changed_line:
        return float('inf')
    
    if number_of_changes == 0:
        return distance_fn(curr_station, goal_station) * DEGREES_TO_KILOMETERS_CONVERTER / AVERAGE_VELOCITY_IN_WROCLAW
    elif number_of_changes == 1:
        return distance_fn(curr_station, goal_station) * DEGREES_TO_KILOMETERS_CONVERTER / AVERAGE_VELOCITY_IN_WROCLAW * 2.25

    return distance_fn(curr_station, goal_station) * DEGREES_TO_KILOMETERS_CONVERTER / AVERAGE_VELOCITY_IN_WROCLAW  * (number_of_changes ** 2)


def euclidean_distance(a, b):
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)]))


def towncenter_distance(a, b):
    return euclidean_distance(a, (0, 0, 0, 0, 0, 0, 0)) + euclidean_distance((0, 0, 0, 0, 0, 0, 0), b)


def unidimensional_distance(a, b):
    return max([abs(x - y) for x, y in zip(a, b)])


def cosine_distance(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(x ** 2 for x in b))
    return 1 - (dot_product / (magnitude_a * magnitude_b))


def chebyshev_distance(a, b):
    return max(abs(x - y) for x, y in zip(a, b))
