"""Octagon-API JSON to CSV Parsing"""

from pathlib import Path
from csv import reader
from unicodedata import normalize, combining
from string import ascii_letters

def _remove_accents(text: str) -> str:
    return ''.join([char for char in normalize('NFKD', text.replace('ł', 'l')) if not combining(char)])

def _cleanup(text: str) -> str:
    allowed_characters = ascii_letters + '-_'
    translation_table = {ord(char): None for char in ''.join(set(text)) if char not in allowed_characters}
    return text.translate(translation_table)


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
                record = str(fight_id) + ";" + row[6].strip().replace("-", "") + "-" +\
                         _cleanup(_remove_accents(row[0].strip()).lower().replace(" ", "_")) + "-" +\
                         _cleanup(_remove_accents(row[1].strip()).lower().replace(" ", "_"))
                record += ";" + _cleanup(_remove_accents(row[0].strip()).lower().replace(" ", "-"))
                record += ";" + _cleanup(_remove_accents(row[1].strip()).lower().replace(" ", "-"))
                for stat in row:
                    normalized_stat = _remove_accents(stat.strip()) #.replace(".", ",")
                    if normalized_stat == "Wrestler":
                        normalized_stat = "Wrestling"
                    elif normalized_stat == "Kickboxer":
                        normalized_stat = "Kickboxing"
                    elif normalized_stat == "Boxer":
                        normalized_stat = "Boxing"
                    elif normalized_stat == "Brawler":
                        normalized_stat = "Brawling"
                    elif normalized_stat == "Grappler":
                        normalized_stat = "Grappling"
                    elif normalized_stat == "Striker":
                        normalized_stat = "Striking"
                    record += ";" + normalized_stat
                output_file.write(record + "\n")
                fight_id += 1
    return True
