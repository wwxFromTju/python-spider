#!/usr/bin/env python
# encoding=utf-8

import csv
import time

from selenium import webdriver
from bs4 import BeautifulSoup


def get_write_info(wechat_type, wechat_name):
    """关于get_write_info的说明

       wechat_type 代表类型：1 公众号，2 文章
       wechat_name 代表要找的关键字

       生成对应的名字为wechat_name+wechat_type的csv文件
       对应列为:
       图片URL 消息内容 发布时间 标题 点赞数 阅读数 公众号名 微信号

    """

    # 查询要使用的link type:2是文章 1是公众号， query是要搜索的具体内容
    url_base = u"http://weixin.sogou.com/weixin?type={0}&query={1}"

    # 启动selenium
    driver = webdriver.Firefox()
    driver.get(url_base.format(wechat_type, wechat_name))

    # 尽量不给对方服务器造成影响，每次请求之后都sleep 2s， 下同
    time.sleep(2)

    driver.find_element_by_xpath("//div[@class='wx-rb bg-blue wx-rb_v1 _item']").click()
    while len(driver.window_handles) == 1:
        pass

    # 切换到具体的公众号页面
    driver.switch_to_window(driver.window_handles[1])

    bsObj = BeautifulSoup(driver.page_source, 'lxml')

    with open(wechat_name + wechat_type + '.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)

        # items是外层的列表，代表一天
        # in_items为里面的具体信息，为一天里面具体发的信息
        items = len(bsObj.find_all('div', attrs={'class':'weui_msg_card_bd'}))
        in_items = [ len([i for i in bsObj.find_all('div', attrs={'class':'weui_msg_card_bd'})[i].children if i != '\n']) for i in range(items)]

        for i in range(items):
            for j in range(in_items[i]):
                # 跳转对应的文章
                driver.find_element_by_xpath("//div[@class='weui_msg_card_list']/div[{}]/div[@class='weui_msg_card_bd']/div[{}]".format(i+1, j+1)).click()

                time.sleep(2)

                # 获得文章的源码，之后解析
                page_resource = BeautifulSoup(driver.page_source, 'lxml')

                # 图片的url
                image_url = [i.get('data-src') for i in page_resource.find('div', attrs={'id': 'img-content'}).find_all('img') if
                i.get('data-src')]

                # 解析文字内容
                conte = page_resource.find('div', attrs={'class': 'rich_media_meta_list'}).next_sibling.next_sibling
                text_context = ''
                for string in conte.stripped_strings:
                    text_context += repr(string)

                # 发送时间
                send_time = page_resource.find('em', attrs={'id': 'post-date'}).text

                # 发送的标题
                send_title = page_resource.find('title').text

                # 点赞人数
                send_like = page_resource.find('span', attrs={'id': 'sg_likeNum3'}).text

                # 阅读人数
                send_read = page_resource.find('span', attrs={'id': 'sg_readNum3'}).text

                # 公众号
                send_post_user = page_resource.find('a', attrs={'id': 'post-user'}).text

                # 微信号
                send_id = page_resource.find('span', attrs={'class': 'profile_meta_value'}).text

                writer.writerow([image_url, text_context, send_time, send_title, send_like, send_read, send_post_user, send_id])

                driver.back()

    driver.quit()
