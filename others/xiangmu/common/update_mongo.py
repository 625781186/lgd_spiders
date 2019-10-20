import json
from hashlib import md5
import pymongo
import datetime
import pymysql


# conn = pymysql.connect(host="192.168.1.77", port=3306, user='root', passwd='798236031', db='test')


def Update(build, province, city):
    client = pymongo.MongoClient('mongodb://root:123456@127.0.0.1:27017')
    m = md5()
    m.update(json.dumps(build).encode('utf-8'))
    d_finger = m.hexdigest()
    id = {'_id': d_finger}
    new_dic = dict(build, **id)
    client[province][city].update_one({"_id": d_finger}, {'$set': new_dic}, upsert=True)


# def Update2(build, city):
#     conn = pymysql.connect(host="192.168.1.77", port=3306, user='root', passwd='798236031', db='work_spider')
#     cur = conn.cursor()
#     sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
#         city.lower())
#     cur.execute(sql, build)
#     conn.commit()

def Update2(build, city):
    conn = pymysql.connect(host="192.168.1.77", port=3306, user='root', passwd='798236031', db='work_spider')
    cur = conn.cursor()
    ca_num = build[1]
    company = build[8]
    pro_name = build[0]
    ca_time = build[2]
    sql = "select * from {} where ca_num=%s and company=%s and pro_name=%s and ca_time=%s;".format(city)
    cur.execute(sql, [ca_num, company, pro_name, ca_time])
    num = cur.fetchall()
    if len(num) > 0:
        # print(num)
        cur.close()
        conn.close()
        return
    sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
        city.lower())
    cur.execute(sql, build)
    conn.commit()
    cur.close()
    conn.close()
