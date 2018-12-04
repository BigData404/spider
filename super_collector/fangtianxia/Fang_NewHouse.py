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

class NewHouse(object):

    start_url='http://xian.newhouse.fang.com/'

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
        dl = soup.find(id='ax1')
        li = dl.find(id='quyu_name')
        a_List = li.find_all('a')
        areaList = re.findall(r'<a href="(.+?)">(.+?)</a>', str(a_List))
        return areaList

    def getArea_b(self):
        try:
            self.driver = self.browser.firstRequest(self.start_url)
            #print(self.driver.page_source)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            dl = soup.find(id='ax1')
            li = dl.find(id='quyu_name')
            a_List = li.find_all('a')
            areaList = re.findall(r'<a href="(.+?)">(.+?)</a>', str(a_List))
            return areaList
        except:
            return

    def getUrl_List(self,filename):
        allUrlList = []
        try:
            allUrlList = self.getArea()
        except:
            print('url调用失败，用浏览器调用')
            allUrlList = self.getArea_b()
        for i in range(len(allUrlList)):
            print('url_list==============', str(allUrlList[i]))
        return allUrlList

    def analysis_dd(self, dd,data):
        try:
            #dd = li[i].find_all(class_='nlc_details')
            name = str(dd.find_all(class_='nlcd_name')).replace('\n', '').replace('\t', '')
            #print(name)
            name2 = dd.find_all(class_='house_type clearfix')
            # print(str(name2))
            name34 = dd.find_all(class_='address')
            #print(str(name34))
            name3 = str(name34).replace('\n', '').replace('\t', '')
            #print('$$$$$$$$$$' + str(name3))
            name4 = dd.find_all(class_='tel')
            # print(str(name4))
            name5 = dd.find_all(class_='nhouse_price')
            #print(str(name5))
            mt = re.findall(r'<a href="(.+?)" target="_blank">(.+?)</a>', str(name), re.S)
            # # if mt == []:
            # #     mt = re.findall(r'<a href="(.+?)" target', str(dd))
            title = re.findall(r'<a href="(.+?)" target="_blank" title="(.+?)"><span class="sngrey">(.+?)</span>(.+?)</a>', str(name3), re.S)
            tell = re.findall(r'<p>(.+?)<span>(.+?)</span>(.+?)</p>', str(name4))
            z = re.findall(r'<span class="forSale">(.+?)</span>',str(dd))
            if z == []:
                z = re.findall(r'<span class="inSale">(.+?)</span>', str(dd))
            if z == []:
                z = re.findall(r'<span class="zusale">(.+?)</span>', str(dd))

            price = re.findall(r'<label>(.+?)</label><label>(.+?)</label><i>(.+?)</i><em>(.+?)</em>', str(name5))
            if price == []:
                price = re.findall(r'<span>(.+?)</span><em>(.+?)</em>', str(name5))
            if price == []:
                price = re.findall(r'<span style="font-size:20px;">(.+?)</span>', str(name5))

            if price == []: return

            # print(str(mt))
            # print(str(title))
            # print(str(tell))
            # print(str(z))
            # print(str(price))

            line = str(mt[0][0]) + '|' + str(mt[0][1]) + '|' + str(title[0][1]) + '|' + str(title[0][2]) + '|' + str(title[0][3]) + '|' + self.toString(tell[0], 0) + '|' + str(z[0]) + '|' + self.toString(price[0], 0)+ '\n'
            print('*************************')
            print(str(line))
            outPutMsg('D:\learnPython\super_collector\\file\\newhouse.txt',str(line))
        except IndexError as e:
            print('解析错误：',e)
            wirteMsg('error put：'+str(mt))
            # print("=========================")
            # print("=========================",str(mt))
            # print("=========================")
    def toString(self,data,flag):
        line = ''
        strr = data[flag:]
        for x in strr:
            line = line + str(x)
        print(line)
        return str(line)






    def getMsgList(self,soup,data):
        div = soup.find(class_='nhouse_list')
        print('==============================')
        li = div.find_all('li')
        #print(str(li))
        print(str(len(li)))
        for i in range(len(li)):
            if li[i].find('h3'):continue
            if li[i].text == '': continue
            self.analysis_dd(li[i], data)






    def getDetail(self,url,data):
        time.sleep(10)
        self.driver = self.browser.firstRequest(url)
        #print(str(self.driver.page_source))
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'main_1200')))
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        #print(str(soup))

        self.getMsgList(soup,data)

        div = soup.find(class_='page')
        nextpage = re.findall(r'<a class="next" href="(.+?)">(.+?)</a>',str(div))
        #nextpage = div.find(class_='next')
        #href = div.find(class_='next').href
        print('_____________________' + str(nextpage))

        if nextpage != []:
            nexts_url = 'http://xian.newhouse.fang.com'+str(nextpage[0][0])
            print(str(nexts_url))
            return nexts_url
        else:
            return None

    def run(self,path):
        print('开始')
        '''1 遍历区域位置 2 遍历租金 3 遍历租房方式 4 判断url显示的内容是否为空 5 遍历url进行浏览器查询，点击下一页'''
        allUrlList = self.getUrl_List(path)
        for i in range(len(allUrlList)):
            url = 'http://xian.newhouse.fang.com'+str(allUrlList[i][0])
            area = str(allUrlList[i][1])
            print('---------------第',i+1,'条',str(area),str(url))
            mark = self.getDetail(url,area)
            j = 1
            while mark != None:
                print('下一页+' + str(j) + '++++++++++++++++', str(mark))
                mark = self.getDetail(mark, area)
                j = j +1
        self.browser.closeBrowser()



if __name__ == '__main__':

    newHouse = NewHouse()
    #zufang.getMeoney_chengdong('/house-a0479/')
    #newHouse.getUrl_List('D:\learnPython\super_collector\\file\\fang_newHouse_url.txt')
    #zufang.getDetail('http://xian.zu.fang.com/house-a0482/c2500-d21000-g21/')
    newHouse.run('D:\learnPython\super_collector\\file\\fang_newHouse.txt')







