"""
自建指数 | guy@quantlytica.com | quantlytica academy
author: guy@quantlytica.com
https://line.me/ti/p/YW0zkjxnxT
"""


def calc_factors_for_filename(df, factor_list, filename=''):
    """
    使用文件夹下的因子脚本进行计算因子
    :param df: 原始k线数据
    :param factor_list: 需要计算的因子列表
    :param filename: 指定因子文件夹名称
    :return:
    """
    column_list = []
    # 根据config中设置的因子列表，逐个计算每个因子的数据
    for factor in factor_list:
        _cls = __import__('%s.%s' % (filename, factor), fromlist=('',))
        # 获取当前因子下的所有参数
        param_list = getattr(_cls, 'get_parameter')()
        # 遍历参数，计算每个参数对应的因子值
        for n in param_list:
            factor_name = f'{factor}_{str(n)}'
            # 计算因子
            df = getattr(_cls, 'signal')(df, n, factor_name)
            # 为了跟实盘保持一致，所有因子信息在下个周期生效
            df[factor_name] = df[factor_name].shift(1)
            # 保存因子列名
            column_list.append(factor_name)

    return df, column_list


def trans_period_for_period(df, period, exg_dict=None):
    """
    周期转换函数
    :param df: K线数据
    :param period: 数据转换周期
    :param exg_dict: 转换规则
    """
    df.set_index('candle_begin_time', inplace=True)
    # 必备字段
    agg_dict = {
        'symbol': 'last',
        '_merge': 'first',
        '开盘买入涨跌幅': 'first',
        'volume': 'sum',
    }
    if exg_dict:
        agg_dict = dict(agg_dict, **exg_dict)

    period_df = df.resample(period).agg(agg_dict)
    # 计算周期资金曲线
    period_df['每小时涨跌幅'] = df['涨跌幅'].resample(period).apply(lambda x: list(x))
    period_df.reset_index(inplace=True)

    # =对数据进行整理
    period_df.dropna(subset=['symbol'], inplace=True)
    period_df = period_df[period_df['_merge'] == 'both']
    del period_df['_merge']

    period_df.sort_values(by='candle_begin_time', inplace=True)
    period_df.reset_index(drop=True, inplace=True)

    return period_df
