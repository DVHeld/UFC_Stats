"""Octagon-API JSON to CSV Parsing"""

from pathlib import Path
from csv import reader
from unicodedata import normalize, combining
from string import ascii_letters

STAT_NAMES = {
    0: 'fight_id',
    1: 'fight_alternate_id',
    2: 'fighter_alternate_id_red',
    3: 'fighter_alternate_id_blue',
    4: 'RedFighter',
    5: 'BlueFighter',
    6: 'Gender',
    7: 'BlueStance',
    8: 'BlueHeightCms',
    9: 'BlueReachCms',
    10: 'RedStance',
    11: 'RedHeightCms',
    12: 'RedReachCms',
    13: 'RedOdds',
    14: 'BlueOdds',
    15: 'RedExpectedValue',
    16: 'BlueExpectedValue',
    17: 'Date',
    18: 'Location',
    19: 'Country',
    20: 'Winner',
    21: 'TitleBout',
    22: 'WeightClass',
    23: 'NumberOfRounds',
    24: 'BlueCurrentLoseStreak',
    25: 'BlueCurrentWinStreak',
    26: 'BlueDraws',
    27: 'BlueAvgSigStrLanded',
    28: 'BlueAvgSigStrPct',
    29: 'BlueAvgSubAtt',
    30: 'BlueAvgTDLanded',
    31: 'BlueAvgTDPct',
    32: 'BlueLongestWinStreak',
    33: 'BlueLosses',
    34: 'BlueTotalRoundsFought',
    35: 'BlueTotalTitleBouts',
    36: 'BlueWinsByDecisionMajority',
    37: 'BlueWinsByDecisionSplit',
    38: 'BlueWinsByDecisionUnanimous',
    39: 'BlueWinsByKO',
    40: 'BlueWinsBySubmission',
    41: 'BlueWinsByTKODoctorStoppage',
    42: 'BlueWins',
    43: 'BlueWeightLbs',
    44: 'RedCurrentLoseStreak',
    45: 'RedCurrentWinStreak',
    46: 'RedDraws',
    47: 'RedAvgSigStrLanded',
    48: 'RedAvgSigStrPct',
    49: 'RedAvgSubAtt',
    50: 'RedAvgTDLanded',
    51: 'RedAvgTDPct',
    52: 'RedLongestWinStreak',
    53: 'RedLosses',
    54: 'RedTotalRoundsFought',
    55: 'RedTotalTitleBouts',
    56: 'RedWinsByDecisionMajority',
    57: 'RedWinsByDecisionSplit',
    58: 'RedWinsByDecisionUnanimous',
    59: 'RedWinsByKO',
    60: 'RedWinsBySubmission',
    61: 'RedWinsByTKODoctorStoppage',
    62: 'RedWins',
    63: 'RedWeightLbs',
    64: 'RedAge',
    65: 'BlueAge',
    66: 'LoseStreakDif',
    67: 'WinStreakDif',
    68: 'LongestWinStreakDif',
    69: 'WinDif',
    70: 'LossDif',
    71: 'TotalRoundDif',
    72: 'TotalTitleBoutDif',
    73: 'KODif',
    74: 'SubDif',
    75: 'HeightDif',
    76: 'ReachDif',
    77: 'AgeDif',
    78: 'SigStrDif',
    79: 'AvgSubAttDif',
    80: 'AvgTDDif',
    81: 'EmptyArena',
    82: 'BMatchWCRank',
    83: 'RMatchWCRank',
    84: 'RWFlyweightRank',
    85: 'RWFeatherweightRank',
    86: 'RWStrawweightRank',
    87: 'RWBantamweightRank',
    88: 'RHeavyweightRank',
    89: 'RLightHeavyweightRank',
    90: 'RMiddleweightRank',
    91: 'RWelterweightRank',
    92: 'RLightweightRank',
    93: 'RFeatherweightRank',
    94: 'RBantamweightRank',
    95: 'RFlyweightRank',
    96: 'RPFPRank',
    97: 'BWFlyweightRank',
    98: 'BWFeatherweightRank',
    99: 'BWStrawweightRank',
    100: 'BWBantamweightRank',
    101: 'BHeavyweightRank',
    102: 'BLightHeavyweightRank',
    103: 'BMiddleweightRank',
    104: 'BWelterweightRank',
    105: 'BLightweightRank',
    106: 'BFeatherweightRank',
    107: 'BBantamweightRank',
    108: 'BFlyweightRank',
    109: 'BPFPRank',
    110: 'BetterRank',
    111: 'Finish',
    112: 'FinishDetails',
    113: 'FinishRound',
    114: 'FinishRoundTime',
    115: 'TotalFightTimeSecs',
    116: 'RedDecOdds',
    117: 'BlueDecOdds',
    118: 'RSubOdds',
    119: 'BSubOdds',
    120: 'RKOOdds',
    121: 'BKOOdds',
}

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
    with open(file_path, 'r', encoding='utf-8') as input_file:
        downloaded_data = reader(input_file, quotechar='"', delimiter=',')
        file_path = Path(__file__).parent / 'data' / 'ufc-master_processed.csv'
        
        with open(file_path, 'w+', encoding='utf-8-sig', newline='') as output_file:
            column_headers = 'fight_id;fight_alternate_id;fighter_alternate_id_red;fighter_alternate_id_blue'
            for header_name in next(downloaded_data):
                column_headers += ';' + header_name
            output_file.write(column_headers + '\n')

            fight_id = 0
            for row in downloaded_data:
                # Create new fight_id, red and blue fighter_alternate_id
                record = str(fight_id) + ';' + row[6].strip().replace('-', '') + '-' +\
                         _cleanup(_remove_accents(row[0].strip()).lower().replace(' ', '_')) + '-' +\
                         _cleanup(_remove_accents(row[1].strip()).lower().replace(' ', '_'))
                record += ';' + _cleanup(_remove_accents(row[0].strip()).lower().replace(' ', '-'))
                record += ';' + _cleanup(_remove_accents(row[1].strip()).lower().replace(' ', '-'))
                for stat_no, stat in enumerate(row):
                    normalized_stat = _remove_accents(stat.strip()) #.replace('.', ',')
                    if STAT_NAMES[stat_no] in ('RedStance', 'BlueStance'):
                        if normalized_stat == 'Wrestler':
                            normalized_stat = 'Wrestling'
                        elif normalized_stat == 'Kickboxer':
                            normalized_stat = 'Kickboxing'
                        elif normalized_stat == 'Boxer':
                            normalized_stat = 'Boxing'
                        elif normalized_stat == 'Brawler':
                            normalized_stat = 'Brawling'
                        elif normalized_stat == 'Grappler':
                            normalized_stat = 'Grappling'
                        elif normalized_stat == 'Striker':
                            normalized_stat = 'Striking'
                    elif stat_no in range(78, 106):
                        if normalized_stat == '':
                            normalized_stat = '16'
                    elif STAT_NAMES[stat_no] == 'Country':
                        if normalized_stat == 'USA':
                            normalized_stat = 'United States'
                        elif normalized_stat == 'England': # Necessary?
                            normalized_stat = 'United Kingdom'
                        
                    record += ';' + normalized_stat
                output_file.write(record + '\n')
                fight_id += 1
    return True

