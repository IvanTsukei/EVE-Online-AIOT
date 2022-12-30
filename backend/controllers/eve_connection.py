import requests

#Gets orders in region_id. 
#order_type can be 'all', 'buy', or 'sell', and it is optional
#page is optional and should be an integer, and is only if you want to access next page of orders(if 1000 on current page)
#type_id is optional, and can specify an item type id

#https://esi.evetech.net/ui/#/Market/get_markets_region_id_orders
def get_orders(region_id, order_type="all", page=1, type_id=None):
    param_string=f"order_type={order_type}&page={page}"
    if type_id:
        param_string += f"&type_id={type_id}"
    return requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/orders?{param_string}").json()

def id_to_name(id):
    return requests.post("https://esi.evetech.net/latest/universe/names/", json=[id]).json()

def ids_to_names(ids):
    return requests.post("https://esi.evetech.net/latest/universe/names/", json=ids).json()

#https://esi.evetech.net/ui/#/Market/get_markets_region_id_history
def get_history(region_id, type_id): 
    return requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/history?type_id={type_id}").json()

regions = [10000002, 10000032, 10000043, 10000042, 10000030]

for places in regions:
    region_items = get_orders(places, type_id=29248)
    for item in region_items:
        print(item)
    print('\n\n')