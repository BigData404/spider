# -*- coding:utf-8 -*-
import time
import requests
import re

def getUrlFile(path):
    with open(path, 'r',encoding='UTF-8') as f1:
        list1 = f1.readlines()
    return list1

def outPutMsg(filePath,content):
    with open(filePath, 'a', encoding='utf-8') as f:
        f.write(content)

def getGps(addressList):
    for i in range(0, len(addressList)):
        time.sleep(5)
        line = addressList[i].strip('\n')
        address = '西安市'+str(line).split(',')[0]+str(line).split(',')[1].strip()
        subway=str(line).split(',')[3]+'&tell:'+str(line).split(',')[2].strip()
        print('*****' + str(address))
        try:
            reqGps(str(address),subway)
        except:
            print(address)
            print('--------------------')
            continue

def reqGps(address,subway):

    url = 'https://apis.map.qq.com/jsapi'

    head={
        'Referer': 'http://www.gpsspg.com/iframe/maps/qq_161128.htm?mapi=2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    payload2 = {'qt': 'geoc',
                'addr': address,
                'key': 'FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS',
                'output': 'jsonp',
                'pf': 'jsapi',
                'ref': 'jsapi',
                'cb': 'qq.maps._svcb3.geocoder0'
                }

    login_req = requests.get(url, headers=head, params=payload2, timeout=50)
    #print(login_req.text)
    x = re.findall(r'pointx":"(.+?)"', str(login_req.text))
    y = re.findall(r'pointy":"(.+?)"', str(login_req.text))
    line = address+','+ x[0]+','+y[0]+','+str(subway)+'\n'
    print(str(line))
    outPutMsg('E:\个人文档\头条号运营\房天下\新房\\newhouse_Gps.txt',str(line))

if __name__ == '__main__':
    ti = time.time()
    getGps(getUrlFile('E:\个人文档\头条号运营\房天下\新房\\newhouse_v2.txt'))
    print('耗时：' + str(time.time() - ti) + '，统计完成')



