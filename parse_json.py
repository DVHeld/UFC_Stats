"""Octagon-API JSON to CSV Parsing"""

from os import path
from pathlib import Path
from json import loads

def parse_fighters() -> bool:
    """Parses the input fighters.json file into a correctly formatted csv.

    :return bool: True when the parsing and writing finishes.
    """

    file_path = Path(__file__).parent / 'data' / 'fighters.json'
    with open(file_path, "r", encoding="utf-8") as input_file:
        downloaded_data = loads(input_file.read())
    file_path = Path(__file__).parent / 'data' / 'fighters.csv'
    if path.exists(file_path):
        mode = 'r+'
    else:
        mode = "w+"
    with open(file_path, mode, encoding='utf-8-sig', newline='') as output_file:

        # Existing fighters to skip
        if mode == "r+":
            to_skip = []
            output_file.readline()
            fighter = output_file.readline()
            while fighter:
                print(fighter)
                to_skip.append(fighter.split(";")[1])
                fighter = output_file.readline()

        # Get column header names for synching
        header_names = []
        for column_header in list(downloaded_data.values())[0].keys():
            header_names.append(column_header)

        fighter_id = len(output_file.readlines())
        output_file.seek(0)

        # Adding column headers to newly created file
        if mode == "w+":
            column_headers = "fighter_id;fighter_alternate_id"
            for header_name in header_names:
                column_headers += ";" + header_name
            output_file.write(column_headers + "\n")

        # Write each fighter's data into the output file
        for fighter_alternate_id, fighter_data in downloaded_data.items():
            position = 0
            record = str(fighter_id) + ";" + fighter_alternate_id

            # Synch for empty data
            for stat, value in fighter_data.items():
                while stat != header_names[position]:
                    record += ";"
                    position += 1
                record += ";" + value
                position += 1

            output_file.write(record + "\n")
            fighter_id += 1
    return True
