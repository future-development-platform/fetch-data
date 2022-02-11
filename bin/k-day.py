#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
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
    if len (sys.argv) != 5:
        print ("请依次输入: 保存路径 股票名字 股票代码 当前时间\n"
                "时间格式为: YYYYMMDD")
        exit(-1)

    # 输入参数
    path = sys.argv[1]
    name = sys.argv[2]
    code = sys.argv[3]
    startDate = '1990-01-01'
    endDate = sys.argv[4]

    print ("开始获取 股票:{} --- {} 开始时间: {} 结束时间 {} 的所有数据 ...".format(name, code, startDate, endDate))

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
    outPath = path + "/" + name + ".csv"
    if os.path.exists(outPath):
        oldResult = pd.read_csv(outPath)
        if len(oldResult) == len(result):
            print ("数据已经最新!")
            exit(0)
    result.to_csv(outPath, index=False)

    bs.logout()
