#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
from k_day import get_k_day

"""
数据拉取主入口
    1. 当前时间: YYYY-MM-DD
    2. 拉取的数据类型: k-day
    3. 拉取键值对路径
    4. 保存路径
"""
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print ("输入参数错误!")
        exit(1)

    time = sys.argv[1]
    dataType = sys.argv[2]
    inpath = sys.argv[3]
    outdir = sys.argv[4]

    if "k-day" == dataType:
        get_k_day (time, inpath, outdir)

    exit (0)
