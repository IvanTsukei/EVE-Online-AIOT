from pathlib import Path
from configparser import ConfigParser
import json
import pandas as pd
import yaml

def read_yaml(path):
    """
    Reads and cleans the yaml file from CCP EVE.
    """

    f = open(path, "r")
    lines, ret, cur = [], [], {}

    # Cleaning #

    for i, line in enumerate(f):
        lines.append(line)

    cleaned_lines = [] 
    for i in range(1, len(lines)):
        if (lines[i][5] == ' '):
            cleaned_lines[len(cleaned_lines) - 1] += lines[i][8:]
        else:
            cleaned_lines.append(lines[i])

    # Reading #

    for line in cleaned_lines:
        if (len(line) == 0): break
        if (line[0] == '-'):
            ret.append(cur)
            cur = {}

        line = line[3:]
        spl = line.split(": ")

        cur[spl[0]] = spl[1].rstrip()

    ret.append(cur)
    ret = ret[1:]
    return ret


def file_path(upath):
    """
    Gets the filepath to the data folder.
    """
    return Path(__file__).parent.resolve() / '../../data' / upath # Points to the file

def all_files():
    """
    Returns all excel files in the folder.
    """
    path = Path(__file__).parent.parent.parent.resolve() / 'data'
    res = [f.__str__().rsplit('\\', 1)[-1] for f in path.glob('*.xlsx')] # f.__str__() faster than str(f). rsplit splits based on \ and gets just file name.
    return res

def station_region_ids(item_list):
    """
    Reads in the IDs and Names of all npc stations/regions in Eve Online.

    Returns a dataframe with the Station and Region IDs swapped to their names.
    """

    eve_stations = read_yaml(file_path("game_data/staStations.yaml"))
    for dict in item_list:
        for k,v in dict.items():
            if k == 'Station': dict[k] = [location[' stationName'] for location in eve_stations if location[' stationID'] == str(v)]
                #print([[(station, station_id) for station,station_id in eve_stations.items()] for eve_stations in eve_stations])
                #dict[k] = [[(station, station_id) for station,station_id in eve_stations.items()] for eve_stations in eve_stations].get(' stationName')

    eve_locations = read_yaml(file_path("game_data/invNames.yaml"))
    for dict in item_list:
        for k,v in dict.items():
            if k == 'Region': dict[k] = [location[' itemName'] for location in eve_locations if location[' itemID'] == str(v)]

    return pd.DataFrame.from_dict(item_list)

def config_reader(section, item):
    """
    Reads in the config.ini file and returns relevant data.
    """
    config = ConfigParser()
    config_fpath = file_path('config.ini')
    config.read(config_fpath)

    return config.get(section, item)

def config_reader_json(section, item):
    """
    Reads in the config.ini file and returns relevant
    data if in json format.
    """
    config = ConfigParser()
    config_fpath = file_path('config.ini')
    config.read(config_fpath)

    return json.loads(config.get(section, item))

def secret_reader(section, item):
    """
    Reads in the config.ini file and returns relevant data.
    """
    config = ConfigParser()
    config_fpath = file_path('secret.ini')
    config.read(config_fpath)

    return config.get(section, item)

def sell_quantity():
    """
    Reads in the min. quanity a region buyer is will to sell of a specific item.
    Returns a list of dict. of key: ID and value: Quantity | key: ID and value: Name
    """
    input_name = str(config_reader('data', 'input_sell_quantity'))
    quantity_config_fpath = file_path(f'{input_name}.xlsx')
    df_buy_quantity = pd.read_excel(quantity_config_fpath)
    quantity_list = dict(zip(df_buy_quantity['ID'], df_buy_quantity['Quantity']))
    id_name = dict(zip(df_buy_quantity['ID'], df_buy_quantity['Name']))
    return [quantity_list, id_name]

def save_region_ids():
    """
    Reads in the yaml dump of eve locations.
    Gets all the region IDs in the game and exports them to a text file for reading.
    """
    eve_locations = read_yaml(file_path("game_data/invNames.yaml"))
    region_ids = []
    for dict in eve_locations:
        for k,v in dict.items():
            if k == ' itemID' and (len(v) == 8 and str(v)[0] == '1'): region_ids.append(v)

    with open(file_path('game_data/allregions.txt'),'w') as file_handler:
        for region in region_ids: file_handler.write(f'{region}\n')

def get_region_ids():
    """
    Reads in all the region ids for eve.
    Returns a list of regions.
    """
    region_ids = []
    with open(file_path('game_data/allregions.txt'),'r') as file_handler:
        for region in file_handler: region_ids.append(region.rstrip('\n'))
    return region_ids