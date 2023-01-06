import pandas as pd
from backend.controllers.eve_connection import get_orders
from backend.controllers.file_access import config_reader, config_reader_json, sell_quantity, region_ids, station_ids, file_path

def sell_orders():
    """
    Gets a list of all the active sell orders in a designated region.
    Returns an excel spreadsheet.
    """

    ## Setting up Variables ##
    regions = config_reader_json('markets', 'regions')
    floor_quantity, item_id_to_name = sell_quantity()[0], sell_quantity()[1]
    region_id_to_name, station_id_to_name = region_ids(), station_ids()
    output_name = str(config_reader('data','output_name'))

    df = pd.DataFrame()
    
    ## Looping through items and regions ##
    for id, quanity in floor_quantity.items():
        df_temp = pd.DataFrame(columns=['Item', 'Region', 'Station', 'Price', 'Quantity'])

        for places in regions:
            region_items = get_orders(places, type_id=id)
            region_items = [x for x in region_items if x['is_buy_order'] == False and x['volume_remain'] >= quanity]

            try:
                temp_dict = min(region_items, key=lambda x:x['price'])
                temp_dict = {k: temp_dict[k] for k in ('location_id', 'price', 'volume_remain')}
                temp_dict = {'Item':[item_id_to_name.get(id)], 'Region':[region_id_to_name.get(places)], 'Station':[station_id_to_name.get(temp_dict.get('location_id'), temp_dict.get('location_id'))], 'Price':[temp_dict.get('price')], 'Quantity':[temp_dict.get('volume_remain')]}
                
                row = pd.DataFrame.from_dict(temp_dict)
                df_temp = pd.concat([df_temp, row], axis = 0)
            except: pass

        df = pd.concat([df, df_temp], axis = 0)

    ## Final Output ##
    df.to_excel(file_path(f'outputs/{output_name}.xlsx'), index=False)