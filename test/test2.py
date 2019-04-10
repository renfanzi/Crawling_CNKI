# http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=SWSL

# -*- coding:utf-8 -*-

"""
@#: 页面： main
@#：URL : http://navi.cnki.net/KNavi/All.html
@#: 时间： 2019/2/26
@#: 作者： Mr.L
"""
import time
from bs4 import BeautifulSoup
from tools.base import dict_append, url_translate
from selenium import webdriver
from core.article import article_info
from tools.base import Sleep


# -----<期刊浏览：时间区块>----- #
def periodical_date(driver, html_code, URL):
    yearissue = html_code.find(name="div", attrs={"id": "yearissue+0"})
    yearissuepage = yearissue.findAll(name='dl')
    issue_data = list()
    for page in yearissuepage:

        year_dict = dict()
        page_year_js_func = page.find(name="dt").get("onclick")
        page_year_data = page.find(name="dt").text

        # 年份有分页，有的期刊从1956年开始的《心理学报》

        # 年份
        year_dict["year"] = str(page_year_data)
        print(str(page_year_data))
        # 时间函数
        year_dict["year_func"] = str(page_year_js_func).strip()
        # 版本
        page_version = page.find(name="dd").findAll(name="a")

        print("page_version: ", page_version)

        page_version_data_list = list()

        for sub_version in page_version:
            # 子版本
            sub_year_version_data_dict = dict()
            page_ver_a_id = sub_version.get("id")
            page_ver_a_func = sub_version.get("onclick")
            page_ver_text = sub_version.text
            sub_year_version_data_dict["sub_version"] = page_ver_text
            sub_year_version_data_dict["sub_ver_func"] = page_ver_a_func
            sub_year_version_data_dict["a_id"] = page_ver_a_id
            print("page_ver_a_id", page_ver_a_id)
            url_arguments = url_translate(URL)
            print(url_arguments)
            #  "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2003&issue=S1&pykm=BZJL&pageIdx=0&pcode=CJFD"
            pykm = url_arguments["pykm"] if "pykm" in url_arguments else url_arguments["baseid"]
            version_articlt_html_url = "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=%s&issue=%s&pykm=%s&pageIdx=0&pcode=%s" % (
                year_dict["year"],
                str(page_ver_a_id).replace("yq" + year_dict["year"], ""),
                pykm,
                url_arguments["pcode"])

            print("version_articlt_html_url: ", version_articlt_html_url)
            import requests
            result = requests.post(version_articlt_html_url)
            data = result.text
            perdical_directory_list = perdical_directory(driver, BeautifulSoup(data, "html.parser"))
            print(perdical_directory_list)

        year_dict["year_version"] = page_version_data_list
        issue_data.append(year_dict)
    # print("issue_data: ", issue_data)
    return issue_data


# -----<期刊浏览： 内容目录页>----- #
def perdical_directory(driver, html_code):
    print(html_code)
    article_title = html_code.findAll(name="dd")  # []

    article_title_list = list()
    for single_article in article_title:
        single_article_dict = dict()
        single_article_title_a = single_article.find(name="span", attrs={'class': 'name'}).find(name="a")
        article_title_a_link = single_article_title_a.get("href")
        # print('article_title_a_link: ', article_title_a_link)
        article_title_a_text = single_article_title_a.text.strip()
        print(article_title_a_text)
        # 跳转链接 http://kns.cnki.net/kcms/detail/detail.aspx? + DBCode + DBName + fileName + uid

        head_url = "http://kns.cnki.net/kcms/detail/detail.aspx?"
        url_arguments = url_translate(article_title_a_link)
        cookie = [(item["name"], item["value"]) for item in driver.get_cookies()]
        # 单个文章的url链接拼接
        # http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=SWSL201400002&dbname=CJFDLASN2014&uid=...
        url = head_url + "dbcode=" + url_arguments["dbCode"] + "&filename=" + url_arguments["filename"] + "&dbname=" + \
              url_arguments["tableName"]
        single_article_dict["title"] = article_title_a_text
        single_article_dict["link"] = article_title_a_link
        single_article_dict["url"] = url
        single_article_dict["article_arguments"] = url_arguments

        article_title_list.append(single_article_dict)
    return article_title_list


# -----<期刊>----- #
def periodical(driver, URL):
    driver.get(URL)  # 获取页面
    time.sleep(Sleep.time_count)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 期刊基本信息
    periodical_date_info_data = periodical_date(driver, soup, URL)

    data = {}
    data["periodical_data"] = periodical_date_info_data

    print(data)
    return data


def main():
    '''
    一个刊期 —— > n年 -》 n版本 -》内容 -》 每个文章 -》　文章标题，　作者，作者详细信息，　其他．．．
    :return:
    '''
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    # periodical(driver, "http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=ANJA")
    # periodical(driver, "http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=SWSL")
    periodical(driver, "http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=CJJJ")
    time.sleep(Sleep.time_count)
    driver.close()


if __name__ == '__main__':
    main()
    # url = "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2003&issue=S1&pykm=BZJL&pageIdx=0&pcode=CJFD"
    # url = "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2018&issue=yq04&pykm=CJJJ&pageIdx=0&pcode=CJFD"
    # import requests
    # result = requests.post(url)
    # data = result.text
    # print(data)
