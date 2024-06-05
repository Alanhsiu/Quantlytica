## ref: https://vocus.cc/article/63ff24b1fd897800012888ef

from utils import place_order,send_to_telegram,get_signal,get_signal_fast
import time
import os
from datetime import datetime

if __name__ == '__main__':
    while True:# 持續執行
        side,n1,n2 = get_signal_fast() # 取得交易訊號
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 時間

        print(f'<bitcoin> side:{side} n1:{n1} n2:{n2} current_time:{cur_time}') #打印信息
        
        if side != 'PASS': # 判斷是否出現方向
            send_to_telegram(message=side)# 發送電報
            # place_order(side) # 根據訊號方向下單
        time.sleep(60*15) # 等15分鐘出現下一根k棒
        os.system("cls") # 清除屏幕
        
from binance.client import Client
import config

api_key = config.API_KEY
api_secret = config.API_SECRET
print(f'API Key: {api_key}')
print(f'API Secret: {api_secret}')

client = Client(api_key=api_key,api_secret=api_secret)