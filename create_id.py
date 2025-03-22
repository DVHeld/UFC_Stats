"""Octagon-API JSON to CSV Parsing"""

from pathlib import Path
from csv import reader
from unicodedata import normalize, combining

def _remove_accents(text: str) -> str:
    return ''.join([char for char in normalize('NFKD', text) if not combining(char)])

def create_fight_id() -> bool:
    """Parses the input fights.csv file to add the ID columns to it.

    :return bool: True when the parsing and writing finishes.
    """

    file_path = Path(__file__).parent / 'data' / 'ufc-master.csv'
    with open(file_path, "r", encoding="utf-8") as input_file:
        downloaded_data = reader(input_file, quotechar='"', delimiter=',')
        file_path = Path(__file__).parent / 'data' / 'ufc-master_processed.csv'
        
        with open(file_path, "w+", encoding='utf-8-sig', newline='') as output_file:
            column_headers = "fight_id;fight_alternate_id;fighter_alternate_id_red;fighter_alternate_id_blue"
            for header_name in next(downloaded_data):
                column_headers += ";" + header_name
            output_file.write(column_headers + "\n")

            fight_id = 0
            for row in downloaded_data:
                # Create new fight_id, red and blue fighter_alternate_id
                record = str(fight_id) + ";" + row[6].replace("-", "") + "-" +\
                         _remove_accents(row[0]).lower().replace(" ", "_") + "-" +\
                         _remove_accents(row[1]).lower().replace(" ", "_")
                record += ";" + _remove_accents(row[0]).lower().replace(" ", "-")
                record += ";" + _remove_accents(row[1]).lower().replace(" ", "-")
                for stat in row:
                    record += ";" + _remove_accents(stat).replace(".", ",")
                output_file.write(record + "\n")
                fight_id += 1
    return True
