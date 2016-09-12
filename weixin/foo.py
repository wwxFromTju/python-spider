#!/usr/bin/env python
# encoding=utf-8

import threading
import os
import time
import csv

from test import get_write_info


find_info = {'金鹿公务': '1',
             '神秘的程序员们': '1',
             '小道消息': '1',
             '微软科技': '1',
             'Linux学习': '1',
             'TechWeb': '1',
             '果壳网': '1',
             '每日豆瓣': '1'}

# for name, type in find_info.items():
#     get_write_info(wechat_type='1', wechat_name='神秘的程序员们')

if __name__ == '__main__':
    waitfor = []

    for name, type in find_info.items():
        thread = threading.Thread(target=get_write_info, args=(type, name))
        thread.daemon = True
        thread.start()
        waitfor.append(thread)

    for thread in waitfor:
        thread.join()

    with open('totol' + str(time.time()) + '.csv', 'w', encoding='utf-8') as f_final:
        final = csv.writer(f_final)
        final.writerow(['图片URL', '消息内容', '发布时间', '标题', '点赞数', '阅读数', '公众号名', '微信号'])
        for name, type in find_info.items():
            if os.path.exists(name + type + '.csv'):
                with open(name + type + '.csv', 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for line in reader:
                        final.writerow(line)
                os.remove(name + type + '.csv')



