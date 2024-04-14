import csv, shutil
from typing import List, Tuple, Dict
from utils import convert_hour, convert_minutes_to_hourtime
from timer import Timer

CONNECTION_GRAPH_FILEPATH = fr'.\connection_graph.csv'
STATIONS_CSV_FILEPATH = fr'.\stations.csv'



class Station:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, Station):
            return (self.name == other.name)
        return False
    
    def __lt__(self, other):
        if isinstance(other, Station):
            return (self.name < other.name)
        return False
    
    def to_json(self):
            return {
                'name': self.name,
                'x': self.x,
                'y': self.y
            }
    
class Edge:
    def __init__(self, start_station: Station, end_station: Station, line: str, start_time: str = "00:00:00", end_time: str = "00:00:00"):
        self.start_station = start_station
        self.end_station = end_station
        self.line = line
        self.start_time = convert_hour(start_time)
        self.end_time = convert_hour(end_time)
        self.weight = self.start_time - self.end_time

    def __str__(self):
        # return f'{self.end_station.name}, {self.line}, {self.start_time}, {self.weight}'
        return f'{self.start_station.name.ljust(40)} | {self.end_station.name.ljust(40)} | {self.line.ljust(5)} | {convert_minutes_to_hourtime(self.start_time).ljust(8)} - {convert_minutes_to_hourtime(self.end_time).ljust(8)}'

    
    def weight(self, other_time: int) -> float:
        dt = other_time - self.start_time
        return float('inf') if dt < 0 else other_time - self.end_time

    def __hash__(self):
        return hash((self.start_station, self.end_station, self.line, self.start_time, self.end_time))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self.start_station, self.end_station, self.line, self.start_time, self.end_time) == \
               (other.start_station, other.end_station, other.line, other.start_time, other.end_time)



    def to_json(self):
        return {
            'start_station': self.start_station.to_json(),
            'end_station': self.end_station.to_json(),
            'line': self.line,
            'start_time': self.start_time,
            'weight': self.weight
        }




class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.graph_dict = {}
        for start, edge in self.edges:
            if not start in self.graph_dict:
                self.graph_dict[start] = dict()
            if edge.end_station in self.graph_dict[start]:
                self.graph_dict[start][edge.end_station].add(edge)
            else:
                self.graph_dict[start][edge.end_station] = {edge}

    def __iter__(self):
        self.nodes = iter(self.graph_dict)
        return self

    def __next__(self):
        node = next(self.nodes)
        return (node, self.graph_dict[node])
    
    def get_all_edges(self, start_station) -> List[Edge]:
        return [edge for edges_list in self.graph_dict[start_station].values() for edge in edges_list]
    


 
def load_csv(file_path: str) -> List[List[str]]:
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return data

def load_stations(file_path: str = STATIONS_CSV_FILEPATH) -> Dict[str, Station]:
    stations = dict()
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            stations[row[0]] = Station(row[0], float(row[1]), float(row[2]))
    return stations

def load_csv_as_graph(file_path: str, show_time: bool = True) -> Graph:
    timer = Timer()
    timer.run(load_csv, file_path)

    if show_time:  print(f"Connection graph loading time: {timer.time:.4f} s")

    stations = load_stations()
    edges = [(stations[row[5]], Edge(stations[row[5]], stations[row[6]], row[2], row[3], row[4])) for row in timer.result]

    timer.run(Graph, edges)
    
    if show_time: print(f"Connection graph building time: {timer.time:.4f} s")

    return timer.result



def main():
    data = load_csv_as_graph(CONNECTION_GRAPH_FILEPATH)

    for station, edges in data:
        print(f'{station}({station.x}, {station.y}): {len(edges)}')


if __name__ == '__main__':
    main()