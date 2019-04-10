# -*- coding:utf-8 -*-

"""
@#: 页面： 学科导航
@#：URL : http://navi.cnki.net/KNavi/All.html
@#: 时间： 2019/2/19
@#: 作者： Mr.L
"""
from bs4 import BeautifulSoup
import time
from core.knavi import periodical
from tools.model import mongo_model


# -----<学科导航>----- #
def subject_navigation(driver):
    driver.get("http://navi.cnki.net/KNavi/All.html")  # 获取页面
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 学科导航最外层
    subject = soup.find(name="ul", attrs={"class": "contentbox"}).findAll(name="li")
    subject_result = list()
    for li in subject:
        li_span = li.find(name="span", attrs={"class": "refirstcol"})
        subject_a_title = li_span.find(name='a').get("title")
        subject_a_onclick = li_span.find(name='a').get("onclick").strip()
        li_data = dict()
        li_data["subject_a_title"] = subject_a_title
        li_data["subject_a_onclick"] = subject_a_onclick
        li_data["url"] = "http://navi.cnki.net/KNavi/All.html"
        li_dl = li.find(name="dl", attrs={"class": "resecondlayer"})
        dl_dd = li_dl.findAll(name="dd")
        dd_list = list()
        for dd_a in dl_dd:
            dd = dict()
            dd_title = dd_a.find(name='a').get("title")
            dd_onclick = dd_a.find(name='a').get("onclick").strip()
            dd["dd_title"] = dd_title
            dd["dd_onclick"] = dd_onclick
            dd_list.append(dd)
        li_data["sub_subject_dd"] = dd_list
        subject_result.append(li_data)

    return subject_result


# -----<学科导航子菜单栏>----- #
def subject_submenu(driver, i, j, subdata):
    """
    pass
    :param driver:
    :param i:
    :param j:
    :param subdata: {'dd_title': '自然科学理论与方法', 'dd_onclick': "Submit.naviSearch('1','专题子栏目代码','A001','自然科学理论与方法');"}
    :return:
    """
    driver.get("http://navi.cnki.net/KNavi/All.html")  # 获取页面
    time.sleep(10)
    qqq = driver.find_element_by_xpath("//ul[@class='contentbox']/li[%s]/dl/dd[%s]/a" % (i + 1, j + 1))  # 寻找位置
    # 对定位到的元素执行鼠标右键操作
    # ActionChains(driver).click(qqq)
    driver.execute_script("document.getElementsByClassName('contentbox').onclick = %s" % subdata["dd_onclick"], qqq)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # -----<总页数>----- #
    page_data = soup.find(name="em", attrs={"id": "lblPageCount"}).text
    data = list()
    for page in range(1, int(page_data) + 1):

        driver.get("http://navi.cnki.net/KNavi/All.html")  # 获取页面
        time.sleep(10)
        qqq = driver.find_element_by_xpath("//ul[@class='contentbox']/li[%s]/dl/dd[%s]/a" % (i + 1, j + 1))
        # 对定位到的元素执行鼠标右键操作
        # ActionChains(driver).click(qqq)
        driver.execute_script("document.getElementsByClassName('contentbox').onclick = %s" % subdata["dd_onclick"], qqq)
        time.sleep(10)

        # Submit.pageTurn(2)
        driver.execute_script("document.getElementsByClassName('pagenav').onclick = Submit.pageTurn(%s)" % page)
        time.sleep(10)
        new_soup = BeautifulSoup(driver.page_source, "html.parser")
        # -----<学科导航子菜单右结果>----- #
        result = new_soup.find(name="dl", attrs={"class": "result"})
        sub_result = result.findAll(name="dd")
        sub_result_data = list()
        for an_info in sub_result:
            an_info_data = dict()
            an_info_div = an_info.find(name="div", attrs={"class": "re_brief fl"})
            # 单个期刊的基本信息
            # periodical 期刊
            title_herf = an_info_div.find(name="a", attrs={"target": "_blank"}).get("href").strip()
            title_name = an_info_div.find(name="a", attrs={"target": "_blank"}).text
            print("单个期刊的名字：", title_name)
            print("单个期刊的链接：", title_herf)
            an_info_data["periodical_name"] = title_name
            an_info_data["periodical_herf"] = title_herf  # ...
            an_info_li = an_info_div.findAll(name="li")
            an_info_li_subdata = []
            for sub_an_infor_li in an_info_li:
                an_info_li_subdata.append(str(sub_an_infor_li.text).strip())
            an_info_data["sub_info"] = an_info_li_subdata

            # periodical(driver, "http://navi.cnki.net/KNavi/pubDetail?pubtype=journal&pcode=CJFD&baseid=SWSL")
            if title_herf[:6] == "/KNavi":
                try:
                    periodical_data = periodical(driver, "http://navi.cnki.net" + title_herf)
                except:
                    continue
            else:
                periodical_data = {}
            an_info_data["periodical_data"] = periodical_data
            """
            unit = an_info_li[0].findAll(name="span")
            if len(unit) == 1:
                # 主办单位
                periodical_unit = unit[0].text  # 当前单位
                periodical_exunit = ""  # 原单位
            elif len(unit) == 2:
                periodical_unit = unit[0].text
                periodical_exunit = unit[1].text
            else:
                periodical_unit = ""
                periodical_exunit = ""
            an_info_data["periodical_unit"] = periodical_unit
            an_info_data["periodical_exunit"] = periodical_exunit
            sequence = an_info_li[1].findAll(name="span")
            periodical_ISSN = sequence[0].text
            periodical_CN = sequence[1].text
            an_info_data["periodical_ISSN"] = periodical_ISSN
            an_info_data["periodical_CN"] = periodical_CN

            try:
                count = an_info_li[2].findAll(name="span")
                if count[2:]:
                    periodical_complex_factor = count[0].text  # 复合因子
                    periodical_influencing_factor = count[1].text  # 综合因子
                    periodical_reference = count[3].text
                    periodical_download = count[4].text
                    an_info_data["periodical_reference"] = periodical_reference
                    an_info_data["periodical_download"] = periodical_download
                    an_info_data["periodical_complex_factor"] = periodical_complex_factor
                    an_info_data["periodical_influencing_factor"] = periodical_influencing_factor
                else:
                    periodical_reference = count[0].text
                    periodical_download = count[1].text
                    an_info_data["periodical_reference"] = periodical_reference
                    an_info_data["periodical_download"] = periodical_download
                    an_info_data["periodical_influencing_factor"] = ""
                    an_info_data["periodical_complex_factor"] = ""
            except:
                an_info_data["periodical_reference"] = 0
                an_info_data["periodical_download"] = 0
            sub_result_data.append(an_info_data)
            """
            # 单个期刊的数据
            print("an_info_data:", an_info_data)
            sub_result_data.append(an_info_data)
            # mongo_model(title_name, an_info_data)
            # break
        data = data + sub_result_data
        # break
    return {subdata["dd_title"]: data}
