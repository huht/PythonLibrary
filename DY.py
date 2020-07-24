#!/usr/bin/python
# coding: utf-8

import time
import random
import requests
from bs4 import BeautifulSoup


def getHtml(urlStr):
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
    req = requests.get(urlStr, headers=ua)
    req.raise_for_status()
    return req.text


def douyu(url, num=5):
    html = getHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    authors = soup.find_all('h2', class_='DyListCover-user')
    titles = soup.find_all('h3', class_='DyListCover-intro')
    hots = soup.find_all('span', class_='DyListCover-hot')
    res = []
    for i in range(num):
        try:
            res.append(u"主播: %s(热度:%s) - 直播间标题: %s" % (authors[i].get_text(), hots[i].get_text(), titles[i].get_text()))
        except Exception as e:
            print e
    return res


def getAllGroups():
    html = getHtml("https://www.douyu.com/directory")
    soup = BeautifulSoup(html, 'html.parser')
    groups = soup.find_all('a', class_='layout-Classify-card')
    res = []
    for group in groups:
        name = group['href']
        title = group.strong.get_text()
        if name.strip() != '':
            if name not in res:
                res.append([name, title])
    return res


def allGroupsTop(num):
    groups = getAllGroups()
    for group in groups:
        print(u"斗鱼-%s主播TOP%d:" % (group[1], num))
        res = douyu(url="https://www.douyu.com%s" % group[0], num=num)
        for r in res:
            print(r)
        time.sleep(random.randrange(2, 10, 2))


def mszb(n):
    print(u"斗鱼-魔兽争霸主播TOP%d:" % n)
    res = douyu(num=n, url="https://www.douyu.com/g_mszb")
    for r in res:
        print(r)


def hots(n):
    print(u"斗鱼-风暴英雄主播TOP%d:" % n)
    res = douyu(num=n, url="https://www.douyu.com/g_HOTS")
    for r in res:
        print(r)


if __name__ == "__main__":
    mszb(5)
    hots(5)
    #allGroupsTop(3)
    # print(getHtml("https://www.douyu.com/infiwang"))
