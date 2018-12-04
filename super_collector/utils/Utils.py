# -*- coding: utf-8 -*-#

# Name:         Utils.py
# Author:       jiaocheng
# Date:         2018/12/3
# Description:

import configparser
import random
import os

proDir = os.path.dirname(os.path.realpath(__file__))

def iteratorDict(data,josn_info):
    list = {}
    for key, value in data.items():
        print(str(key) + ':' + str(value))
        josn_info[key] = str(value)
        if type(value) == dict:
            iteratorDict(value, josn_info)
        else:
            list[str(key)]=str(value)
    return list

def getConfig(name1,name2):

    configPath = os.path.join(proDir, "utilConfig.ini")
    path = os.path.abspath(configPath)
    Config = configparser.ConfigParser()
    Config.read(path)
    return Config.get(name1, name2)


def get_user_agent():
    configPath = os.path.join(proDir, "user_agent.txt")
    user_agent_list = []
    f = open(configPath, 'r')
    for date_line in f:
        user_agent_list.append(date_line.replace('\n', ''))
    user_agent = random.choice(user_agent_list)
    return user_agent


if __name__ == '__main__':
    s = getConfig('bankcardbin','icbcUrl')
    print(str(s))

