from pathlib import Path
from configparser import ConfigParser
import json
import pandas as pd
import yaml

def readYaml(path):
    f = open(path, "r")
    ret, cur = [], {}
    enum = enumerate(f)
    for i, line in enum:
        if (len(line) == 0): break
        if (line[0] == '-'):
            ret.append(cur)
            cur = {}

        line = line[3:]
        spl = line.split(": ")
        print(spl)
        # print(next(enum))
        # if len(f[(i + 1) % len(f)]) < 2:
        #     print(f[(i + 1) % len(f)].rsplit())
        # if len(f[(i + 1) % len(f)]) < 2: 
        #     line[1] = line[1] + next(i)

        cur[spl[0]] = spl[1].rstrip()

        # if len(next(line)) < 2: 
        #     line[1] = line[1] + line+1
        print(cur)

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
    
    with open(f'{file_path("game_data/staStations.yaml")}', 'r') as file:
        eve_stations = yaml.load(file, Loader=yaml.CLoader)
        for dict in item_list:
            for k,v in dict.items():
                if k == 'Station': dict[k] = [station for station in eve_stations if station['stationID'] == v][0].get('stationName')

    with open(f'{file_path("game_data/invNames.yaml")}', 'r') as file:
        eve_locations = yaml.load(file, Loader=yaml.CLoader)
        for dict in item_list:
            for k,v in dict.items():
                if k == 'Region': dict[k] = [location for location in eve_locations if location['itemID'] == v][0].get('itemName')

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