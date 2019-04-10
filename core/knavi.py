# -*- coding:utf-8 -*-

"""
@#: 页面： main
@#：URL : http://navi.cnki.net/KNavi/All.html
@#: 时间： 2019/3/26
@#: 作者： Mr.L
"""
import time, requests
from bs4 import BeautifulSoup
from tools.base import dict_append, url_translate
from selenium import webdriver
from core.article import article_info
from tools.base import Sleep
from tools.model import mongo_model


# -----<期刊基本信息>----- #
def periodical_base_info(URL, html_code):
    # class = infobox, titbox
    infobox = html_code.find(name="dd", attrs={"class": "infobox"})

    # 期刊标签[CSSCI, 核心期刊，等...]
    journalType = [i.text for i in infobox.find(name="p", attrs={"class": "journalType"}).findAll("span")]
    print("期刊标签：", journalType)
    titbox = infobox.find(name="h3", attrs={"class": "titbox"})
    # 英文期刊名
    english_period_name = infobox.find(name="p").text
    # 中文期刊名
    chinese_period_name = str(titbox.text).strip().rstrip(str(english_period_name))
    # listbox clearfix
    baseinfo_and_issesinfo = html_code.find(name="div", attrs={"class": "listbox clearfix"})
    """
    这里有三个<ul>， 有的有两个， 基本信息(JournalBaseInfo)， 出版信息(publishInfo)， 评价信息(evaluateInfo)
    """
    info = baseinfo_and_issesinfo.findAll(name="ul")
    info_data_list = list()
    # 中文
    info_data_list.append(chinese_period_name)
    # 英文
    info_data_list.append(english_period_name)
    # url
    info_data_list.append(URL)
    # 标签
    info_data_list.append(journalType)

    for sub_ul in info:
        sub_ul_id = sub_ul.get("id").strip()
        if sub_ul_id == "JournalBaseInfo":
            ul_name = "基本信息"
        elif sub_ul_id == "publishInfo":
            ul_name = "出版信息"
        elif sub_ul_id == "evaluateInfo":
            ul_name = "评价信息"
        else:
            ul_name = ""
        p_data = dict()
        p_all_info = sub_ul.findAll(name="p")

        for sub_p_key in p_all_info:
            sub_p_data = dict()
            p_subdata_key = str(sub_p_key.text).split("：")[0]
            try:
                p_subdata_value = sub_p_key.find(name="span").text
            except:
                continue
            sub_p_data[p_subdata_key] = p_subdata_value
            p_data = dict_append(p_data, sub_p_data)

        sub_info_data = dict()
        sub_info_data["ul_name"] = ul_name
        sub_info_data["ul_english_name"] = sub_ul_id
        sub_info_data["data"] = p_data
        info_data_list.append(sub_info_data)
    return info_data_list


# -----<期刊浏览：时间区块>----- #
def periodical_date(driver, html_code, URL, periodical_base_info_data):
    yearissue = html_code.find(name="div", attrs={"id": "yearissue+0"})
    yearissuepage = yearissue.findAll(name='dl')
    issue_data = list()
    # 年
    for page in yearissuepage:

        """
        [
            {
            "year": "2017",
            "year_func": "JournalDetail.BindYearClick(this);"
                这里注意： 需要把<a标签 id拿到>方便出发js
                <a id="yq201805" onclick="JournalDetail.BindIssueClick(this)">No.05</a>
                driver.execute_script("document.getElementsByClassName('contentbox').onclick = %s" % subdata["dd_onclick"], qqq)
            "year_version": 
                    [
                        {
                            "sub_version": "No.05", 
                            "sub_ver_func": "JournalDetail.BindIssueClick(this)", 
                            "a_id": "yq201805"
                        }, ...
                    ]
            },.....
        ]
        """
        year_dict = dict()
        page_year_js_func = page.find(name="dt").get("onclick")
        page_year_data = page.find(name="dt").text

        # 年份有分页，有的期刊从1956年开始的《心理学报》

        # 年份
        year_dict["year"] = str(page_year_data)
        # 时间函数
        year_dict["year_func"] = str(page_year_js_func).strip()
        # 版本
        page_version = page.find(name="dd").findAll(name="a")
        page_version_data_list = list()
        # 出版期号
        for sub_version in page_version:
            # 子版本
            sub_year_version_data_dict = dict()
            page_ver_a_id = sub_version.get("id")
            page_ver_a_func = sub_version.get("onclick")
            page_ver_text = sub_version.text
            sub_year_version_data_dict["sub_version"] = page_ver_text
            sub_year_version_data_dict["sub_ver_func"] = page_ver_a_func
            sub_year_version_data_dict["a_id"] = page_ver_a_id

            # 期刊每期，得到内容目录
            # 出发a标签每年的版本
            print(sub_year_version_data_dict)
            driver.get(URL)
            """
            # 触发无效果，改用requests
            time.sleep(Sleep.time_count)
            js_dom_func = "document.getElementById('%s').onclick = %s;" % (page_ver_a_id, page_ver_a_func)
            print("js_dom_func: ", js_dom_func)
            driver.execute_script(js_dom_func)
            time.sleep(Sleep.time_count)
            print(BeautifulSoup(driver.page_source, "html.parser"))
            perdical_directory_list = perdical_directory(driver, BeautifulSoup(driver.page_source, "html.parser"))
            """
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
            result = requests.post(version_articlt_html_url)
            data = result.text
            perdical_directory_list = perdical_directory(driver, BeautifulSoup(data, "html.parser"),
                                                         periodical_base_info_data, page_year_data, page_ver_text) # year, version

            sub_year_version_data_dict["article_directory"] = perdical_directory_list
            page_version_data_list.append(sub_year_version_data_dict)

        year_dict["year_version"] = page_version_data_list
        issue_data.append(year_dict)
    # print("issue_data: ", issue_data)
    return issue_data


