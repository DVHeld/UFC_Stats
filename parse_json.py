"""Octagon-API JSON to CSV Parsing"""

from pathlib import Path
from json import loads
from unicodedata import normalize, combining
from string import ascii_letters

def _remove_accents(text: str) -> str:
    return ''.join([char for char in normalize('NFKD', text.replace('ł', 'l')) if not combining(char)])

def _cleanup(text: str) -> str:
    allowed_characters = ascii_letters + '-_'
    translation_table = {ord(char): None for char in ''.join(set(text)) if char not in allowed_characters}
    return text.translate(translation_table)

def parse_fighters() -> bool:
    """Parses the input fighters.json file into a correctly formatted csv.

    :return bool: True when the parsing and writing finishes.
    """

    file_path = Path(__file__).parent / 'data' / 'fighters.json'
    with open(file_path, "r", encoding="utf-8") as input_file:
        downloaded_data = loads(input_file.read())
    file_path = Path(__file__).parent / 'data' / 'fighters.csv'
    with open(file_path, "w+", encoding='utf-8-sig', newline='') as output_file:

        # Get column header names for synching
        header_names = []
        for column_header in list(downloaded_data.values())[0].keys():
            header_names.append(column_header)
        output_file.seek(0)

        # Adding column headers to newly created file
        column_headers = 'fighter_id;fighter_alternate_id'
        for header_name in header_names:
            column_headers += ';' + header_name
        output_file.write(column_headers + '\n')

        # Write each fighter's data into the output file
        for fighter_alternate_id, fighter_data in downloaded_data.items():
            position = 0
            record = ''
            for stat, value in fighter_data.items():
                # Synch for empty data
                while stat != header_names[position]:
                    record += ';'
                    position += 1
                if stat == 'category':
                    record += ';' + _remove_accents(value.strip()).replace(' Division', '')
                elif stat == 'name':
                    fighter_alternate_id = _cleanup(
                                           _remove_accents(value.strip()).lower().replace(' ', '-')
                                           )
                    record += ';' + _remove_accents(value.strip())
                else:
                    record += ';' + _remove_accents(value.strip())
                position += 1
            record = ';' + fighter_alternate_id + record
            output_file.write(record + '\n')
    return True
