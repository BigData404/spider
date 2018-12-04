# -*- coding:utf-8 -*-


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


'''
class Browser(object):


    def startBrowser(self):
        raise Exception('startBrowser子类中必须实现该方法')

    def requestURL(self,url):
        raise Exception('requestURL 发出请求方法，子类中必须实现该方法')

    def closeBrowser(self):
        raise Exception('closeBrowser子类中必须实现该方法')



