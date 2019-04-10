# -*- coding:utf-8 -*-

"""
@#: 页面： main
@#：URL : http://navi.cnki.net/KNavi/All.html
@#: 时间： 2019/2/19
@#: 作者： Mr.L
"""
from selenium import webdriver  # 从selenium导入webdriver
from bs4 import BeautifulSoup
from core.navigation import subject_navigation
from selenium.webdriver.common.action_chains import ActionChains


def main():
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get("http://navi.cnki.net/KNavi/All.html")  # 获取百度页面

    qqq = driver.find_element_by_xpath("//ul[@class='contentbox']/li[1]/dl/dd[1]/a")
    # 对定位到的元素执行鼠标右键操作
    # ActionChains(driver).click(qqq)

    driver.execute_script(
        "document.getElementsByClassName('contentbox').onclick = Submit.naviSearch('1','专题子栏目代码','A001','自然科学理论与方法');",
        qqq)
    import time
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # print(soup)
    url = "http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=BJWD"
    driver.get(url)
    # -----<学科导航>----- #
    # subject_data = subject_navigation(soup)
    # print(subject_data)
    # 可以不用 + uid，已测试
    cookie = [(item["name"], item["value"]) for item in driver.get_cookies()]
    print(dict(cookie))

    driver.quit()
    # driver.close()

#!/usr/bin/env python
# encoding=utf-8

import requests

DOWNLOAD_URL = 'http://movie.douban.com/top250/'


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).text
    print(data)
    return data

def test_dev():
    code = \
        """
        <li class="">
        <em>[1]</em>
        <a target="kcmstarget" href="/kcms/detail/detail.aspx?filename=TJYJ201304021&amp;dbcode=CJFQ&amp;dbname=CJFD2013&amp;v=">单位根过程联合检验的Bootstrap研究</a>
        [J]. 陶长琪,江海峰.&nbsp;&nbsp;
        <a onclick="getKns55NaviLink('','CJFQ','CJFQbaseinfo','TJYJ');">统计研究</a>.
         <a onclick="getKns55NaviLinkIssue('','CJFQ','CJFQyearinfo','TJYJ','2013','04')">2013(04)
        </a></li>
        """
    soup = BeautifulSoup(code)
    result = soup.find(name="li").text
    print(result)


class aaa(object):
    a = 10



if __name__ == '__main__':
    from core.article import article_reference
    # article_reference("http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode=CJFD&filename=SWSL201400003&dbname=CJFDLASN2014&RefType=1&vl=")
    # test_dev()
    # main()
    # download_page(DOWNLOAD_URL)
    # a = '<p class="hostUnit">出版文献量：<span>72 篇</span></p>'
    # soup = BeautifulSoup(a, "html.parser")
    # result = soup.text
    # print(result)
    print(aaa.a)
    pass
