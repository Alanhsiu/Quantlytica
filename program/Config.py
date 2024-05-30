"""
自建指数 | guy@quantlytica.com | quantlytica academy
author: guy@quantlytica.com
https://line.me/ti/p/YW0zkjxnxT
"""

import os

_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, '..'))  # 返回根目录文件夹


# k线数据路径
kline_path = root_path + '/data/k线数据/'

# 回测信息配置
start_date = '2021-01-01'  # 回测开始时间
end_date = '2024-03-28'  # 回测结束时间
hold_period = '30D'  # 持仓周期。目前回测只支持日线级别
index_name = 'Q3PriceMA'
black_list=[]
# black_list = ['TRB-USDT','BNB-USDT','OP-USDT','APT-USDT','EOS-USDT','AXS-USDT']  # 例：LUNA-USDT, 这里与实盘不太一样，需要有'-'
white_list = ['BTC-USDT', 'ETH-USDT', 'XRP-USDT', 'SOL-USDT', 'ADA-USDT','DOGE-USDT','TRX-USDT', 'LINK-USDT', 'AVAX-USDT',
               'MATIC-USDT','DOT-USDT','LTC-USDT','SHIB-USDT', 'BCH-USDT','ATOM-USDT', 'RNDR-USDT','NEAR-USDT',
              'STX-USDT','ROSE-USDT','IMX-USDT','APE-USDT','HBAR-USDT','LRC-USDT','MINA-USDT','QNT-USDT','OP-USDT',
              'SAND-USDT','CHZ-USDT','XLM-USDT','ENJ-USDT','GMT-USDT','AXS-USDT','APT-USDT','FLOW-USDT','ENS-USDT',
              'ICP-USDT','BICO-USDT','MASK-USDT','JASMY-USDT','BNB-USDT']  # 例：LUNA-USDT, 这里与实盘不太一样，需要有'-'
# white_list=[]
# 参与计算的所有因子，一次性计算节约时间，避免反复1_数据整理
factor_class_list = ['PriceMa','QuoteVolumeStd','MarketCap_Max']