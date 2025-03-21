"""Octagon-API JSON to CSV Parsing"""

from os import path
from json import loads

def parse_fighters() -> bool:

    full_input_path = r"D:\Projects\UFC_Stats\Sources\fighters.json"
    with open(full_input_path, "r", encoding="utf-8") as input_file:
        downloaded_data = loads(input_file.read())

    full_output_path = r"D:\Projects\UFC_Stats\Sources\fighters.csv"
    if path.exists(full_output_path):
        mode = 'r+'
    else:
        mode = "w+"
    with open(full_output_path, mode, encoding='utf-8-sig', newline='') as output_file:
        pass
    
    return False
