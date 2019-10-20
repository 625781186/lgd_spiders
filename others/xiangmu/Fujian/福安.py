# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime
import os

path = os.path.dirname(__file__)
file = 'city.txt'

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'fuan'


class Producer(TongyongSpider):
    first_url = ''
    url = 'http://www.fjfa.gov.cn/was5/web/search?channelid=226763&templet=docs.jsp&sortfield=-docreltime&classsql=(%27%E9%A2%84%E5%94%AE%27)*(siteid%3D39)&prepage=10&page={}'

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url,headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                links = re.findall(r'http:.*?htm', text, re.S)
                for i in links:
                    if 'zfxxgkml/gkml' in i:
                        print(i)
                        self.db.sadd(self.redis_db, i)
                return
            except Exception as e:
                print(url, e)
                if i == 4:
                    return

    def run(self):
        for i in range(1, 34):
            self.get_links(self.url.format(i))
            time.sleep(1)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('utf-8')
                html = etree.HTML(text)
                content = ''.join(html.xpath('//body//text()'))
                if '同意你公司' not in content:
                    return 1
                else:
                    try:
                        company = re.search(r'(.*?公司)', content).group(1)
                        company = re.sub(r'\s', '', company)
                        pro_name = re.search(r'同意.*?公司开?发?.*?“(.*?)”', content).group(1)
                        position = re.search(r'楼盘(.*?)预售', content)
                        position = position.group(1) if position else ''
                        area = re.search(r'预售许?可?.*?面积.*?(\d+\.?\d+)㎡', content)
                        area = area.group(1) if area else ''
                        ca_time = re.search(r'(\d+年\d+月\d+)日', content)
                        ca_time = ca_time.group(1) if ca_time else ''
                        ca_time = re.sub(r'[年月]', '/', ca_time)
                        p_list = html.xpath('//p')
                        sale_num = ''
                        for p in p_list:
                            content2 = ''.join(p.xpath('.//text()'))
                            if '同意你公司' in content2:
                                sale_num = re.findall(r'共(\d+)[个套间]', content2)
                                # print(sale_num)
                                if len(sale_num) > 0:
                                    num = 0
                                    for i in sale_num:
                                        num += int(i)
                                    sale_num = str(num)
                                else:
                                    sale_num = ''
                        pan_time = ''
                        price = ''
                        ca_num = ''
                        build = (
                        pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                        print(build)
                        Update2(build, city)
                        return 1
                    except AttributeError:
                        print('没有项目名')
                        return 1
                    except Exception:
                        print(url, '解析异常')
                        return 1
            except Exception as e:
                print(url, e)
                if i == 4:
                    return 1

    def run(self):
        while True:
            set_num = self.db.scard(self.redis_db)
            if set_num == 0:
                print('数目为0')
                time.sleep(10)
                set_num2 = self.db.scard(self.redis_db)
                if set_num2 == 0: return
            link = self.db.spop(self.redis_db)
            num = self.parse_detail(link)
            if num == 1:
                time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    try:
        p = Producer('FjFuan')
        p.run()
        c = Consumer('FjFuan')
        c.run()
    except Exception as e:
        file_path = os.path.join(path, file)
        with open(file_path, 'at', encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')


if __name__ == '__main__':
    run()
