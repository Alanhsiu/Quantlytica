import pandas as pd
import datetime as dt
from Config import *

# 转换周期
config_frq = '1D' # 1M

# 选币因子
factor_list = [
    ('PriceMa', True, [21]),  # QuoteVolumeStd，PriceMa
]

# 构建df中参与选币的因子信息
factor_column_list = []
factor_name_list = []
for factor_name, if_reverse, parameter_list in factor_list:
    factor_column_list.append(f'{factor_name}_{str(parameter_list)}')
    factor_name_list.append(f'{factor_name}_{str(parameter_list)}_{if_reverse}')

# read csv
df = pd.read_csv(root_path + f'/data/result/{str(factor_name_list)}_{str(index_name)}指数回测.csv', encoding='gbk', parse_dates=['candle_begin_time'])
df.sort_values(by='candle_begin_time', inplace=True)
df = df[['candle_begin_time', '选币','开平仓标识','指数净值','btc_净值']]
df.set_index('candle_begin_time', inplace=True)

df_resample = df.copy()
agg_dict = {
    '指数净值': 'last',
    'btc_净值': 'last',
    '选币': 'last',
    '开平仓标识': 'last',
}
df_resample=df_resample.resample(config_frq).agg(agg_dict)
df_resample.sort_values(by='candle_begin_time', inplace = True)
df_resample.reset_index(inplace=True)
print(df_resample.tail(60))
# to csv
df_resample.to_csv(root_path + f'/data/result/{str(factor_name_list)}_{str(index_name)}_{str(config_frq)}周期指数回测.csv', encoding='gbk', index=False)

