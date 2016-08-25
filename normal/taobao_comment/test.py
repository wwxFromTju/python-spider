# -*- coding: utf-8 -*-
import sys
import requests
import json
import re

url = r'https://rate.taobao.com/feedRateList.htm?callback=jsonp_reviews_list&user' \
      r'NumId=357648797&auctionNumId=529712214111&siteID=1&currentPageNum=1&rateType' \
      r'=&orderType=sort_weight&showContent=1&attribute='

cont=str(requests.get(url).content, 'utf-8')
rex=re.compile(r'\w+[(]{1}(.*)[)]{1}')
content=rex.findall(cont)[0]
print(cont)
con=json.loads(content)
count=len(con['rateDetail']['rateList'])
print("start")
for i in range(count):
    print(con['rateDetail']['rateList'][i]['appendComment']['content'])

print("end")