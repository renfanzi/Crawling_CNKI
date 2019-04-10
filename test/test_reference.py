from bs4 import BeautifulSoup

import requests

reference_url = "http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode=CJFD&filename=SWSL201400007&dbname=CJFDLASN2014&RefType=1&vl="


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
    a_list = soup.find(name="body").findAll(name="li")
    reference_list = list()
    for i in a_list:
        try:
            reference_dict = dict()
            i.find("em").clear()
            if i.find(name="a", attrs={"target": "kcmstarget"}):
                title = i.text
                link = "http://kns.cnki.net" + i.find(name="a", attrs={"target": "kcmstarget"}).get("href").strip()
            else:
                title = i.text
                link = "http://scholar.cnki.net/result.aspx?q=" + i.find(name="a").get("onclick").replace(
                    "              OpenCRLDENG('", '').replace("');", '').replace("\n", '')
            reference_dict["title"] = title
            reference_dict["link"] = link
            reference_list.append(reference_dict)
        except:
            continue

    return reference_list


if __name__ == '__main__':
    article_reference(reference_url)
