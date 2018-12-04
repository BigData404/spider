# -*- coding:utf-8 -*-
from selenium import webdriver
from super_collector.browser.scrapping_helper import get_user_agent
from selenium.webdriver.common.action_chains import ActionChains
import os
import requests
import json

'''
浏览器的父类， 提供启动浏览器 关闭浏览器的方法
1 抽象方法
  a 打开浏览器  b 请求url地址  c 关闭浏览器
  获取浏览器user_agent
  获取浏览器session
  获取浏览器header
  改变浏览器header
  浏览器get请求
  浏览器post请求
  浏览器session级别get请求
  浏览器session级别post请求
  浏览器超时设置
  通过id 或者 class 查找固定标签的内容
  

'''
'''浏览器驱动最后 抽取到配置文件中'''

class ChromeBrowser(object):

    user_agent = None
    session = None
    header = None

    def __init__(self):
        self.user_agent = get_user_agent()
        self.session = requests.Session()
        self.header = {'User-Agent': self.user_agent}

    def getUser_agent(self):
        return self.user_agent

    def updateUser_agent(self):
        self.user_agent = get_user_agent()

    def startBrowser(self):
        print("start Chrome")
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=%s' % self.user_agent)
        chromedriver=os.path.dirname(os.path.realpath(__file__))+'\\chromedriver'
        self.driver = webdriver.Chrome(chromedriver, chrome_options=options)

    '''打开浏览器后第一次请求'''
    def firstRequest(self,url):
        self.driver.get(url)
        return self.driver

    '''关闭浏览器'''
    def closeBrowser(self):
        print("close Chrome")
        self.driver.close()

    '''登陆后写入session信息'''
    def setSession(self):
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
            #print(cookie['name'], cookie['value'])

    def updateHeader(self):
        self.header = {'User-Agent': self.updateUser_agent()}

    '''session级别请求，返回json'''
    def get_info_request(self, url):
        print(str(url))
        response = self.session.get(url, headers=self.header, timeout=50)
        return json.loads(response.text.strip("()"))

    '''点击按钮方法'''
    def clickbut(self,butten):
        ActionChains(self.driver).click(self.driver.find_element_by_id(butten)).perform()
        # return True

    '''session级别的post请求'''
    def post_request(self,url,payload,headerss):
        response = self.session.post(url, data=payload, headers=headerss, timeout=50)
        return json.loads(response.text.strip("()"))
















