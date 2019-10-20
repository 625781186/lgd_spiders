# coding=utf-8
import pandas as pd
import pymysql
from conf.settings import *

conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
cur = conn.cursor()
# 北京 有
# url=http://zjw.beijing.gov.cn/eportal/ui?pageId=307670
sql = 'SELECT * FROM beijing WHERE ca_time in ("2019/8/12","2019/8/13","2019/8/14","2019/8/15","2019/8/16","2019/8/17","2019/8/18");'
df = pd.read_sql(sql, con=conn)
df = df.drop(columns=['spider_time', 'link_url'])
df.to_excel(r'D:\xiangmu\数据\北京.xlsx', index=False,
            header=['备案名', '预售证号', '核发日期', '开盘日期', '预售套数', '预售面积(平方米)', '预售均价(元/平方米)', '预售部位', '项目公司'])

# 天津
# url=http://zfcxjs.tj.gov.cn/ztzl/spfxsxk/2019n/index.html
# sql = 'SELECT * FROM tianjing WHERE ca_time in ("2019/08/12","2019/08/13","2019/08/14","2019/08/15","2019/08/16","2019/08/17","2019/08/18");'
# df = pd.read_sql(sql, con=conn)
# df = df.drop(columns=['spider_time', 'link_url'])
# df.to_excel(r'D:\xiangmu\数据\天津.xlsx', index=False,
#             header=['备案名', '预售证号', '核发日期', '开盘日期', '预售套数', '预售面积(平方米)', '预售均价(元/平方米)', '预售部位', '项目公司'])

# 济南
# url='http://jncc.jinan.gov.cn/jncjzhcx/zhcx/spfysxkz.do?searchname=xmmc&searchword=%E5%BC%80%E5%8F%91%E9%A1%B9%E7%9B%AE'
# sql = 'SELECT * FROM jinan WHERE ca_time in ("2019/08/12","2019/08/13","2019/08/14","2019/08/15","2019/08/16","2019/08/17","2019/08/18");'



# 青岛 有
# url='https://www.qdfd.com.cn/qdweb/realweb/fh/FhProjectQueryNew.jsp'
sql = 'SELECT * FROM qingdao WHERE pan_time in ("2019-08-12","2019-08-13","2019-08-14","2019-08-15","2019-08-16","2019-08-17","2019-08-18");'
df = pd.read_sql(sql, con=conn)
df = df.drop(columns=['spider_time', 'link_url'])
df.to_excel(r'D:\xiangmu\数据\青岛.xlsx', index=False,
            header=['备案名', '预售证号', '核发日期', '开盘日期', '预售套数', '预售面积(平方米)', '预售均价(元/平方米)', '预售部位', '项目公司'])

# 郑州 有
# url='http://218.28.223.13/zzzfdc/zhengzhou/permission.jsp?pn=&cn=&it=&pager.offset=0&page=1'
sql = 'SELECT * FROM zhengzhou WHERE ca_time in ("2019/08/12","2019/08/13","2019/08/14","2019/08/15","2019/08/16","2019/08/17","2019/08/18");'
df = pd.read_sql(sql, con=conn)
df = df.drop(columns=['spider_time', 'link_url'])
df.to_excel(r'D:\xiangmu\数据\郑州.xlsx', index=False,
            header=['备案名', '预售证号', '核发日期', '开盘日期', '预售套数', '预售面积(平方米)', '预售均价(元/平方米)', '预售部位', '项目公司'])

