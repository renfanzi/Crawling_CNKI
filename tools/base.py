#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests, os, configparser
from urllib.parse import urlparse


class Config(object):
    """
    # Config().get_content("user_information")
    """

    def __init__(self, config_filename="my.cnf"):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf", config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class Sleep(object):
    time_count = Config().get_content("sleeptime")["time_count"]


class Requests(object):
    @staticmethod
    def post(url, data=None, json=None, **kwargs):
        return requests.post(url, data, json, **kwargs)

    @staticmethod
    def get(url, params=None, **kwargs):
        return requests.get(url, params=None, **kwargs)


def dict_append(dict1, dict2):
    new_dict = list(dict1.items()) + list(dict2.items())
    return dict(new_dict)


def url_translate(arg):
    '''
    test = "Common/RedirectPage?sfield=FN&amp;dbCode=CJFD&amp;filename=BJWD201706001&amp;tableName=CJFDLAST2018&amp;url="
    from urllib.parse import urlparse

    url_change = urlparse(test)
    print(url_change.query.split(";"))

    result = url_translate(test)
    print(result)
    :param arg:
    :return: ['sfield=FN&amp', 'dbCode=CJFD&amp', 'filename=BJWD201706001&amp', 'tableName=CJFDLAST2018&amp', 'url=']
    {'sfield': 'FN', 'dbCode': 'CJFD', 'filename': 'BJWD201706001', 'tableName': 'CJFDLAST2018', 'url': ''}
    '''
    url_change = urlparse(arg)
    data = dict()
    for i in url_change.query.split("&"):
        key = i.split("=")
        if len(key) == 2:
            # key[1] = key[1].replace("&amp", '')
            data[key[0]] = key[1]
        else:
            data[key[0]] = ""
    return data


if __name__ == '__main__':
    # result = Requests.post("http://192.168.2.137:8001/test")
    # print(result.text)
    # result = dict_append({1: 2}, {2: 3})
    # print(result)
    # url = "Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=SWSL201400002&tableName=CJFDLASN2014&url="
    # print(url_translate(url))
    print(Sleep.time_count)
