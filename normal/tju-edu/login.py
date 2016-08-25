#!/usr/bin/env python
# encoding=utf-8

import os
import requests
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image

# 头部, 避免被认为爬虫, 然而学校好像根本不管
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
}

# 登陆使用的URL
url_base = u"http://e.tju.edu.cn"
url_temp = url_base + "/Main/toModule.do?prefix=/Main&page=/logon.jsp"
url_login = url_base + "/Main/logon.do;jsessionid="
url_pic = url_base + "/Kaptcha.jpg"

# 不同学期的成绩
score_url_list = [u"http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=13141",
                  u"http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=13142",
                  u"http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=14151",
                  u"http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=14152",
                  u"http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=15161",
                  u"http://e.tju.edu.cn/Education/stuachv.do?todo=display&term=15162"
                  ]

# 登陆用户信息
params = {"uid": os.environ.get('tju_name'),
          "password": os.environ.get('tju_password')}

# 使用Session
session = requests.session()

# 主要目的是获得sessionid, 登陆的url中需要对应的sessionid
req = session.get(url_temp, headers=headers)

# 使用sessionid来拼接实际的登陆url
url_login = url_login + req.cookies.get_dict()["JSESSIONID"]

# 获得最后一个刷新的验证码, 同时保存下来
kaptcha = session.get(url_pic, headers=headers)
f = open("test.jpg", "wb")
f.write(kaptcha.content)
f.close()

# 使用pytesseract来识别验证码, 需要在本地安装tesseract
kaptcha = Image.open("test.jpg")
kaptcha_num = pytesseract.image_to_string(kaptcha);

# 将验证码输入到post的参数中
params["captchas"] = kaptcha_num;

# 发送请求, 登陆
post_login = session.post(url_login, params, headers=headers)

score_list = [session.get(url_score, headers=headers) for url_score in score_url_list]

bsObj = [BeautifulSoup(score_list_text.text, "lxml") for score_list_text in score_list]

print(bsObj)
