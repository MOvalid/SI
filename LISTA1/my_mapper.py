from utils import convert_minutes_to_hourtime
from graph import Station
# import folium, webbrowser

COLORS = ['red', 'green', 'blue', 'orange', 'purple']
ZOOM_START = 14


def print_map(start_station, goal_station, path):
    basic_map = folium.Map(location=[start_station.x, start_station.y], zoom_start=ZOOM_START)
    folium.Marker(location=[start_station.x, start_station.y], color='red', popup=f"{start_station.name}").add_to(basic_map)
    prev_station = start_station
    color_i = 0
    current_line = prev_line = path[0].line
    for edge in path:

        if current_line != prev_line:
            color_i = (color_i + 1) % len(COLORS)

        line_label = folium.Tooltip(text=f'[{prev_line}] {prev_station.name} ({convert_minutes_to_hourtime(edge.start_time)}) - {edge.end_station.name} ({convert_minutes_to_hourtime(edge.end_time)})')

        folium.PolyLine([(prev_station.x, prev_station.y), (edge.end_station.x, edge.end_station.y)], tooltip=line_label, color=COLORS[color_i], line_opacity=0.5, weight=4).add_to(basic_map)

        prev_station = edge.end_station
        prev_line = current_line
        current_line = edge.line

        if (edge.end_station == goal_station):  
            folium.Marker(location=[edge.end_station.x, edge.end_station.y],color='red', popup=f"{edge.end_station.name}").add_to(basic_map)
        else:
            folium.Marker(location=[edge.end_station.x, edge.end_station.y], popup=f"{edge.end_station.name}").add_to(basic_map)

    map_name = f"{start_station.name}-{path[-1].end_station.name}.html"
    basic_map.save(map_name)
    webbrowser.open(map_name)


def print_tabu_test():
    stations = [
        Station('KOSZAROWA (Uniwersytet)',51.14049516000027,17.068479890000113),
        Station('Poczta Główna' ,51.10785650000178,17.045637420000244),
        Station('KRZYKI',51.07493721362521,17.0069501585093),
        Station('Wiejska',51.07764363944034,16.96402221613348),
        Station('FAT',51.09447767835252,16.979967113845426),
        Station('KOSZAROWA (Uniwersytet)',51.14049516000027,17.068479890000113)

    ]
    basic_map = folium.Map(location=[stations[0].x, stations[0].y], zoom_start=ZOOM_START)
    for i in range(len(stations)):
        folium.PolyLine([(stations[i].x, stations[i].y), (stations[((i + 1) % len(stations))].x, stations[((i + 1) % len(stations))].y)], color='red', line_opacity=0.5, weight=4).add_to(basic_map)
        folium.Marker(location=[stations[((i + 1) % len(stations))].x, stations[((i + 1) % len(stations))].y],color='red').add_to(basic_map)
    map_name = "tabu_search_map.html"
    basic_map.save(map_name)
    webbrowser.open(map_name)