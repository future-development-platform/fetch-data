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
    if len (sys.argv) != 3:
        print ("请依次输入: 股票代码  当前时间\n"
                "时间格式为: YYYYMMDD")
        exit(-1)

    # 输入参数
    code = sys.argv[1]
    startDate = '1990-01-01'
    endDate = sys.argv[2]

    print ("开始获取 股票: {} 开始时间: {} 结束时间 {} 的所有数据 ...".format(code, startDate, endDate))

    lg = bs.login()
    if not lg.error_code:
        print ("登录失败! 错误码: {}  错误信息: {}".format(lg.error_code, lg.error_msg))

    rs = bs.query_history_k_data_plus(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
            start_date=startDate, end_date=endDate, frequency="d", adjustflag="3")
    if not rs.error_code:
        print ("获取历史K线出错! 错误码: {}, 错误信息: {}".format(rs.error_code, rs.error_code))

    dataList = []
    while (rs.error_code == '0') & rs.next():
        dataList.append(rs.get_row_data())
    if len(dataList) <= 0:
        print ("股票: {} 开始时间: {} 结束时间 {} 的所有数据 不存在!!!".format(code, startDate, endDate))
        bs.logout()
        exit (0)
    result = pd.DataFrame(dataList, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv(code + ".csv", index=False)
    print(result)

    bs.logout()
