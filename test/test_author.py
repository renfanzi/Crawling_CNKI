# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup


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


if __name__ == '__main__':
    print(article_author("李洪峰", ''))