# -*- coding:utf-8 -*-

"""
@#: 页面： article
@#：URL : http://navi.cnki.net/KNavi/All.html
@#: 时间： 2019/3/15
@#: 作者： Mr.L
"""

import time
from bs4 import BeautifulSoup
from tools.base import dict_append, url_translate
from selenium import webdriver
import requests
from tools.base import Sleep


# -----<文章：期刊信息>----- #
def publication_baseinfo(baseinfo):
    """
    baseinfo = {'periodical_info':
        [
            '北京大学学报(自然科学版)',
            'Acta Scientiarum Naturalium Universitatis Pekinensis',
            'http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=BJDZ&tdsourcetag=s_pctim_aiomsg',
            ['核心期刊', 'CA', 'SA', 'JST', 'Pж(AJ)', 'EI', 'CSCD'],
            {
                'ul_name': '基本信息',
                'ul_english_name': 'JournalBaseInfo',
                'data': {
                    '主办单位': '北京大学',
                    '出版周期': '双月',
                    'ISSN': '0479-8023',
                    'CN': '11-2442/N',
                    '出版地': '北京市',
                    '语种': '中文',
                    '开本': '16开',
                    '邮发代号': '2-89',
                    '创刊时间': '1955'}
            },
            {
                'ul_name': '出版信息',
                'ul_english_name': 'publishInfo',
                'data': {
                    '专辑名称': '基础科学',
                    '专题名称': '基础科学综合',
                    '出版文献量': '5545 篇',
                    '总下载次数': '1300044 次',
                    '总被引次数': '55734 次'}
            },
            {
                'ul_name': '评价信息',
                'ul_english_name': 'evaluateInfo',
                'data': {
                    '（2018版）复合影响因子': '1.613',
                    '（2018版）综合影响因子': '0.993',
                    '1992年(第一版),1996年(第二版),2000年版,2004年版,2008年版,2011年版,2014年版,2017年版;': '1992年(第一版),1996年(第二版),2000年版,2004年版,2008年版,2011年版,2014年版,2017年版;',
                    '中科双高期刊;第二届全国优秀科技期刊;第三届(2005)国家期刊提名奖期刊;': '中科双高期刊;第二届全国优秀科技期刊;第三届(2005)国家期刊提名奖期刊;'
                }
            }
        ]
    }
    """
    """
    'name':'中国社会科学',
    'link':'http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=ZSHK',
    'label':['核心期刊','CSSCI'],
    'type':1,                            //出版物类型：1-期刊，2-会议，3-学位论文，4-年鉴，5-书籍专著，5-新闻报纸
    'influence_fh': 7.218,               //复合影响因子
    'influence_zh': 5.357,               //综合影响因子
    'influence_year': 2018,              //影响因子计算年份
    """
    publication = {}
    publication["name"] = baseinfo[0]
    publication["link"] = baseinfo[2]
    # publication["link"] = baseinfo[3]
    publication["type"] = 1
    base_dict = dict()
    for i in baseinfo[4:]:
        base_dict = dict_append(base_dict, i["data"])
    print("base_dict: ", base_dict)
    influence_fh = [base_dict[i] for i in list(base_dict.keys()) if '复合影响因子' in i]
    influence_zh = [base_dict[i] for i in list(base_dict.keys()) if '综合影响因子' in i]
    publication["influence_fh"] = influence_fh[0] if influence_fh else 0
    publication["influence_zh"] = influence_zh[0] if influence_zh else 0
    publication["influence_year"] = 0
    return publication


# -----<文章：作者机构>----- #
def article_author(author, author_code):
    url = "http://kns.cnki.net/kcms/detail/knetsearch.aspx?sfield=au&skey=%s&code=%s" % (author, author_code)
    author_html = requests.get(url).text
    soup = BeautifulSoup(author_html, "html.parser")
    p = soup.find(name="p", attrs={"class": "orgn"})
    if not p:
        organ = ''
        cnki_organ_id = ''
    else:
        # kcmstarget
        a = p.find(name="a", attrs={"target": "kcmstarget"})
        cnki_organ_id = a.get("onclick").strip().replace("TurnPageToKnet(", '').replace(")", '').split(',')[2]
        organ = a.text
    return {
        "name": author,
        "cnki_author_id": author_code,
        "organ": organ,
        "depart": "",
        "cnki_organ_id": cnki_organ_id
    }


