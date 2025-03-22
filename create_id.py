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

            column_headers = "fight_id;fight_alternate_id"
            for header_name in next(downloaded_data):
                #Exclude fighter details
                if header_name in ["BlueFighter", "RedFighter"]:
                    header_name += "ID"
                if header_name not in ["RedStance", "BlueStance", "RedHeightCms",\
                                       "BlueHeightCms", "RedReachCms", "BlueReachCms"]:
                    column_headers += ";" + header_name
            output_file.write(column_headers + "\n")

            # Write each fight's data into the output file
            fight_id = 0
            for row in downloaded_data:
                record = str(fight_id) + ";" + row[6].replace("-", "") + "-" +\
                         _remove_accents(row[0]).lower().replace(" ", "_") + "-" +\
                         _remove_accents(row[1]).lower().replace(" ", "_")
                for stat_no, stat in enumerate(row):
                    if stat_no not in [33, 34, 35, 56, 57, 58]:
                        if stat_no in [0, 1]:
                            record += ";" + _remove_accents(stat).lower().replace(" ", "-")
                        else:
                            record += ";" + _remove_accents(stat).replace(".", ",")
                output_file.write(record + "\n")
                fight_id += 1
    return True
