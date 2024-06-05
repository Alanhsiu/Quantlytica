# import bybit
import time

import sys
sys.path.append('../')
import config

cur_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
print('current time:', cur_time)

# client = bybit.bybit(test=False, api_key=config.API_KEY, api_secret=config.API_SECRET)
# print('log in successfully')

from pybit.unified_trading import HTTP
session = HTTP(
    testnet=False,
    api_key=config.API_KEY_BYBIT,
    api_secret=config.API_SECRET_BYBIT
)

print(session.get_instruments_info(
    category="linear",
    symbol="OMGUSDT",
))

# # get kline
# print(session.get_kline(
#     category="inverse",
#     symbol="BTCUSD",
#     interval=60,
#     start=int(time.time() * 1000) - 3600000,  # Current time minus 1 hour in milliseconds
#     end=int(time.time() * 1000),  # Current time in milliseconds
# ))

# # get announcement
# print(session.get_announcement(
#     locale="en-US",
#     limit=1,
# ))

# balance = session.get_wallet_balance(
#     accountType="UNIFIED",
#     coin="USDT",
# )
# print('balance:', balance)

# place order
start_time = time.time()
# response = session.place_order(
#     category="spot",
#     symbol="BTCUSDT",
#     side="Sell",
#     orderType="Limit", 
#     price="70661.9", # Limit
#     timeInForce="PostOnly",# Limit
#     qty="0.000126", # Limit
#     # orderType="Market",
#     # qty="7", 
#     orderLinkId=str(cur_time),
#     isLeverage=0,
#     orderFilter="Order",
# )
response = session.place_order(
    category="linear",
    symbol="BTCUSDT",
    side="Sell",
    orderType="Limit", 
    price="72084", 
    qty="1", 
    # orderType="Market",
    # qty="7", 
    orderLinkId=str(cur_time),
    isLeverage=0,
    orderFilter="Order",
)
print('order:', response)
end_time = time.time()
print(f"Runtime: {end_time - start_time} seconds")

# # get all open orders
# response = session.get_open_orders(
#     category="spot",
#     symbol="BTCUSDT",
# )

# # cancel all open orders
# orders = response["result"]["list"]
# for order in orders:
#     session.cancel_order(
#         category="spot",
#         symbol="BTCUSDT",
#         orderId=order["orderId"],
#     )