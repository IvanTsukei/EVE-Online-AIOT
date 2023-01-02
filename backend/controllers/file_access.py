from pathlib import Path
import os.path
import configparser
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

def buy_quantity():
    """
    Reads in the min. quanity a region buyer is will to purchase of a specific item.
    Returns a dict. of key: ID and value: Quantity
    """
    quantity_config_fpath = file_path('itemIDs.xlsx')
    df_buy_quantity = pd.read_excel(quantity_config_fpath)
    quantity_list = dict(zip(df_buy_quantity['ID'], df_buy_quantity['Quantity']))
    id_name = dict(zip(df_buy_quantity['ID'], df_buy_quantity['Name']))
    return [quantity_list, id_name]

def config_reader():
    """
    Reads in the config.ini file and returns relevant data.
    """
    config = configparser.ConfigParser()
    config_fpath = file_path('config.ini')
    config.read(config_fpath)

    json.loads(config.get('markets', 'regions'))

    # Reading Section Values
    market_regions = json.loads(config.get('markets', 'regions'))

    return market_regions

buy_quantity()