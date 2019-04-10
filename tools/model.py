# -*- coding:utf-8 -*-

from pymongo import MongoClient


def mongo_model(database, content):
    # 建立MongoDB数据库连接
    client = MongoClient('192.168.2.137', 27017)

    # 连接所需数据库,test为数据库名
    # db = client[database]
    db = client.test

    # 连接所用集合，也就是我们通常所说的表，test为表名
    collection = db["article"]

    # 向集合中插入数据
    data = collection.find_one({"link": content["link"]})
    if not data:
        collection.insert(content)


if __name__ == '__main__':
    mongo_model("吃饭", [{"aaa": 23232}, {"bbbb": "asdfafd"}])
