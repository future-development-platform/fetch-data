#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys

"""
根据输入文件生成shell中的字典
    1. 输入文件名: 股票名,股票码     ---     这种格式
    2. 股票码之前要加的前缀
    3. 输出名字前缀: xxx-
    4. 输出文件名: 一般为 xxx.sh
"""
if __name__ == '__main__':
    if len (sys.argv) != 5:
        print ("输入参数错误!")
        exit(-1)

    inPath = sys.argv[1]
    prex = sys.argv[2]
    namePrex = sys.argv[3]
    outPath = sys.argv[4]

    if not os.path.exists (inPath):
        print ("'{}' 不存在".format(inPath))
        exit(-1)

    if namePrex.endswith('-'):
        namePrex = namePrex[:-1]

    if prex.endswith('.'):
        prex = prex[:-1]

    with open (outPath, 'w+') as fw:
        fw.write ("#!/bin/bash\n")
        fw.write ("\n")
        fw.write ("declare -A stock_{}\n".format(prex))
        fw.write ("\n")
        fw.write ("stock_{}=(\n".format(prex))
        with open (inPath, 'r') as fr:
            for line in fr.readlines():
                line = line.strip()
                arr = line.split(',')
                if len(arr) != 2:
                    continue
                if not arr[1].isdigit():
                    continue 
                code = arr[1]
                name = arr[0].replace(' ', '')
                name = name.replace('\t', '')
                fw.write ("    ['{}.{}']='{}-{}'\n".format(prex, code, namePrex, name))
        fw.write (")\n")
