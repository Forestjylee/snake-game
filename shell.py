import os
import json
import time
import pickle
import datetime
from snake import game
from prettytable import PrettyTable

default_setting_info = {
    'init_scores':0,
    'speed':20,
}

table = PrettyTable(["命令", "功能"])
table.add_row(["h/?", "帮助"])
table.add_row(["s/go", "开始游戏"])
table.add_row(["t", "托管模式"])
table.add_row(["set", "打开配置文件"])
table.add_row(["p", "排行榜"])

def save_setting(setting_info):
    with open("setting.txt", 'w') as f:
        json.dump(setting_info, f)

def load_setting():
    with open("setting.txt", 'r') as f:
        setting_info = json.load(f)
        return setting_info

def save_rank(scores, name, efficiency):
    rank_info = load_rank()
    with open('rank.pck', 'wb') as f:
        if not rank_info:
            rank_info = []
        info = {
            'name':name if name else '用户',
            'scores':scores,
            'efficiency':efficiency,
            'datetime':datetime.datetime.now(),
        }
        rank_info.append(info)
        pickle.dump(rank_info, f)

def load_rank():
    try:
        with open('rank.pck', 'rb') as f:
            rank_info = pickle.load(f)
            return rank_info
    except:
        return None

def shell():
    '''贪吃蛇控制台'''
    command = input("请输入命令>>")
    if command == 's' or command == 'go':
        setting_info = load_setting()
        print("游戏正在运行...")
        start_time = time.time()
        scores = game(init_scores=setting_info['init_scores'], speed=setting_info['speed'])
        end_time = time.time()
        efficiency = round(scores/(end_time-start_time),5)
        name = input("请输入您的名字:")
        save_rank(scores=scores, name=name, efficiency=efficiency)
    elif command == 'h' or command == '?' or command == '？':
        print(table)
    elif command == 'set':
        os.startfile("setting.txt")
    elif command == 'p':
        rank_info = load_rank()
        if not rank_info:
            return
        table2 = PrettyTable(["名字", "分数", "完成时间"])
        rank_info = sorted(rank_info, key=lambda x:-x['scores'])
        for info in rank_info:
            table2.add_row([info['name'], info['scores'], info['datetime']])
        print(table2)
        print('--------------------------------------------------')
        table3 = PrettyTable(["名字", "效率值", "完成时间"])
        rank_info = sorted(rank_info, key=lambda x:-x['efficiency'])
        for info in rank_info:
            table3.add_row([info['name'], info['efficiency'], info['datetime']])
        print(table3)
    elif command == 't':
        #TODO 托管
        pass

if __name__ == '__main__':
    print(table)
    while True:
        try:
            shell()
        except Exception as e:
            print(repr(e))
            print("出现未知错误")
            flag = input("是否恢复默认配置?\n  y.是    n.否\n>>")
            if flag == 'y' or flag == 'Y':
                save_setting(setting_info=default_setting_info)