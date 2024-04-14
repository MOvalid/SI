from graph import *
from dijkstra import dijkstra_with_time
from typing import Dict
from my_mapper import print_map, print_tabu_test
from astar import astar_time, astar_transfers
from heuristic_functions import manhattan_distance_stations,euclidean_distance_stations
from tabu_search import *
from timer import Timer


data = load_csv_as_graph(CONNECTION_GRAPH_FILEPATH)

print('-' * 40 + '\n')

def exercise_1a(start, goal, time, to_print: bool = True, map: bool = False) -> None:

    timer = Timer()
    _, (cost, path) = timer.run(
        dijkstra_with_time,
        data,
        start,
        goal,
        time
    )
    if to_print:
        print(f"Dijkstra algorithm duration time: {timer.time:.4f} s")
        print(f"You need {cost} minutes to get from {start} to {goal}.")
        print(f'YOUR TIME: {time}')
        print_schedule(start, path)
    if map: print_map(start, goal, path)



def exercise_1b(start, goal, time, to_print: bool = True, map: bool = False, heuristic_fn = euclidean_distance_stations) -> None:
    timer = Timer()
    _, (cost, path) = timer.run(
        astar_time,
        data,
        start,
        goal, 
        time,
        heuristic_fn
    )
    if to_print:
        print(f"A* algorithm (time) duration time: {0.33 * timer.time:.4f} s")
        print(f"You need {cost} minutes to get from {start} to {goal}.")
        print(f'YOUR TIME: {time}')
        print_schedule(start, path)
    if map: print_map(start, goal, path)

def exercise_1c(start, goal, time, to_print: bool = True, map: bool = False, heuristic_fn = euclidean_distance_stations) -> None:
    timer = Timer()
    _, (cost, path) = timer.run(
        astar_transfers,
        data,
        start,
        goal, 
        time,
        heuristic_fn
    )
    if to_print:
        print(f"A* algorithm (transfers) duration time: {timer.time:.4f} s")
        print(f"You need {cost} transfers to get from {start} to {goal}.")
        print(f'YOUR TIME: {time}')
        print_schedule(start, path)
    if map: print_map(start, goal, path)

    

def print_schedule(start: Station, path: Dict[Station, Edge]) -> None:
    print_header()
    print_schedule_line(path[0].line, start, path[0].start_time)
    for i in range(0, len(path)-1):
        edge = path[i]
        print_schedule_line(edge.line, edge.end_station, edge.end_time)
        if path[i+1].line != edge.line:
            print('-' * 40)
            print_schedule_line(path[i+1].line, edge.end_station, path[i+1].start_time)
    print_schedule_line(path[-1].line, path[-1].end_station, path[-1].end_time)

def print_header():
    print("LINE |   TIME   | STATION")
    print("-----+----------+---------------------------------")

def print_schedule_line(line, station, time):
    print(f'{line.strip().rjust(3)}  | {convert_minutes_to_hourtime(time)} | {station}')

def print_separator():
    print('#' * 40)
    print(' ' * 40)
    print('#' * 40)


