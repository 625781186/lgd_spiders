# coding = utf - 8
import sys
from pymongo import MongoClient

#自己配置mongo的连接，
class MongoDBUtil:
    def __init__(self, col, mongo_urls='', user='',
                 pwd='', dbName='ip_pool'):
        self.client = MongoClient(mongo_urls)
        self.db_auth = self.client[dbName]
        #如果没有 账号密码，此条语句可以被注释
        # self.db_auth.authenticate(user, pwd)
        self.db = self.client[dbName]
        self.account = self.db[col]
    #删除无用的ip，返回删除ip的个数
    def delect(self):
        a = {"isValid": 0}
        x = self.account.delete_many(a)
        return x.deleted_count
    #更新ip的是否可用
    def updata(self, ip, isValid):
        # 连接需要存储数据库
        myquery = {"ip": ip}
        newvalues = {"$set": {"isValid": isValid}}
        self.account.update_one(myquery, newvalues)
    #返回一个无效ip的列表
    def select_all(self):
        all_ip = []
        # "_id": 0, "ip": 1, "isValid": 0, "count": 0
        for x in self.account.find({}, {"_id": 0, "isValid": 0, "count": 0}):
            all_ip.append(x['ip'])
        return all_ip

    def select_all_available_ip(self):
        ip_list = []
        for x in self.account.find({"isValid": 1}, {"_id": 0, "isValid": 0, "count": 0}):
            ip_list.append(x['ip'])
        # print(ip_list)
        return ip_list

    def insert_mongo(self, ip):
        mydict = {"ip": ip, "isValid": 1, "count": 0}
        x = self.account.insert_one(mydict)
        # print(x)

#
# if __name__ == '__main__':
#     # insert_mongo('b')
#     # delect()
#     pass
