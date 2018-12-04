# -*- coding:utf-8 -*-

import requests
import re

def pachong(cardNo , prov):
    provName = ''
    try:
        url = 'http://www.cardcn.com/search.php?word=' + str(cardNo) + '&submit='
        """"""
        body = requests.get(url)
        name = re.findall(r'<dt><font class="con_sub_title">(.+?)</font>(.+?)</dt>', str(body.text))
        for msg in name:
            if msg[0] == '归属信息：':
                if msg[1] != '':
                    provName = msg[1]
                    #print(prov + ' == ' + msg[1])
                break
    except:
        provName = 'error'
    return provName

def randomZno(no , lens):
    z_len = lens - len(no)
    for num in range(1, z_len+1):
        no = '0' + no
    return no

def randomZno2(no , lens):
    z_len = lens - len(no)
    for num in range(1, z_len+1):
        no = no + '0'
    return no

def createCardNoZhaohang(fileName , cardBin , bankName , cardType , randomNum , provNumLen):
    errorFileName = 'D:\\kbin\\prov\\error.txt'
    errorFile = open(errorFileName, 'a+' ,encoding='UTF-8')
    filePath = 'D:\\kbin\\prov\\'
    maxLen = int(randomZno2('1',provNumLen+1))
    with open(filePath + fileName, 'a+' ,encoding='UTF-8') as f:
        for num in range(0, maxLen):
            no = str(num)
            prov = randomZno(no , provNumLen)
            t_num = cardBin + prov + randomNum
            provName = pachong(t_num , prov)
            line = cardBin + '\t' + bankName + '\t' + cardType + '\t' + prov + '\t' + provName + '\r\n'
            if provName != 'error':
                if provName != '':
                    print('msg ### '+line)
                    f.write(line)
            else:
                print('error ' +t_num+ ' ### ' + line)
                errorFile.write(line)

if __name__ == '__main__':
    provNumLen = 4
    filePath = 'D:\\kbin\\target\\'

    list = []
    list.append('other.txt')

    """
    list.append('youzheng.txt')
    list.append('zhonghang.txt')
    list.append('zhaoshang.txt')
    list.append('jianshe.txt')
    list.append('jiaotong.txt')
    list.append('nonghang.txt')
    """

    for fileName in list:
        for line in open(filePath + fileName, "r", encoding='UTF-8'):
            line = line.strip('\n')
            lines = line.split('\t')
            cardBin = lines[0]
            print('### ' + cardBin + ' start ...')
            bankName = lines[1]
            cardType = lines[3]
            numLen = lines[4]
            randomNum = randomZno('1', int(numLen) - provNumLen - len(cardBin))
            createCardNoZhaohang(fileName , cardBin, bankName, cardType, randomNum, provNumLen)
