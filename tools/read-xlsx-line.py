#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import pandas as pd

"""
输入参数:
    1. 文件名 .xlsx
    2. sheet 名字
    3. 提取字段,以逗号区分
    4. 输出文件 .txt
"""
if __name__ == '__main__':
    if len (sys.argv) != 5:
        print ("输入参数错误")
        exit(0)

    inPath = sys.argv[1]
    sheetName = sys.argv[2]
    filds = sys.argv[3]
    outPath = sys.argv[4]

    fildList = filds.split(',')
    if len(fildList) <= 0:
        print ("参数不正确")
        exit(0)

    if not os.path.exists (inPath):
        print ("路径 '{}' 不存在!".format(inPath))
        exit(0)

    df = pd.read_excel(inPath, sheet_name=sheetName, dtype=str)
    if len(df) <= 0:
        print ("读取 {} 错误!".format (inPath))
        exit(0)

    dfilds = {}
    for k in fildList:
        if k in df:
            dfilds[k] = df[k]
        else:
            print ("'{}'字段不存在于 {} 文件的 {} sheet 中!", k, inPath, sheetName)

    if len(dfilds) <= 0:
        print ("没有从 '{}' 文件的 '{}' 表中抽取到任何字段".format(inPath, sheetName))
        exit(0)

    # 重新输出
    outdf = None
    for ik in dfilds:
        outdf = pd.concat([outdf,dfilds[ik]], axis=1)

    if None is not outdf:
        outdf.to_csv (outPath, index=False)
        print ("输出路径: {}".format(outPath))
