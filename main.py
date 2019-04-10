# -*- coding:utf-8 -*-

"""
@#: 页面： main
@#：URL : http://navi.cnki.net/KNavi/All.html
@#: 时间： 2019/2/19
@#: 作者： Mr.L
"""
from selenium import webdriver  # 从selenium导入webdriver
from core.navigation import subject_navigation, subject_submenu


def main():
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

    # -----<学科导航>----- #
    subject_data = subject_navigation(driver)

    # for sub_data in range(len(subject_data) - 1, len(subject_data)):  # i， 每个学科, 基础科学， 工程科技I辑..... [6:8] -->[6, 7]
    for sub_data in [6, 7]:  # i， 每个学科, 基础科学， 工程科技I辑..... [6:8]
        print("subject_data[sub_data]: ", subject_data[sub_data])
        for sub_sub_data in range(len(subject_data[sub_data]["sub_subject_dd"])):  # j， 每个学科的子学科, 自然科学理论与方法
            """
            print(sub_data) # 0
            print(sub_sub_data) #0
            print(subject_data[sub_data]["sub_subject_dd"][sub_sub_data]) # {'dd_title': '自然科学理论与方法', 'dd_onclick': "Submit.naviSearch('1','专题子栏目代码','A001','自然科学理论与方法');"}
            """
            # 获取每个子学科的期刊
            periodical_all_list = subject_submenu(driver, sub_data, sub_sub_data,
                                                  subject_data[sub_data]["sub_subject_dd"][sub_sub_data])
            print("periodical_all_list: ")
            print(periodical_all_list)
            # break
        # break

    driver.close()


if __name__ == '__main__':
    main()
