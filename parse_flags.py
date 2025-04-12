from pathlib import Path
from csv import reader
from unicodedata import normalize, combining
from string import ascii_letters

COLUMN_NAMES = {
    0: 'Country',
    1: 'Alpha-2 code',
    2: 'Alpha-3 code',
    3: 'URL'
}

def _remove_accents(text: str) -> str:
    return ''.join([char for char in normalize('NFKD', text.replace('ł', 'l')) if not combining(char)])

def _cleanup(text: str) -> str:
    allowed_characters = ascii_letters + '-_'
    translation_table = {ord(char): None for char in ''.join(set(text)) if char not in allowed_characters}
    return text.translate(translation_table)

def process_flags() -> bool:
    """Parses the input fights.csv file to add the ID columns to it.

    :return bool: True when the parsing and writing finishes.
    """

    file_path = Path(__file__).parent / 'data' / 'flags.csv'
    with open(file_path, 'r', encoding='utf-8') as input_file:
        downloaded_data = reader(input_file, quotechar='"', delimiter=',')
        file_path = Path(__file__).parent / 'data' / 'flags_processed.csv'
        
        with open(file_path, 'w+', encoding='utf-8-sig', newline='') as output_file:
            column_headers = ''
            for header_name in next(downloaded_data):
                column_headers += header_name + ';'
            column_headers = column_headers[:-1]
            output_file.write(column_headers + '\n')
            for row in downloaded_data:
                record = ''
                for column_no, stat in enumerate(row):
                    if COLUMN_NAMES[column_no] == 'imgURL':
                        normalized_data = stat.strip()
                    else:
                        normalized_data = _remove_accents(stat.strip())
                    if COLUMN_NAMES[column_no] == 'Country':
                        if normalized_data == 'Congo (the Democratic Republic of the)':
                            normalized_data = 'Democratic Republic Congo'
                        elif normalized_data == "Korea (the Democratic People's Republic of)":
                            normalized_data = 'North Korea'
                        elif normalized_data == "Korea (the Democratic People's Republic of)":
                            normalized_data = 'South Korea'
                        if ' (' in normalized_data:
                            normalized_data, _ = normalized_data.split(' (')
                        if ',' in normalized_data:
                            normalized_data, _ = normalized_data.split(',')
                        if 'United Kingdom' in normalized_data:
                            normalized_data = 'United Kingdom'
                        elif 'United States' in normalized_data:
                            normalized_data = 'United States'
                    record += normalized_data + ";"
                output_file.write(record[:-1] + "\n")
    return True

print(process_flags())