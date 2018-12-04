# -*- coding:utf-8 -*-

import time
import re
import numpy as np

def outPutMsg(filePath,content):
    with open(filePath, 'a', encoding='utf-8') as f:
        f.write(content)



'''读文件，按行遍历'''
def readline(filePath,writeFile):
    with open(filePath, 'r', encoding='utf-8') as f:
        while True:
            catchLine = '-99'
            line = f.readline()
            line = line.strip('\n')
            if line == catchLine:
                print('出现重复：')
                print('上一条：')
                print(str(catchLine))
                print('本条：')
                print(str(line))
                continue
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break
            newLine = dealWith_Msg(line)
            outPutMsg(writeFile,newLine)
            catchLine = line

'''文件行处理方法'''
def dealWith_Msg(line):
    _mark = ','
    print(str(line))
    newLine = ''
    line_split = splitString(line, '|')

    try:
        print(str(line_split[1]))
        print(str(line_split[3]))
        print(str(line_split[5]))
        print(str(line_split[6]))
        print(str(line_split[7]))

        newLine = line_split[3]+_mark+line_split[1]+_mark+line_split[5]+_mark+line_split[6]+'-'+line_split[7]+'\n'
        newLine = str(newLine).replace(' ','').replace('[','').replace(']','')
        print(newLine)
        return newLine
    except IndexError as e :
        print('异常行IndexError，写入异常文件')
        #outPutMsg('D:\learnPython\spider_man\\file\\exc.txt', str(line) + '\n')
        return ''
    except UnicodeEncodeError as e2 :
        print('异常行UnicodeEncodeError，写入异常文件')
        #outPutMsg('D:\learnPython\spider_man\\file\\exc.txt', str(line) + '\n')
        return ''



def splitString(data,splitFlag):
    return str(data).split(splitFlag)


if __name__ == '__main__':
    ti = time.time()

    readFile = 'E:\个人文档\头条号运营\房天下\新房\\newhouse.txt'
    writeFile = 'E:\个人文档\头条号运营\房天下\新房\\newhouse_v2.txt'
    readline(readFile,writeFile)

    print('耗时：' + str(time.time() - ti) + '，统计完成')