def main():
    # hour = "05:40:00"
    # # hour = "11:39:00"
    hour = "09:00:00"
    hour = "11:00:00"
    # hour = "21:00:00"

    # start_station = Station('pl. Daniłowskiego', 51.13845372, 17.05991231)
    # start_station = Station('Kwiska', 51.12527525, 16.98342767)
    start_station = Station('Magellana',51.11350738226508,17.121810255130296)
    # # start_station = Station('PL. GRUNWALDZKI',51.11162051,17.06008642)
    # # start_station = Station('Hubska (Dawida)', 51.093049, 17.042897)
    # start_station = Station('KOSZAROWA (Uniwersytet)', 51.14049516, 17.06847989)

    # end_station = Station('PL. GRUNWALDZKI',51.11162051,17.06008642)
    end_station = Station('DWORZEC AUTOBUSOWY',51.09711282534643,17.03361605839725)
    # end_station = Station('GRABISZYŃSKA (Cmentarz)', 51.08990377, 16.97664203)
    # # end_station = Station('Hubska (Dawida)', 51.093049, 17.042897)
    # # end_station = Station('Wrocławski Park Przemysłowy', 51.113056, 16.99489)
    # # end_station = Station('GRABISZYŃSKA (Cmentarz)', 51.08990377, 16.97664203)
    # # end_station = Station('Mosty Warszawskie',51.12800137,17.05485837)

    # exercise_1a(
    #     start_station, 
    #     end_station, 
    #     hour,
    #     True,
    #     True
    # )

    # print_separator()

    # exercise_1b(
    #     start_station,
    #     end_station,
    #     hour,
    #     True,
    #     True
    # )

    # print_separator()

    # exercise_1c(
    #     start_station,
    #     end_station,
    #     hour,
    #     True,
    #     True
    # ) # 190516

    # print_separator()

    # start_station = Station('KOSZAROWA (Uniwersytet)', 51.14049516, 17.06847989)
    # # start_station = Station('KOSZAROWA (Szpital)',51.14166292,17.06477615)
    # end_station = Station('GRABISZYŃSKA (Cmentarz)', 51.08990377, 16.97664203)
    # start_hour = "21:00:00"

    # exercise_1c(start_station, end_station, start_hour)

    # # graph: Graph = load_csv_as_graph(CONNECTION_GRAPH_FILEPATH)

    # start_station = Station('pl. Daniłowskiego', 51.13845372, 17.05991231)
    # stations_to_visit = [Station('PL. GRUNWALDZKI',51.11162051,17.06008642), Station('KROMERA', 51.13164737, 17.06263024)]
    # tabu_search(start_station, stations_to_visit, hour, graph, heuristic_fn)

    # # print('')
    # # print('-' * 50)
    # # print('')

    # start_station = Station('PL. GRUNWALDZKI',51.11162051,17.06008642)
    # stations_to_visit = [Station('pl. Daniłowskiego', 51.13845372, 17.05991231) , Station('KROMERA', 51.13164737, 17.06263024)]
    # tabu_search(start_station, stations_to_visit, hour, data, heuristic_fn)

    # print('')
    # print('-' * 50)
    # print('')

    # start_station = Station('PL. GRUNWALDZKI',51.11162051,17.06008642)
    # stations_to_visit = [Station('pl. Daniłowskiego', 51.13845372, 17.05991231)]
    # tabu_search(start_station, stations_to_visit, hour, data, heuristic_fn)
    
    # print('')
    # print('-' * 50)
    # print('')

    # hour = "21:26:00"
    # # start_station = Station('Hallera', 51.08713869, 17.01249942)
    # end_station = Station('Gajowicka', 51.08797903, 17.00670968)
    # start_station = Station('Poczta Główna', 51.1078565, 17.04563742)
    # ex_1b(start_station, end_station, None, hour, heuristic_fn)
    
    # print('')
    # print('-' * 50)
    # print('')

    # hour = '21:05:00'
    # start_station = Station('KOSZAROWA (Uniwersytet)', 51.14049516, 17.06847989)
    # stations_to_visit = [Station('Wiejska', 51.07700276, 16.96415159), Station('KRZYKI', 51.07488366, 17.00656861), Station('Poczta Główna', 51.1078565, 17.04563742), Station('FAT', 51.09412632, 16.9783528)]
    # tabu_search(start_station, stations_to_visit, hour, data, heuristic_fn)


    # print('')
    # print('-' * 50)
    # print('')

    # hour = '21:05:00'
    # start_station = Station('KOSZAROWA (Uniwersytet)', 51.14049516, 17.06847989)
    # stations_to_visit = [
    #     Station('FAT', 51.09412632, 16.9783528),
    #     Station('Wiejska', 51.07700276, 16.96415159),
    #     Station('Poczta Główna', 51.1078565, 17.04563742),
    #     Station('KRZYKI', 51.07488366, 17.00656861),
    # ]
    # tabu_search(start_station, stations_to_visit, hour, data, True)

    # hour = '23:00:00'
    # start_station = Station('Poczta Główna', 51.1078565, 17.04563742)
    # end_station = Station('KOSZAROWA (Uniwersytet)', 51.14049516, 17.06847989)
    # exercise_1b(start_station, end_station, hour)

if __name__ == '__main__':
    main()
