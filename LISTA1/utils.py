
import math, random
import graph

DEGREES_TO_KILOMETERS_CONVERTER = 111
AVERAGE_VELOCITY_IN_WROCLAW = 20.3 # km/h
AVERAGE_WALKING_SPEED_OF_PEDESTRIANS = 4 # km/h

NO_TIME_DELTA = float('inf')
MINUTES_IN_DAY = 1440
MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24
HOUR_FORMAT = "%H:%M:%S"

def convert_minutes_to_hourtime(time: int) -> str:
    if time is None:
        return 'XX:XX:XX'
    
    if time > 0:
        if time % MINUTES_IN_HOUR == 0:
            hour = HOURS_IN_DAY - int(time / MINUTES_IN_HOUR)
            minutes = 0
        else:
            hour = (HOURS_IN_DAY - 1) - int(time / MINUTES_IN_HOUR)  
            minutes = MINUTES_IN_HOUR - (time % MINUTES_IN_HOUR)
    else:
        time = time * -1
        hour = int(time / MINUTES_IN_HOUR)
        minutes = time % MINUTES_IN_HOUR
    return f'{str(hour).zfill(2)}:{str(minutes).zfill(2)}:00'


def time_diff(start_time, end_time) -> float:
    if start_time < 0 and end_time > 0:
        dt = start_time - end_time + MINUTES_IN_DAY
    else:
        dt = start_time - end_time
    return float('inf') if dt < 0 else dt



def prepare_P_line_edge(start_station, goal_station, last_edge, min_distance):
    new_start_time = last_edge.end_time
    new_end_time = new_start_time - math.ceil(min_distance * DEGREES_TO_KILOMETERS_CONVERTER / AVERAGE_WALKING_SPEED_OF_PEDESTRIANS)
    edge  = graph.Edge(start_station, goal_station, 'P')
    edge.start_time = new_start_time
    edge.end_time = new_end_time
    edge.weight = new_start_time - new_end_time
    return edge


def has_fewer_changes(previous, new, goal) -> bool:
    previous_came_from, previous_edges = previous
    new_came_from, new_edges = new
    previous_counter = get_number_of_changes(previous_came_from, previous_edges, goal)
    new_counter = get_number_of_changes(new_came_from, new_edges, goal)

    return new_counter < previous_counter


def get_number_of_changes(came_from, edges, goal):
    counter = 0
    if goal not in edges: return float('inf')
    last_edge = edges[goal]
    current = goal
    while edges[came_from[current]] is not None:
        if last_edge.line != edges[came_from[current]].line:
            counter = counter + 1
        last_edge = edges[came_from[current]]
        current = came_from[current]
    return counter

def euclidean_distance_stations(station1, station2) -> float:
    return math.sqrt((station2.x - station1.x) ** 2 + (station2.y - station1.y) ** 2)
    

def get_sorted_min_distances(goal, edges):
    min_distances = {station: euclidean_distance_stations(station, goal) for station in edges}
    return dict(sorted(min_distances.items(), key=lambda x : x[1]))

def has_direct_connection(edge, goal_station, graph, start_time: int = 720, time_delta: int = NO_TIME_DELTA):
    return any(
       edge.line == goal_edge.line for goal_edge in graph.get_all_edges(goal_station) if not time_diff(start_time, edge.start_time) > time_delta
    )

def convert_hour(time: str) -> int:
    return MINUTES_IN_DAY - (int(time[:2]) * MINUTES_IN_HOUR + int(time[3:5]))

def create_path(goal, edges, came_from):
    path = []
    current = goal
    while current is not None:
        path.append(edges[current])
        current = came_from[current]

    path.reverse()
    return path[1:]

def shuffle_array_except_first_last(arr):
    if len(arr) <= 3:
        return arr
    middle_part = []
    [middle_part.append(x) for x in arr[1:-1] if x not in middle_part]
    random.shuffle(middle_part)
    return [arr[0]] + middle_part + [arr[-1]]

