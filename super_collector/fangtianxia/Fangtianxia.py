# -*- coding: utf-8 -*-#

# Name:         Fangtianxia.py
# Author:       jiaocheng
# Date:         2018/11/19
# Description:  房天下新房 二手房 租房
import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import time
from super_collector.browser.ChromeBrowser import ChromeBrowser
from super_collector.utils.Utils_File import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class Zufang(object):

    start_url='http://xian.zu.fang.com/'

    '''抓取数据的步骤： 
    1启动浏览器备用 
    2发送requests请求 
    3第二步请求失败后抛异常，捕获异常调用浏览器进行请求 
    4分别获取区域，价格，户型层级嵌套的URL
    5过滤URL，判断筛选条件是否有结果
    6请求过滤后的URL链接，并处理分页问题
    7页面解析过程中捕获异常并跳过本条解析逻辑，执行下一条，将错误数据打印文件输出
    '''

    def __init__(self):
        self.browser = ChromeBrowser()
        self.browser.startBrowser() #优化点： 浏览器的启动可以写成单例模式，用到的时候在启动

    def getArea(self):
        responseCon = requests.get(self.start_url, headers=self.browser.header, timeout=50)
        soup = BeautifulSoup(responseCon.content, 'lxml')
        dl = soup.find(id='rentid_D04_01')
        dd = dl.find('dd')
        a_List = dd.find_all('a')
        areaName = re.findall(r'/">(.+?)</a>', str(a_List))
        areaUrl = re.findall(r'<a href="(.+?)">', str(a_List))
        return areaName,areaUrl

    def getMoney(self,url):
        try:
            #time.sleep(2)
            url = 'http://xian.zu.fang.com'+str(url)
            responseCon = requests.get(url, headers=self.browser.header, timeout=50)
            soup = BeautifulSoup(responseCon.content, 'lxml')
            dl = soup.find(id='rentid_D04_02')
            dd = dl.find('dd')
            a_List = dd.find_all('a')
            #print(str(a_List))
            moneyName = re.findall(r'rel="nofollow">(.+?)</a>', str(a_List))
            moneyUrl = re.findall(r'href="(.+?)" rel', str(a_List))
            del moneyName[0]
            del moneyUrl[0]
            print(str(moneyName))
            print(str(moneyUrl))
            return moneyName, moneyUrl
        except:
            return

    def getMeoney_chengdong(self,url):
        try:
            url = 'http://xian.zu.fang.com'+str(url)
            self.driver = self.browser.firstRequest(url)
            print(self.driver.page_source)
            #responseCon = requests.get(url, headers=self.browser.header, timeout=50)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            print(str(soup))
            dl = soup.find(id='rentid_D04_02')
            dd = dl.find('dd')
            a_List = dd.find_all('a')
            print(str(a_List))
            moneyName = re.findall(r'rel="nofollow">(.+?)</a>', str(a_List))
            moneyUrl = re.findall(r'href="(.+?)" rel', str(a_List))
            del moneyName[0]
            del moneyUrl[0]
            print(str(moneyName))
            print(str(moneyUrl))
            return moneyName, moneyUrl
        except:
            return



    def getchengdong_way(self,url):
        time.sleep(1)
        url = 'http://xian.zu.fang.com'+str(url)
        self.driver = self.browser.firstRequest(url)
        print(self.driver.page_source)
        #responseCon = requests.get(url, headers=self.browser.header, timeout=50)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        dl = soup.find(id='rentid_D04_03')
        dd = dl.find('dd')
        a_List = dd.find_all('a')
        #print(str(a_List))
        wayName = re.findall(r'rel="nofollow">(.+?)</a>', str(a_List))
        wayUrl = re.findall(r'href="(.+?)" rel', str(a_List))
        del wayName[0]
        del wayUrl[0]
        print(str(wayName))
        print(str(wayUrl))

        return wayName, wayUrl

    def getWay(self,url):
        time.sleep(1)
        url = 'http://xian.zu.fang.com' + str(url)
        responseCon = requests.get(url, headers=self.browser.header, timeout=50)
        soup = BeautifulSoup(responseCon.content, 'lxml')
        dl = soup.find(id='rentid_D04_03')
        dd = dl.find('dd')
        a_List = dd.find_all('a')
        # print(str(a_List))
        wayName = re.findall(r'rel="nofollow">(.+?)</a>', str(a_List))
        wayUrl = re.findall(r'href="(.+?)" rel', str(a_List))
        del wayName[0]
        del wayUrl[0]
        # print(str(wayName))
        # print(str(wayUrl))
        return wayName, wayUrl


    def getUrl_List(self,filename):
        allNameList = []
        allUrlList = []
        areaName, areaUrl = self.getArea()
        for i in range(len(areaUrl)):
            print('url_list==============',str(areaName[i]),str(areaUrl[i]))
            try:
                moneyName, moneyUrl = self.getMoney(areaUrl[i])
            except:
                print('url调用失败，用浏览器调用')
                moneyName, moneyUrl = self.getMeoney_chengdong(areaUrl[i])

            for money in range(len(moneyUrl)):
                #print(str(moneyName[money]))
                print('url_list==============', str(moneyName[money]))
                try:
                    wayName, wayUrl = self.getWay(moneyUrl[money])
                except:
                    print('url调用失败，用浏览器调用')
                    wayName, wayUrl = self.getchengdong_way(moneyUrl[money])
                for way in range(len(wayUrl)):
                    #print(wayUrl[way])
                    print(str(areaName[i]),str(moneyName[money]),wayName[way])
                    allNameList.append(str(areaName[i]) + ',' + str(moneyName[money]) + ',' + str(wayName[way]))
                    allUrlList.append('http://xian.zu.fang.com'+str(wayUrl[way]))
                    line = str(areaName[i]) + ',' + str(moneyName[money]) + ',' + str(wayName[way]) + ',' + 'http://xian.zu.fang.com'+str(wayUrl[way])+'\n'
                    outPutMsg(filename, str(line))

        return allNameList,allUrlList

    def judgeDetail(self,soup):
        p = soup.find(class_='not_find_note')
        span = re.findall(r'<span>(.+?)</span>', str(p))
        if span != []:
            print(str(span[0]))
            return False
        else:
            return True

    def analysis_dd(self, dd,data):
        try:
            #print(str(dd))
            mt = re.findall(r'<a data_channel="1,2" href="(.+?)"', str(dd))
            if mt == []:
                mt = re.findall(r'<a href="(.+?)" target', str(dd))
            title = re.findall(r'title="(.+?)">', str(dd))
            bold = re.findall(r'class="font15 mt12 bold">(.+?)<span class="splitline">\|</span>(.+?)<span class="splitline">\|</span>(.+?)<span class="splitline">\|</span>(.+?)</p>',str(dd), re.S)
            gray6_mt12 = re.findall(r'class="gray6 mt12" id="(.+?)">(.+?)<a href="(.+?)" target="_blank"><span>(.+?)</span></a>(.+?)<a href="(.+?)" target="_blank"><span>(.+?)</span>',str(dd), re.S)
            #gray6_mt12 = re.findall(r'<p class="gray6 mt12" (.+?)</p>', str(dd))
            price = re.findall(r'<span class="price">(.+?)</span>(.+?)</p>', str(dd))
            weizhi = re.findall(r'class="mt12"><span class="note subInfor">(.+?)<a href="(.+?)">(.+?)</a>(.+?)</span>', str(dd))
            case = str(bold[0][0]).replace('\\n','').strip()+'|'+str(bold[0][1])+'|'+str(bold[0][2])+'|'+str(bold[0][3]).replace('\\n','').strip()
            address = str(gray6_mt12[0][1]).replace('-','')+'|'+str(gray6_mt12[0][3])+'|'+str(gray6_mt12[0][6])
            prices = str(price[0][0])+'|'+str(price[0][1])
            # print(str(mt[0]))
            # print(str(title[0]))
            # #print(str(bold[0]))
            # print(str(case))
            # #print(str(gray6_mt12[0]))
            # print(str(address))
            # print(str(prices))
            if weizhi != []:
                weizhis = str(weizhi[0][0])+'|'+str(weizhi[0][2])+'|'+str(weizhi[0][3]).replace('。','')
            else:
                weizhis = '没有地铁线|木有啊|没有距离'

            line = 'http://xian.zu.fang.com' +str(mt[0])+ '|' + str(data) + '|' + str(title[0]) + '|' + str(case) + '|' + str(address) + '|' + str(prices) + '|' + str(weizhis)+'\n'
            print(str(line))
            outPutMsg('D:\learnPython\super_collector\\file\\zu_fang3.txt',str(line))
        except IndexError as e:
            print('解析错误：',e)
            wirteMsg('error put：'+str(mt))
            print("=========================")
            print("=========================",str(mt))
            print("=========================")



    def getMsgList(self,soup,data):
        div = soup.find(class_='houseList')
        print('==============================')
        dl = div.find_all('dl')
        for i in range(len(dl)):
            if dl[i].find('h3'):
                continue
            dd = dl[i].find_all('dd')
            self.analysis_dd(dd,data)




    def getDetail(self,url,data):
        time.sleep(1)
        self.driver = self.browser.firstRequest(url)
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gray6')))
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        #print(str(soup))
        if self.judgeDetail(soup):
            self.getMsgList(soup,data)
        else:
            '''url写入文件'''
            print('无数据')
            wirteMsg(str(url))
        div = soup.find(class_='fanye')
        #print(str(div))
        strss = re.findall(r'<a href="(.+?)">(.+?)</a>', str(div))
        print(str(len(strss)))
        aa = re.search(r'下一页', str(strss))
        #print(aa)
        if aa != None:
            nexts_url = self.getNextUrl(strss)
            #print(str(nexts_url))
            return nexts_url
        else:
            return None

    def getNextUrl(self,list):
        for i in range(len(list)):
            if str(list[i][1]) == '下一页':
                return 'http://xian.zu.fang.com'+list[i][0]





    def run(self,path):
        print('开始')
        '''1 遍历区域位置 2 遍历租金 3 遍历租房方式 4 判断url显示的内容是否为空 5 遍历url进行浏览器查询，点击下一页'''
        #allNameList, allUrlList = self.getUrl_List(path)
        allUrlList = getUrlFile('D:\learnPython\super_collector\\file\\fang_url3.txt')
        for i in range(len(allUrlList)):
            url = str(allUrlList[i]).split(',')[3]
            datastr = str(allUrlList[i]).split(',')[0] + '|' + str(allUrlList[i]).split(',')[1] + '|' + str(allUrlList[i]).split(',')[2]
            print('---------------第',i+1,'条',str(allUrlList[i]))
            mark = self.getDetail(url,datastr)
            j = 1
            while mark != None:
                print('下一页+' + str(j) + '++++++++++++++++', str(mark))
                mark = self.getDetail(mark, datastr)
                j = j +1
        self.browser.closeBrowser()



if __name__ == '__main__':

    zufang = Zufang()
    #zufang.getMeoney_chengdong('/house-a0479/')
    #zufang.getUrl_List('D:\learnPython\super_collector\\file\\fang_url.txt')
    #zufang.getDetail('http://xian.zu.fang.com/house-a0482/c2500-d21000-g21/')
    zufang.run('D:\learnPython\super_collector\\file\\fang_url3.txt')







