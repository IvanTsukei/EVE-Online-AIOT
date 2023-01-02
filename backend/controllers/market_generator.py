import pandas as pd
from eve_connection import get_orders, get_history
from file_access import config_reader, buy_quantity

def buy_orders():
    regions = config_reader()
    floor_quantity = buy_quantity()
 
    for places in regions:
        region_items = get_orders(places, type_id=11549)

        region_items = [x for x in region_items if x['is_buy_order'] == False and x['volume_remain'] >= 200]
        print(places)
        # for item in region_items:
        #     print(item)
        try:
            print(min(region_items, key=lambda x:x['price']))
        except:
            print('NA')
        print('\n\n')

buy_orders()