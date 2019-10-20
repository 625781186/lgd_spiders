# -*- coding: utf-8 -*-
import pandas as pd
from conf.settings import *
import pymysql

conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
cur = conn.cursor()

# 北京8.12到8.18日数据
# sql='select * from beijing where ca_time=%s'
# pub_times=['2019/8/12','2019/8/13','2019/8/14','2019/8/15','2019/8/16','2019/8/17','2019/8/18']
# for pub_time in pub_times:
#     cur.execute(sql,(pub_time,))
#     mes=cur.fetchall()
#     print(mes)

# 导出某个城市数据
city = 'wuhu'
excel_name = '芜湖.xlsx'
sql = 'select * from {}'.format(city)
df = pd.read_sql(sql, con=conn)
df = df.drop(columns=['spider_time', 'link_url'])
df.to_excel(r'D:\xiangmu\data\{}'.format(excel_name), index=False,
            header=['备案名', '预售证号', '核发日期', '开盘日期', '预售套数', '预售面积', '预售均价', '预售部位', '项目公司'])
