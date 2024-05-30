"""
自建指数 | guy@quantlytica.com | quantlytica academy
author: guy@quantlytica.com
https://line.me/ti/p/YW0zkjxnxT
"""
from Evaluate import *
from Config import *
import warnings
warnings.filterwarnings('ignore')
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# 定义一个开始的基准时间，避免周期转换出现问题
benchmark = pd.DataFrame(pd.date_range(start='2017-01-01', end=end_date, freq='1H'))  # 创建2017-01-01至回测结束时间的1H列表
benchmark.rename(columns={0: 'candle_begin_time'}, inplace=True)

# ===导入数据
df = pd.read_pickle(f'{root_path}/data/数据整理/all_data_{hold_period}.pkl')

# 设置benchmark
benchmark_list = ['BTC-USDT'] # 目前支持单一币种为benchmark
if benchmark_list:
    df = df[df['symbol'].isin(benchmark_list)]  # 只保留白名单币种

# 删除某些行数据
df.dropna(subset=['每小时涨跌幅'], inplace=True)
df = df[df['volume'] > 0]  # 该周期不交易的币种
# 筛选日期范围
df = df[df['candle_begin_time'] >= pd.to_datetime(start_date)]
df = df[df['candle_begin_time'] <= pd.to_datetime(end_date)]
# 计算下个周期的收益率
df['ret_next'] = df['close'] / df['open'] - 1
df['开盘买入涨跌幅'] = df['开盘买入涨跌幅'].transform(lambda x: [x])
df['每小时涨跌幅'] = df['每小时涨跌幅'].transform(lambda x: x[1:])
df['每小时涨跌幅'] = df['开盘买入涨跌幅'] + df['每小时涨跌幅']
# 保留指定字段，减少计算时间
df = df[['candle_begin_time', 'symbol', 'ret_next', '每小时涨跌幅']]

df.reset_index(drop=True, inplace=True)
print('数据处理完毕!!!')


# ===选币
select_coin = df.copy()
# 保留指定字段
select_coin = select_coin[['candle_begin_time', 'symbol', 'ret_next', '每小时涨跌幅']]
select_coin.sort_values(by='candle_begin_time', inplace=True)
select_coin.reset_index(drop=True, inplace=True)
print('选币处理完毕!!!')
print(select_coin)

# 整理选币信息
select_coin['当周期选币数量'] = select_coin.groupby('candle_begin_time')['symbol'].transform('size')
# 通过币种的每小时涨跌幅，计算币种的每小时资金曲线
select_coin['每小时资金曲线'] = select_coin['每小时涨跌幅'].apply(lambda x: np.cumprod(np.array(list(x)) + 1))
select_coin['选币'] = select_coin['symbol'] + ' '

# 计算周期内的持仓收益
group = select_coin.groupby('candle_begin_time')
merge_df = pd.DataFrame()
merge_df['选币'] = group['选币'].sum()
merge_df['选币数量'] = group['选币'].size()
# 合并多币的资金曲线
merge_df['每小时资金曲线'] = group['每小时资金曲线'].apply(lambda x: np.mean(x, axis=0))
# 计算周期的涨跌幅
merge_df['周期涨跌幅'] = merge_df['每小时资金曲线'].apply(lambda x: x[-1] - 1)
# 通过每小时资金曲线，计算每小时账户资金的涨跌幅
merge_df['每小时涨跌幅'] = merge_df['每小时资金曲线'].apply(lambda x: list(pd.DataFrame([1] + list(x)).pct_change()[0].iloc[1:]))
merge_df['开平仓标识'] = 1
print(merge_df)

# 将合并后的资金曲线，与benchmark合并
index_df = pd.merge(left=benchmark, right=merge_df[['选币', '选币数量', '开平仓标识']], on=['candle_begin_time'], how='left', sort=True)
# 填充选币数据
index_df['选币数量'].fillna(method='ffill', inplace=True)
index_df['选币'].fillna(method='ffill', inplace=True)
index_df.dropna(subset=['选币'], inplace=True)
index_df.reset_index(inplace=True, drop=True)
# 将每小时涨跌幅数据，填充到index中
index_df['涨跌幅'] = merge_df['每小时涨跌幅'].sum()
# 计算最终每小时净值变化
index_df['资金曲线'] = (index_df['涨跌幅'] + 1).cumprod()
# 构建指数填充字段
index_df['open'] = index_df['资金曲线']
index_df['high'] = index_df['资金曲线']
index_df['low'] = index_df['资金曲线']
index_df['close'] = index_df['资金曲线']
index_df['volume'] = 1
# 首行数据单独处理一下
index_df.loc[0, 'open'] = 1  # 最开始的资金曲线从1开始
index_df.loc[0, 'high'] = max(index_df.loc[0, 'high'], 1)
index_df.loc[0, 'low'] = min(index_df.loc[0, 'low'], 1)
# 将开平仓标志向前移1h，上个周期最后一个小时结束后进行换仓
index_df['开平仓标识'] = index_df['开平仓标识'].shift(-1)
# 筛选指定字段保存
col_list = ['candle_begin_time', '选币', 'open', 'high', 'low', 'close', 'volume', '开平仓标识', '资金曲线', '涨跌幅']
index_df[col_list].to_csv(root_path + f'/data/指数结果/{str(benchmark_list)}_benchmark_每小时资金曲线.csv', encoding='gbk', index=False)
print(index_df)

# ===每小时资金曲线绘图
equity = index_df.copy()
equity.reset_index(inplace=True)
equity['本周期多空涨跌幅'] = equity['涨跌幅']

# ===策略评价
rtn = strategy_evaluate(equity)
print(rtn)

# ===画图
pic_title = 'factor:%s_nv:%s_pro:%s_risk:%s' % (benchmark_list, rtn.at['累积净值', 0], rtn.at['年化收益', 0], rtn.at['最大回撤', 0])
draw_equity_curve_mat(equity, data_dict={'BTC': '资金曲线'}, date_col='candle_begin_time', title=pic_title)
# 如果上面的函数不能画图，就用下面的画图
# draw_equity_curve_plotly(equity, data_dict={'策略资金曲线': '资金曲线'}, date_col='candle_begin_time', title=pic_title)
