#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import baostock as bs
import pandas as pd

"""
输入参数如下:
    1. 股票代码
    2. 起始时间
    3. 当前时间
"""
if __name__ == '__main__':
    if len (sys.argv) != 4:
        print ("请依次输入: 股票代码  起始时间  当前时间\n"
                "时间格式为: YYYY-MM-DD")
        exit(-1)

    # 输入参数
    code = sys.argv[1]
    startDate = sys.argv[2]
    endDate = sys.argv[3]

    print ("开始获取 股票: {} 开始时间: {} 结束时间 {} 的所有数据 ...".format(code, startDate, endDate))

    lg = bs.login()
    if not lg.error_code:
        print ("登录失败! 错误码: {}  错误信息: {}".format(lg.error_code, lg.error_msg))

    rs = bs.query_history_k_data_plus(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
            start_date=startDate, end_date=endDate, frequency="d", adjustflag="3")
    if not rs.error_code:
        print ("获取历史K线出错! 错误码: {}, 错误信息: {}".format(rs.error_code, rs.error_code))

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("aa.csv", index=False)
    print(result)

    bs.logout()