# -----<期刊浏览： 内容目录页>----- #
def perdical_directory(driver, html_code, periodical_base_info_data, page_year_data, page_ver_text):
    # directory_all = html_code.find(name="dl", attrs={"id": "CataLogContent"})
    # 文章标题
    article_title = html_code.findAll(name="dd")  # []
    article_title_list = list()
    for single_article in article_title:
        single_article_dict = dict()
        single_article_title_a = single_article.find(name="span", attrs={'class': 'name'}).find(name="a")
        article_title_a_link = single_article_title_a.get("href")
        print('article_title_a_link: ', article_title_a_link)
        article_title_a_text = single_article_title_a.text.strip()
        # 跳转链接 http://kns.cnki.net/kcms/detail/detail.aspx? + DBCode + DBName + fileName + uid
        '''
        http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=BJWD201706001&dbname=CJFDLAST2018&uid=WEEvREcwSlJHSldRa1FhdkJkVG1COG9jZzUxQWhaWU05UjM2SGZ0aEoyUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!
        Common/RedirectPage?sfield=FN&amp;dbCode=CJFD&amp;filename=BJWD201706001&amp;tableName=CJFDLAST2018&amp;url=
        '''
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
        if url[:4] == "http":
            try:
                single_article_dict["article_data"] = article_info(driver, url, url_arguments,
                                                                   periodical_base_info_data, page_year_data, page_ver_text)
                mongo_model(single_article_dict["title"], single_article_dict["article_data"])
            except:
                single_article_dict["article_data"] = []
        else:
            single_article_dict["article_data"] = []

            # 这个地方需要--》进入单个文章，得到详细信息

        article_title_list.append(single_article_dict)
    return article_title_list


# -----<期刊>----- #
def periodical(driver, URL):
    driver.get(URL)  # 获取页面
    time.sleep(Sleep.time_count)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 期刊基本信息
    periodical_base_info_data = periodical_base_info(URL, soup)
    periodical_date_info_data = periodical_date(driver, soup, URL, periodical_base_info_data)
    # print(periodical_base_info_data)
    # print(periodical_date_info_data)
    data = {}
    data["periodical_info"] = periodical_base_info_data
    data["periodical_data"] = periodical_date_info_data

    # 期刊浏览--》 有的期刊没有
    # 年份
    # 期号
    # 目录大标题
    # 标题
    print(data)
    return data


def main():
    '''
    一个刊期 —— > n年 -》 n版本 -》内容 -》 每个文章 -》　文章标题，　作者，作者详细信息，　其他．．．
    :return:
    '''
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    # periodical(driver, "http://navi.cnki.net/KNavi/pubDetail?pubtype=journal&pcode=CJFD&baseid=SWSL")
    periodical(driver, "http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=BJDZ&tdsourcetag=s_pctim_aiomsg")
    time.sleep(Sleep.time_count)
    driver.close()


if __name__ == '__main__':
    main()
