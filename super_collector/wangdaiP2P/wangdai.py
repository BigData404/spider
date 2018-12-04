# coding=utf-8

import request
import re
import urllib
import sys
import importlib
import urllib
import time
import threading
from china_Judgement_Online.requestType import *
from china_Judgement_Online.general import *
import queue

que = queue.Queue()

global filePath
global exceptionFilePath

def operation(url):
    try:
        headers = {
            'User-Agent': get_user_agent(),
            'Referer': 'http://dailianmeng.com/p2pblacklist/index.html'
        }
        r = requests.get(url, headers=headers)
        print(r.text)
        return r.text
    except Exception as e:
        print('请求失败')
        print(e)

def gethtmlData(text):
    hrefText = re.findall(r'target="_blank" href="(.+?)"', text)
    return hrefText

def requestMore():
    global flag
    url_ajax = 'http://dailianmeng.com/p2pblacklist/index.html?P2pBlacklist_page=3&ajax=yw0'
    index = 2
    while True:
        if index > 164: break
        url = 'http://dailianmeng.com/p2pblacklist/index.html?P2pBlacklist_page='+index+'&ajax=yw0'
        print(url)
        hrefText = gethtmlData(operation(url))
        print(hrefText)
        getEndData(hrefText)
        index = index + 1
    flag = 0

def getEndData(hrefText):
    ths = []
    print('生产者开始启动，生产数据...')
    for index in range(len(hrefText)):
        sleeptime = random.uniform(2, 4)
        print('休息：', sleeptime, '秒')
        time.sleep(sleeptime)
        t = threading.Thread(target=get_Msg, name="生产者", args=(str(hrefText[index]),))
        t.start()
        ths.append(t)
    for th in ths:
        th.join()

def get_Msg(docID):
    url_index = 'http://dailianmeng.com'+str(docID)    # /p2pblacklist/view/QJJZ7v.html'
    global exceptionFilePath
    try:
        name = threading.current_thread().getName()
        time.sleep(1)
        r = operation(url_index)
        line = explain_waidai(r)
        print(name + "生产一个数据: ", line)
        que.put(line)
    except Exception as e:
        print('获取原文失败，保存docID' + docID)
        exceptionDocID(exceptionFilePath, docID + '\n')

def explain_waidai(r):
    hrefText = re.findall(r'yw0"\>(.+?)\<\/table', r)
    td = re.findall(r'td\>(.+?)\<\/td', r)
    print(str(td))
    return str(td)

def comsumer():
    c = threading.Thread(target=comsumer_worker, name="消费者")
    c.start()

def comsumer_worker():
    global flag
    global filePath
    print(filePath)
    flag = 1
    name = threading.current_thread().getName()
    print('消费者线程启动。。。')
    while True:
        if (que.empty() and flag==0):
            print('队列为空，消费者线程执行结束')
            break
        items = que.get()
        print(name+"消费一个数据: ",items)
        write_data_inFile(filePath,str(items))
    print('消费者线程注销...')


def initData():
    print('初始化参数配置')
    global filePath
    global exceptionFilePath
    filePath = 'D:\ppppp\网贷黑名单.txt'
    exceptionFilePath = 'D:\ppppp\贷黑名单.txt'



if __name__ == '__main__':
    '''一共 164 页'''
    url_a = 'http://dailianmeng.com/p2pblacklist/index.html?ajax=yw0'
    aa = operation(url_a)
    hrefText = gethtmlData(aa)
    print(hrefText)
    getEndData(hrefText)






