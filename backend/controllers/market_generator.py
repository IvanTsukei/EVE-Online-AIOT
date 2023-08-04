import pandas as pd
import numpy as np
from eve_connection import get_orders
from file_access import config_reader_json, sell_quantity, station_region_ids, get_region_ids

def sell_orders():
    """
    Gets a list of all the active sell orders in a designated region.
    Returns a pandas dataframe.
    """

    ## Setting up Variables ##
    regions = config_reader_json('markets', 'regions')
    floor_quantity, item_id_to_name = sell_quantity()[0], sell_quantity()[1]

    matched_items = []
    
    ## Looping through items and regions ##
    for id, quantity in floor_quantity.items():
        for places in regions:
            region_items = get_orders(places, type_id=id) 
            region_items = [x for x in region_items if x['is_buy_order'] == False and x['volume_remain'] >= quantity]

            try:
                temp_dict = min(region_items, key=lambda x:x['price'])
                temp_dict = {k: temp_dict[k] for k in ('location_id', 'price', 'volume_remain')}
                temp_dict = {'Item':item_id_to_name.get(id), 'Region':places, 'Station':temp_dict.get('location_id'), 'Price':temp_dict.get('price'), 'Quantity':temp_dict.get('volume_remain')}
                matched_items.append(temp_dict)
            except: pass
    return station_region_ids(matched_items)

def all_orders():
    """
    Gets a list of all orders for all regions in eve.
    Returns a pandas dataframe.
    """
    regions = [eval(i) for i in get_region_ids()]
    temp_df = pd.DataFrame()

    for places in regions:
        region_items = get_orders(places)
        temp_df = pd.concat([temp_df, pd.DataFrame.from_dict(region_items)], ignore_index=True, sort=False)
    
    return temp_df