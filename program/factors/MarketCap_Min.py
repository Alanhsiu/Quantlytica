"""
自建指数 | guy@quantlytica.com | quantlytica academy
author: guy@quantlytica.com
https://line.me/ti/p/YW0zkjxnxT
"""


def signal(*args):
    df = args[0]
    n = args[1][0]
    factor_name = args[2]

    df[factor_name] = df['quote_volume'].rolling(n, min_periods=1).mean()

    return df


def get_parameter():
    param_list = []
    n_list = [3, 5, 7, 8, 10, 13, 21, 34,55,144]
    for n in n_list:
        param_list.append([n])

    return param_list
