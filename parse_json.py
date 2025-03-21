"""Octagon-API JSON to CSV Parsing"""

from os import path
from pathlib import Path
from json import loads

def parse_fighters() -> bool:

    full_input_path = Path(__file__).parent / 'data' / 'fighters.json'
    with open(full_input_path, "r", encoding="utf-8") as input_file:
        downloaded_data = loads(input_file.read())

    full_output_path = Path(__file__).parent / 'data' / 'fighters.csv'
    if path.exists(full_output_path):
        mode = 'r+'
    else:
        mode = "w+"
    print(mode)
    with open(full_output_path, mode, encoding='utf-8-sig', newline='') as output_file:

        # Existing fighters to skip
        if mode == "r+":
            to_skip = []
            print(output_file.readline())
            for fighter in output_file.readline():
                print(fighter)
                to_skip.append(fighter.split(";")[1])

        header_names = []
        for column_header in list(downloaded_data.values())[0].keys():
            header_names.append(column_header)

        # Adding column headers to newly created file
        if mode == "w+":
            print("a")
            column_headers = "fighter_id;fighter_alternate_id"
            for header_name in header_names:
                column_headers += ";" + header_name
            print("b")
            output_file.write(column_headers + "\n")
            print("c")

        fighter_id = len(output_file.readlines())
        output_file.seek(0)

        for fighter_alternate_id, fighter_data in downloaded_data.items():
            position = 0
            record = str(fighter_id) + ";" + fighter_alternate_id
            for stat, value in fighter_data.items():
                while stat != header_names[position]:
                    record += ";"
                    position += 1
                record += ";" + value
                position += 1

            output_file.write(record + "\n")
            fighter_id += 1
            # print(record)
        
            
            
    
    return False

parse_fighters()
