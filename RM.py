#!/usr/bin/python
# coding:utf-8

import re
import requests
from bs4 import BeautifulSoup


def getHtml(urlStr):
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
    req = requests.get(urlStr, headers=ua)
    req.raise_for_status()
    return req.text


def printBili(soup):
    src = soup.find('iframe')
    print(u'   Bilibili-Link: http:%s' % src['src'])


def printBaidu(soup):
    baiduSrc = soup.find_all('a', href=re.compile("https://pan\.baidu\.com/s/.*"))
    pattern = re.compile(u'提取码 ([a-zA-Z0-9]{4})')
    txt = soup.select('div[class="part"]')[-1].get_text()
    password = pattern.findall(txt)
    for n in range(len(baiduSrc)):
        print(u"   Baidupan-Link：%s Code：%s" % (baiduSrc[n]['href'], password[n]))


def rm(num=1):
    html = getHtml("http://www.hanfan.cc/tag/runningman/")
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', title=re.compile('.*Running Man E.*'))
    for n in range(num):
        html = getHtml(links[n]['href'])
        print(u'%d. [%s]' % (n + 1, links[n].get_text()))
        soup = BeautifulSoup(html, 'html.parser')
        printBili(soup)
        printBaidu(soup)


if __name__ == '__main__':
    rm(3)
