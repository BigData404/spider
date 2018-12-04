# -*- coding: utf-8 -*-#

# Name:         Utils_File.py
# Author:       jiaocheng
# Date:         2018/11/19
# Description:


import time
import re
import os

'''判断文件是否存在'''
def is_exist(filePath):
    return os.path.exists(filePath)

'''判断文件夹是否存在,不存在就创建'''
def is_exist_andCreatePath(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        return True

'''写文件'''
def outPutMsg(filePath, content):
    with open(filePath, 'a', encoding='utf-8') as f:
        f.write(content)

'''写文件'''
def wirteMsg(msg):
    f = open('D:\learnPython\super_collector\\file\\empty_newhouse.txt', 'a', encoding='utf-8')
    f.write(msg)
    f.close()

def getUrlFile(path):
    with open(path, 'r',encoding='UTF-8') as f1:
        list1 = f1.readlines()
    return list1

def splitString(data, splitFlag):
    return str(data).split(splitFlag)

def reFind():
    a = "[('/house-a0482/c2500-d21000-g21/', '首页'), ('/house-a0482/c2500-d21000-g21-i32/', '2'), ('/house-a0482/c2500-d21000-g21-i33/', '3'), ('/house-a0482/c2500-d21000-g21-i32/', '下一页'), ('/house-a0482/c2500-d21000-g21-i33/', '末页')]"

    nexts = re.findall(r'<a href="(.+?)">下一页', str(a))
    print(nexts)







if __name__ == '__main__':
    ti = time.time()
    tup2 = (1, 2, 3, 4, 5, 6, 7)
    print(tup2[0:])
    # readFile = 'D:\learnPython\spider_man\\file\\msgAA.txt'
    # writeFile = 'D:\learnPython\spider_man\\file\\endData.txt'
    # readline(readFile,writeFile)

    print('耗时：' + str(time.time() - ti) + '，统计完成')