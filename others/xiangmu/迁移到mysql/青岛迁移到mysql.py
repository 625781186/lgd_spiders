# -*- coding: utf-8 -*-
import pymysql
import pymongo

client = pymongo.MongoClient('mongodb://root:123456@127.0.0.1:27017')
conn = pymysql.connect(host="192.168.1.77", port=3306, user='root', passwd='798236031', db='work_spider')
cur = conn.cursor()



#先清空青岛的表
sql='truncate table qingdao;'
cur.execute(sql)
conn.commit()


col = client['Shandong']['Qingdao']
mes = list(col.find())
city_data = list(col.find())
lis_data = [[
    i['备案名'], i['预售证号'], i['核发日期'], i['开盘日期'], i['预售套数'], i['预售面积(平方米)'],
    i['预售均价(元/平方米)'],
    i['预售部位'], i['项目公司'], i['爬取时间'], i['链接地址']] for i in city_data]
for index, value in enumerate(lis_data):
    for field_index, field_value in enumerate(value):
        if field_value == 'XXX':
            lis_data[index][field_index] = ''
tup_data = [(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10]) for i in lis_data]
# print(tup_data)
# print(len(tup_data))
sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
    'Qingdao'.lower())
cur.executemany(sql, tup_data)
conn.commit()
