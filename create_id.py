"""Octagon-API JSON to CSV Parsing"""

from os import path
from pathlib import Path
from csv import reader

def create_fight_id() -> bool:
    """Parses the input fighters.json file into a correctly formatted csv.

    :return bool: True when the parsing and writing finishes.
    """

    file_path = Path(__file__).parent / 'data' / 'ufc-master.csv'
    with open(file_path, "r", encoding="utf-8") as input_file:
        downloaded_data = reader(input_file, quotechar='"', delimiter=',')
        file_path = Path(__file__).parent / 'data' / 'ufc-master_processed.csv'
        
        # TODO: Update mode
        # if path.exists(file_path):
        #     mode = 'r+'
        # else:
        #     mode = "w+"
        with open(file_path, "w+", encoding='utf-8-sig', newline='') as output_file:

        #     # Existing fights to skip
        #     to_skip = []
        #     if mode == "r+":
        #         output_file.readline()
        #         fight = output_file.readline()
        #         while fight:
        #             to_skip.append([fight.split(",")[0], fight.split(",")[1], fight.split(",")[6]])
        #             fight = output_file.readline()

        #     fight_id = len(output_file.readlines())
        #     output_file.seek(0)

            # Adding column headers to newly created file
            # if mode == "w+":
            fight_id = 0
            column_headers = "fight_id;fight_alternate_id"
            for header_name in next(downloaded_data):
                column_headers += ";" + header_name
            output_file.write(column_headers + "\n")

            # Write each fight's data into the output file
            for row in downloaded_data:
                # if [row[0], row[1], row[6]] in to_skip:
                #     continue
                record = str(fight_id) + ";" + row[6].replace("-", "") + row[0].lower().replace(" ", "_") + "-" + row[1].lower().replace(" ", "_")
                for stat in row: 
                    record += ";" + stat.replace(".", ",")
                output_file.write(record + "\n")
                fight_id += 1
    return True

create_fight_id()