def article_info(driver, url, url_arguments, periodical_base_info_data, page_year_data, page_ver_text):
    '''
    @: 获取单个文章的基本信息
    @：作者， 机构
    @：文章概述
    @：基金， 关键词 x
    @：下载链接
    @：参考文献
    @：关联作者
    @：相似文献
    :param driver:
    :param url:
    :return:
    @： 作者URL拼接
    http://kns.cnki.net/kcms/detail/knetsearch.aspx?sfield=au&skey=%E6%B1%9F%E6%B5%B7%E5%B3%B0&code=06147284
    '''
    driver.get(url)  # 获取页面
    time.sleep(Sleep.time_count)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 标题
    article_data = dict()

    article_title = soup.find(name="h2", attrs={"class": "title"}).text
    article_author_list = soup.find(name="div", attrs={"class": "author"}).findAll(name="a")
    # 组织
    article_orgn_list = soup.find(name="div", attrs={"class": "orgn"}).findAll(name="a")
    # 摘要
    article_summary = soup.find(name="span", attrs={"id": "ChDivSummary"}).text
    # 基金标签
    try:
        fundation_label = soup.find(name="label", attrs={"id": "catalog_FUND"})
        fundation = fundation_label.next_sibling.string
    except:
        fundation = ""

    # 关键字标签
    try:
        keywords_label = soup.find(name="label", attrs={"id": "catalog_KEYWORD"})
        keywords = [i.string for i in keywords_label.parent.findAll("a")]
    except:
        keywords = ""

    # 分类号标签
    try:
        class_label = soup.find(name="label", attrs={"id": "catalog_ZTCLS"})
        class_number = class_label.parent.string
    except:
        class_number = ""

    # 页数
    article_page_obj = soup.find(name="div", attrs={"class": "total"}).findAll(name="span")
    article_page_dict = dict()
    for page_h in article_page_obj:
        page_key = page_h.find("label").text
        page_val = page_h.find("b").text
        article_page_dict[page_key] = page_val

    # 下载链接
    article_link_list = soup.find(name="div", attrs={"id": "DownLoadParts"}).findAll(name='a', attrs={
        "onclick": "WriteKrsDownLog()"})
    # 作者
    author_list = list()
    for au in article_author_list:
        author_dict = dict()
        author_dict["name"] = au.text.strip()
        author_dict["author_func"] = au.get("onclick").strip()
        cnki_author_id = au.get("onclick").strip().replace("TurnPageToKnet(", '').replace(")", '').split(',')[2]
        author_dict["author_func"] = cnki_author_id
        # author_list.append(author_dict)
        author_list.append(article_author(au.text.strip(), cnki_author_id))

    orgn_list = list()
    for orgn in article_orgn_list:
        orgn_dict = dict()
        orgn_dict["orgn"] = orgn.text.strip()
        orgn_dict["orgn_func"] = orgn.get("onclick").strip()
        orgn_list.append(orgn_dict)
    # download
    down_list = list()
    for down in article_link_list:
        down_dict = dict()
        down_dict["source"] = down.text.strip()
        down_dict["link"] = "http://kns.cnki.net" + down.get("href").strip()
        down_dict["free"] = "false"
        down_list.append(down_dict)

    # 刊物基本信息
    try:
        article_data["publication"] = publication_baseinfo(periodical_base_info_data)
    except:
        article_data["publication"] = {}
    # 出版信息
    article_data["publish"] = {"year": page_year_data, "period": page_ver_text, "time": ''}
    # 链接
    article_data["link"] = url.strip()
    # page
    article_data["page"] = article_page_dict["页码："] if article_page_dict["页码："] else 0
    # page_count
    article_data["page_count"] = article_page_dict["页数："] if article_page_dict["页数："] else 0
    # 文章代码
    article_data["article_code"] = url_arguments
    # 标题
    article_data["title"] = article_title
    # 作者
    article_data["author"] = author_list
    # 组织
    article_data["orgn"] = orgn_list
    # 摘要
    article_data["summary"] = article_summary
    # 基金
    article_data["fundation"] = fundation
    # 关键字
    article_data["keywords"] = keywords
    # 分类号
    article_data["class_number"] = class_number
    # 下载资源
    article_data["download"] = down_list

    # 参考文献
    # http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode=CJFD&filename=swsl201400002&dbname=CJFDLASN2014&RefType=1&vl=
    reference_head_url = "http://kns.cnki.net/kcms/detail/frame/list.aspx?"
    reference_url = reference_head_url + "dbcode=" + url_arguments["dbCode"] + "&filename=" + url_arguments["filename"]
    reference_url += "&dbname=" + url_arguments["tableName"] + "&RefType=1&vl="
    # print(reference_url)

    reference_data = article_reference(reference_url)
    # 参考文章
    article_data["reference"] = reference_data
    print(article_data)
    return article_data


