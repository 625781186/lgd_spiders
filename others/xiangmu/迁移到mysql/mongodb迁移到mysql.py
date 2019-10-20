# -*- coding: utf-8 -*-
import pymysql
from pymongo import MongoClient

conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='', db='yushou2')
cur = conn.cursor()
dic = {
    'Beijing': ['beijing'],
    'Fujian': ['Jianyang', 'Longyan', 'Nanan', 'Quanzhou', 'Zhangzhou','Fuan'],
    'Guangdong': ['Guangzhou', 'Heyuan', 'Huizhou', 'Jiangmen', 'Shantou', 'Zhaoqing', 'Zhuhai'],
    'Guangxi': ['Guigang', 'Guiling', 'Nannin'],
    'Hebei': ['Cangzhou', 'Handan', 'Shijiazhuang', 'Tangshan', 'Zhangjiakou'],
    'Heilongjiang': ['Haerbin'],
    'Henan': ['Anyang', 'Kaifeng', 'Luoyang', 'Xinzheng', 'Zhengzhou', 'Zhoukou', 'Zhumadian'],
    'Liaoning': ['Anshan', 'Shenyang', 'Yingkou'],
    'Neimenggu': ['Baotou'],
    'Shandong': ['Jinan', 'Jining', 'Linyi', 'Qingdao', 'Qingzhou', 'Shouguang', 'Weihai', 'Xingtai', 'Yantai',
                 'Zaozhuang', 'Zibo'],
    'Shanxi': ['Jinzhong'],
    'Sichuan': ['Leshan', 'Luzhou'],
    'Tianjing': ['Tianjing'],
    'Yunnan': ['Kunming']
}
client = MongoClient('mongodb://root:123456@127.0.0.1:27017')
# 多条插入
for pro in dic:
    city_list = dic[pro]
    for city in city_list:
        print(city)
        col = client[pro][city]
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
        sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
            city.lower())
        cur.executemany(sql,tup_data)
        conn.commit()
        # break
    # break

# 单条插入
# for pro in dic:
#     city_list = dic[pro]
#     for city in city_list:
#         col = client[pro][city]
#         city_data = list(col.find())
#         print(city)
#         for i in city_data:
#             sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(city.lower())
#             data = (
#                 i['备案名'], i['预售证号'], i['核发日期'], i['开盘日期'], i['预售套数'], i['预售面积(平方米)'],
#                 i['预售均价(元/平方米)'],
#                 i['预售部位'], i['项目公司'], i['爬取时间'], i['链接地址'])
#             cur.execute(sql, data)
#             conn.commit()
