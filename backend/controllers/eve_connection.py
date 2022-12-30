from esipy import EsiApp, EsiClient
import time

start = time.time()

esi_app = EsiApp()
app = esi_app.get_latest_swagger

# basic client, for public endpoints only
client = EsiClient(
    retry_requests=True,  # set to retry on http 5xx error (default False)
    headers={'User-Agent': 'Something CCP can use to contact you and that define your app'},
    raw_body_only=False,  # default False, set to True to never parse response and only return raw JSON string content.
)

# generate the operation tuple
# the parameters given are the actual parameters the endpoint requires
market_order_operation = app.op['get_markets_region_id_orders'](
    region_id=10000002,
    type_id=11188,
    order_type='all',
)

# do the request
response = client.request(market_order_operation)

# use it: response.data contains the parsed result of the request.
print(response.data[0].price)

end = time.time()
print(f'\nTotal time: {end-start}')
res = ((end-start)*118)/60
print(f'\nTotal time for all items approx: {res}')
# to get the headers objects, you can get the header attribute
# print(response.header)
