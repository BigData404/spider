
import random
import os

def get_user_agent():
    user_agent_list = []
    filePath=os.path.dirname(os.path.realpath(__file__))+'\\user_agent_chrome_no_mobile.txt'
    print(filePath)
    f = open(filePath, 'r')
    for date_line in f:
        user_agent_list.append(date_line.replace('\n', ''))
    user_agent = random.choice(user_agent_list)
    f.close()
    return user_agent
