#!/usr/bin/env python
# encoding=utf-8

import sys
import requests
import json
import re

url = r'https://rate.taobao.com/feedRateList.htm?callback=jsonp_reviews_list&user' \
      r'NumId=357648797&auctionNumId=529712214111&siteID=1&currentPageNum=1&rateType' \
      r'=&orderType=sort_weight&showContent=1&attribute='

print(url)

content = requests.get(url).content.decode("GBK")
rex=re.compile(r'\w+[(]{1}(.*)[)]{1}')
content=rex.findall(content)[0]
con=json.loads(content, "GBK")
print(con)
count=len(con['comments'])
print("start")
for i in range(count):
      print(con['comments'][i]['content'])

print("end")