# -----<参考文章>----- #
def article_reference(url):
    '''
    http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode=CJFD&filename=swsl201400002&dbname=CJFDLASN2014&RefType=1&vl=
    :param url:
    :return:
    '''
    # try
    print(url)
    result = requests.get(url).text
    # print(result)
    '''
    ﻿<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
      <head>
        <META http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link rel="stylesheet" type="text/css" href="http://piccache.cnki.net/kdn/KCMS/detail/resource/gb/css_min/Global.min.css?v=FBC16D09D6F9935E">
        <link rel="stylesheet" type="text/css" href="http://piccache.cnki.net/kdn/KCMS/detail/resource/gb/css_min/ecplogin.min.css?v=FBC16D09D6F9935E">
        <script type="text/javascript" src="/kcms/detail/js/getLink.aspx"></script>
        <script type="text/javascript" src="http://piccache.cnki.net/kdn/KCMS/detail/js/jquery-1.4.2.min.js"></script>
        <script type="text/javascript" src="http://piccache.cnki.net/kdn/KCMS/detail/resource/gb/js/min/rs.min.js?v=FBC16D09D6F9935E"></script>
        <script type="text/javascript" src="http://piccache.cnki.net/kdn/KCMS/detail/js/min/Common.min.js?v=FBC16D09D6F9935E0129"></script>
        <script type="text/javascript" src="http://piccache.cnki.net/kdn/KCMS/detail/js/min/refer.min.js?v=FBC16D09D6F9935E"></script></head>
      <body onload="ResezeParent(10);SetParentCatalog();"><script type="text/javascript" src="http://piccache.cnki.net/kdn/KCMS/detail/js/min/WideScreen.min.js"></script>
      </body>
    </html>
    '''
    soup = BeautifulSoup(result, "html.parser")
    a_list = soup.find(name="body").findAll(name="a", attrs={"target": "kcmstarget"})
    if a_list:
        reference_list = list()
        for reference in a_list:
            print(reference)
            reference_dict = dict()
            # 参考文章标题
            reference_dict["title"] = reference.text
            reference_dict["link"] = "http://kns.cnki.net" + reference.get("href").strip()
            reference_list.append(reference_dict)
        return reference_list
    else:
        # 没有怎么返回
        return []


def main():
    '''
    单个页面的数据， 详细信息， 下载链接， 作者信息， 关联作者， 相似文献
    :return:
    '''
    driver = webdriver.Chrome("C:\Program Files (x86)\Chrome\Application\chromedriver.exe")  # Optional argument, if not specified will search path.
    """article_info(driver,
                 "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=SWSL201400002&dbname=CJFDLASN2014",
                 # "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=CBBZ201206015&dbname=CJFD2012",
                 {'sfield': 'FN', 'dbCode': 'CJFD', 'filename': 'SWSL201400003', 'tableName': 'CJFDLASN2014', 'url': ''}
                 )"""
    article_info(
        driver,
        "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=SWSL201400007&dbname=CJFDLASN2014",
        # "http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=SWSL201400002&dbname=CJFDLASN2014"
        # {'sfield': 'FN', 'dbCode': 'CJFD', 'filename': 'SWSL201400003', 'tableName': 'CJFDLASN2014', 'url': ''},
        {'sfield': 'FN', 'dbCode': 'CJFD', 'filename': 'SWSL201400007', 'tableName': 'CJFDLASN2014', 'url': ''},
        {},
        '',
        ''
    )
    time.sleep(3)
    driver.close()


if __name__ == '__main__':
    main()
