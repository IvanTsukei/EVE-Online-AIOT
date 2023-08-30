import pandas as pd
from datetime import datetime
from eve_connection import get_orders
from file_access import config_reader_json, sell_quantity, station_region_ids, get_region_ids
from database_handler import fetch_database_latest
from datetime import datetime, timezone, timedelta

def sell_orders():
    """
    Gets a list of all the active sell orders in a designated region.
    Returns a pandas dataframe.
    """

    ## Setting up Variables ##

    # First three are for querying the MongoDB collection #
    time_tdy = f'{datetime.now(timezone.utc).strftime("%Y-%m-%d")} 13:01'
    time_yesterday = f'{(datetime.now(timezone.utc)- timedelta(days=1)).strftime("%Y-%m-%d")} 13:01'
    create_indx, indx_nme = True, 'timestamp'

    # These are for querying the dataframe or results #
    regions = config_reader_json('markets', 'stations')
    floor_quantity, item_id_to_name = sell_quantity()[0], sell_quantity()[1]

    # These get the dataframe of latest market data #
    if datetime.now(timezone.utc).strftime('%H:%M') >= '13:01':
        active_orders = fetch_database_latest({indx_nme:time_tdy}, create_indx, indx_nme, f'{time_tdy}')
    else:
        active_orders = fetch_database_latest({indx_nme:time_yesterday}, create_indx, indx_nme, f'{time_yesterday}')
    
    active_orders = active_orders.drop(['_id', 'timestamp', 'issued', 'range'], axis=1)
    matched_items = []
    
    ## Looping through items and regions ##
    for id, quantity in floor_quantity.items():
        for places in regions:
            print(places, id)
            region_items = active_orders.loc[(active_orders['system_id'] == places) & active_orders['type_id'] == id]
            region_items = active_orders.loc[(active_orders['is_buy_order'] == False) & active_orders['volume_remain'] >= quantity]
            print(region_items)
            
    #         try:
    #             temp_dict = min(region_items, key=lambda x:x['price'])
    #             temp_dict = {k: temp_dict[k] for k in ('location_id', 'price', 'volume_remain')}
    #             temp_dict = {'Item':item_id_to_name.get(id), 'Region':places, 'Station':temp_dict.get('location_id'), 'Price':temp_dict.get('price'), 'Quantity':temp_dict.get('volume_remain')}
    #             matched_items.append(temp_dict)
    #         except: pass
    # return station_region_ids(matched_items)

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
    
    temp_df['timestamp'] = datetime.today().strftime('%Y-%m-%d %H:%M')
    return temp_df.to_dict(orient='records') # needs to be in dict form.