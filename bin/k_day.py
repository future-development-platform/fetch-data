#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import time
import baostock as bs
import pandas as pd

def fetch_k_data(startDate, endDate, code):
    rs = bs.query_history_k_data_plus(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
            start_date=startDate, end_date=endDate, frequency="d", adjustflag="3")
    if not rs.error_code:
        #print ("获取历史K线出错! 错误码: {}, 错误信息: {}".format(rs.error_code, rs.error_code))
        return None

    dataList = []
    while (rs.error_code == '0') & rs.next():
        dataList.append(rs.get_row_data())
    if len(dataList) <= 0:
        #print ("股票: {} 开始时间: {} 结束时间 {} 的所有数据 不存在!!!".format(code, startDate, endDate))
        return None
    result = pd.DataFrame(dataList, columns=rs.fields)

    return result


"""
输入参数如下:
    1. 时间
    2. 要拉取的股票代码:每行都是 key,value (key表示股票码,value表示名字)
    3. 保存目录
"""
def get_k_day (curDay, inPath, out):
    if not os.path.exists (inPath):
        return -1

    startDate = '1990-01-01'
    endDate = curDay

    lg = bs.login()
    if not lg.error_code:
        #print ("登录失败! 错误码: {}  错误信息: {}".format(lg.error_code, lg.error_msg))
        return -1

    with open (inPath, "r") as fr:
        for line in fr.readlines ():
            line = line.strip()
            arr = line.split(",")
            if len (arr) != 2:
                continue
            code = arr[0]
            name = arr[1]
            oldLen = 0
            outPath = out + "/" + code + ".csv"
            if os.path.exists (outPath):
                # 已存在，检测时间是否最新/获取数据是否为最新，最新则略过
                mtime = time.localtime(os.path.getmtime(outPath))
                mtimeFormat = time.strftime("%Y-%m-%d", mtime)
                if mtimeFormat == endDate:
                    continue
            df = fetch_k_data (startDate, endDate, code)
            if df is None:
                return -1
            df.to_csv(outPath, index=False)
    bs.logout()
