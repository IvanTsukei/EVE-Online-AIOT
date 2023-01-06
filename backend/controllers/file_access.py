from pathlib import Path
from configparser import ConfigParser
import json
import pandas as pd

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

def region_ids():
    """
    Reads in the IDs and Names of all regions in Eve Online.
    Returns a dict. of key: ID and value: Name
    """
    quantity_config_fpath = file_path('game_data/region_ids.xlsx')
    df_buy_quantity = pd.read_excel(quantity_config_fpath)
    id_name = dict(zip(df_buy_quantity['ID'], df_buy_quantity['Name']))
    return id_name

def station_ids():
    """
    Reads in the IDs and Names of all npc stations in Eve Online.
    Returns a dict. of key: ID and value: Name
    """
    quantity_config_fpath = file_path('game_data/npc_station_ids.xlsx')
    df_buy_quantity = pd.read_excel(quantity_config_fpath)
    id_name = dict(zip(df_buy_quantity['ID'], df_buy_quantity['Name']))
    return id_name

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