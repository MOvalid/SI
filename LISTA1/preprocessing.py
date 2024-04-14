from graph import *

MOSTEK = Station('Żórawina - Niepodległości (Mostek)', 50.97974058, 17.04068965)
SKRZYZ = Station('Żórawina - skrzy. Niepodległości', 50.97974058, 17.04068965)


def remove_rows_with_text(csv_file, text_to_remove):
    temp_file = csv_file + '.tmp'
    with open(csv_file, 'r', newline='', encoding='utf-8') as csv_input, \
         open(temp_file, 'w', newline='', encoding='utf-8') as csv_output:
        csv_reader = csv.reader(csv_input)
        csv_writer = csv.writer(csv_output)
        
        for row in csv_reader:
            if text_to_remove not in row:
                csv_writer.writerow(row)

    shutil.move(temp_file, csv_file)


def remove_unneccesary_stations():
    station_name_to_remove = MOSTEK.name
    remove_rows_with_text(CONNECTION_GRAPH_FILEPATH, station_name_to_remove)
    text_to_remove = SKRZYZ.name
    remove_rows_with_text(CONNECTION_GRAPH_FILEPATH, text_to_remove)


def process_stations(file_path: str):
    data = load_csv(file_path)
    stations = dict()
    for row in data:
        if row[5] in stations:
            temp = stations[row[5]] 
            stations[row[5]] = (temp[0] + float(row[7]), temp[1] + float(row[8]), temp[2] + 1)

        else:
            stations[row[5]] = (float(row[7]), float(row[8]), 1)

        if row[6] in stations:
            temp = stations[row[6]] 
            stations[row[6]] = (temp[0] + float(row[9]), temp[1] + float(row[10]), temp[2] + 1)

        else:
            stations[row[6]] = (float(row[9]), float(row[10]), 1)     

    return {key: (value[0]/value[2], value[1]/value[2]) for key, value in stations.items()}

def save_stations(stations: Dict[str, Tuple[str, str]], output_file_path: str = STATIONS_CSV_FILEPATH) -> None:
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for station, (x, y) in stations.items():
            writer.writerow([station, x, y])
