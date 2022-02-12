#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys

"""
根据输入文件生成shell中的字典
    1. 输入文件名: 股票名,股票码     ---     这种格式
    2. 股票码之前要加的前缀
    3. 股票名字前加的前缀
    4. 输出文件名
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

    if prex.endswith('.'):
        prex = prex[:-1]

    if namePrex.endswith('-'):
        namePrex = namePrex[:-1]

    with open (outPath, 'w+') as fw:
        with open (inPath, 'r') as fr:
            for line in fr.readlines():
                line = line.strip()
                arr = line.split(',')
                if len(arr) != 2:
                    continue
                code = arr[0]
                name = arr[1].replace(' ', '')
                name = name.replace('\t', '')
                if not code.isdigit():
                    continue 
                fw.write ("{}.{},{}-{}\n".format(prex, code, namePrex, name))
    exit(0)


