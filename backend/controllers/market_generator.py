import pandas as pd
from eve_connection import get_orders
from file_access import config_reader, buy_quantity

def sell_orders():
    """
    Gets a list of all the active sell orders in a designated region.
    Returns an excel spreadsheet.
    """
    ## Setting up Variables ##
    regions = config_reader()
    floor_quantity = buy_quantity()[0]
    item_id_to_name = buy_quantity()[1]

    df = pd.Dataframe()
    
    ## Looping through items and regions ##
    for id, quanity in floor_quantity.items():
        print(item_id_to_name.get(id)) 
        for places in regions:

            region_items = get_orders(places, type_id=id)

            region_items = [x for x in region_items if x['is_buy_order'] == False and x['volume_remain'] >= quanity]
            print(places)
            try:
                print(min(region_items, key=lambda x:x['price']))
            except:
                print('NA')
            print('\n\n')

sell_orders()