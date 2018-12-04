# -*- coding:utf-8 -*-

import requests
import re
from super_collector.utils.Utils import *
from super_collector.utils.Utils_File import *


import time


class BandCard_Bin(object):

    baseUrl = None
    outputPath = 'D:\hadoop_test\\'

    def __init__(self):
        self.dicts = {}
        self.baseUrl = getConfig('bankcardbin', 'baseUrl')
        self.dicts['icbc'] = str(getConfig('bankcardbin', 'icbcUrl'))
        self.dicts['jiaotong'] = str(getConfig('bankcardbin', 'jiaotongUrl'))
        self.dicts['jianshe'] = str(getConfig('bankcardbin', 'jiansheUrl'))
        self.dicts['zhonghang'] = str(getConfig('bankcardbin', 'zhonghang'))
        self.dicts['zhaoshang'] = str(getConfig('bankcardbin', 'zhaoshang'))
        self.dicts['youzheng'] = str(getConfig('bankcardbin', 'youzheng'))
        self.dicts['nonghang'] = str(getConfig('bankcardbin', 'nonghang'))
        self.dicts['other'] = str(getConfig('bankcardbin', 'other'))

    def run(self):

        for key, value in self.dicts.items():
            print(key, ' value : ', value)
            self.filePath = self.outputPath + key + '.txt'
            r = requests.get(value)
            # print(r.text)
            self.childUrlList = re.findall(r'href=\'(.+?)\'', str(r.text))
            print(str(self.childUrlList))
            print(str(len(self.childUrlList)))
            lst = self.getDetail()
            if lst == []:
                continue
            else:
                self.childUrlList = lst
                self.getDetail()



    def getDetail(self):
        errorList = []
        for curl in range(len(self.childUrlList)):
            time.sleep(1)
            try:
                ch_url = self.baseUrl + self.childUrlList[curl]
                print(str(ch_url))
                headers = {
                    "User-Agent": get_user_agent()
                }
                requests.get(ch_url, headers=headers, timeout=50)
                child_r = requests.get(ch_url)
                child_r.encoding = 'gb2312'
                # print(child_r.text)
                name = re.findall(r'<h1>银行卡BIN：(.+?)</h1>', str(child_r.text))
                card_msg = re.findall(r'<p>(.+?)</p>', str(child_r.text))
                # print(name)
                # print(card_msg)
                cardName = re.findall(r'是(.+)', str(card_msg[0]))
                cardType = re.findall(r'类型是(.+)', str(card_msg[1]))
                cardCount = re.findall(r'卡号数字长度为(.+?)位 如', str(card_msg[2]))
                # print(str(cardName))
                # print(str(cardType))
                # print(str(cardCount))
                if '借记卡' in str(cardType):
                    num = 1
                elif '贷记卡' in str(cardType):
                    num = 2
                else:
                    num = 3
                content = str(name[0]) + ',' + str(cardName[0]) + ',' + str(cardType[0]) + ',' +str(num)+ ',' + str(cardCount[0]) + '\n'
                print(str(content))
                outPutMsg(self.filePath,str(content))
            except:
                print(self.childUrlList[curl],'写入错误文件')
                errorList.append(self.childUrlList[curl])
        return errorList




if __name__ == '__main__':
    bankcard = BandCard_Bin()
    bankcard.run()





