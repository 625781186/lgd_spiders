# -*- coding: utf-8 -*-
import pymysql
from pymongo import MongoClient

conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='', db='yushou2')
cur = conn.cursor()
# names = ['Beijing', 'Fujian', 'Guangdong', 'Guangxi', 'Hebei', 'Heilongjiang', 'Henan', 'Liaoning', 'Neimenggu',
#          'Shandong', 'Shanxi', 'Sichuan', 'Tianjing', 'Yunnan']
dic = {
    'Beijing': ['beijing'],
    'Fujian': ['Jianyang', 'Longyan', 'Nanan', 'Quanzhou', 'Zhangzhou'],
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
# for db_name in dic:
#     create_database_sql = 'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci;' % db_name
#     cur.execute(create_database_sql)
#     for col_name in dic[db_name]:
#         cur.execute("use %s;"%db_name)
#         create_table_sql = '''
#             CREATE TABLE %s(
#                 ``id`` int AUTO_INCREMENT PRIMARY KEY,
#                 ``备案名`` text,
#                 ``预售证号`` text,
#                 ``核发日期`` text,
#                 ``开盘日期`` text,
#                 ``预售套数`` text,
#                 ``预售面积(平方米)`` text,
#                 ``预售均价(元/平方米)`` text,
#                 ``预售部位`` text,
#                 ``项目公司`` text,
#                 ``爬取时间`` text,
#                 ``链接地址`` text,
#                 ``md5`` text
#             )engine=innodb DEFAULT CHARACTER set utf8;
#         '''%col_name
#         cur.execute(create_table_sql)
#         print('创建数据库表成功')
# cur.close()
client = MongoClient('mongodb://root:123456@127.0.0.1:27017')
ss = ''
for pro in dic:
    city_list = dic[pro]
    for city in city_list:
        col = client[pro][city]
        city_data = list(col.find())
        print(city)
        for i in city_data:
            sql = "insert into {}(pro_name,ca_num,ca_time,pan_time,sale_num,area,price,position,company,spider_time,link_url,md5) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(city.lower())
            data = (
                i['备案名'], i['预售证号'], i['核发日期'], i['开盘日期'], i['预售套数'], i['预售面积(平方米)'],
                i['预售均价(元/平方米)'],
                i['预售部位'], i['项目公司'], i['爬取时间'], i['链接地址'], i['_id'])
            # break
            cur.execute(sql, data)
            conn.commit()
