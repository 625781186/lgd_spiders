# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import time
from common.spider_class import TongyongSpider
from common.update_mongo import Update
from common.update_mongo import Update2
import datetime
import os

path=os.path.dirname(__file__)
file='city.txt'
now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'guangzhou'


# 有频率限制
# 有些链接是死链，要去除掉

# 广州有一个网站会异常
class Producer(TongyongSpider):
    url = 'http://zfcj.gz.gov.cn/data/Laho/PreSellSearch.aspx?page={}'

    def get_links(self, url):
        for i in range(1,5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                trs = html.xpath('//table[@class="resultTableC"]//tr')[1:]
                for tr in trs:
                    href = tr.xpath('./td[3]/a/@href')[0]
                    link = 'http://zfcj.gz.gov.cn/data/laho/preSell.aspx?' + href.split('&')[3] + '&' + href.split('&')[
                        2] + '&maxPrice=&groundPrice='
                    pro_name = tr.xpath('./td[3]/a/text()')[0]
                    print(link)
                    self.db.sadd(self.redis_db, link + '<<<' + pro_name)
                return
            except Exception as e:
                print(url, e)
                if i==4:return

    def run(self):
        urls = [self.url.format(i) for i in range(1, 50)]
        for url in urls:
            self.get_links(url)
            time.sleep(2)


class Consumer(TongyongSpider):
    def parse_detail(self, link, pro_name):
        url = 'http://zfcj.gz.gov.cn/data/laho/projectdetail.aspx?changeproInfoTag=0&changePreSellTag=1&' + \
              re.split('[?&]', link)[2] + '&' + re.split('[?&]', link)[1] + '&name=ysz'
        try:
            response = requests.get(link, headers=self.headers,timeout=40)
            text = response.text
            html = etree.HTML(text)
            table = html.xpath('//table')[0]
            ca_num = table.xpath('.//tr[2]/td[2]/p/text()')[0]
            position = table.xpath('.//tr[2]/td[6]/p/text()')
            position = position[0] if position else ''
            sale_num = table.xpath('.//tr[4]/td[6]/p/text()')[0]
            area = table.xpath('.//tr[5]/td[2]/p/text()')[0]
            ca_time = table.xpath('.//tr[7]/td[6]/p/text()')[0]
            ca_time = re.sub(r'-', '/', ca_time)
            link2 = 'http://zfcj.gz.gov.cn/data//laho/project.aspx?' + re.split('[?&]', link)[1]
            response2 = requests.get(link2, headers=self.headers)
            text2 = response2.text
            html2 = etree.HTML(text2)
            company = ''.join(html2.xpath('//table//tr[3]/td[2]//text()'))
            pan_time = ''
            price = ''
            build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
            print(build)
            Update2(build, city)
            return 1
        except Exception as e:
            print(url, e)
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
            url = link.split('<<<')[0]
            title = link.split('<<<')[1]
            num = self.parse_detail(url, title)
            if num == 1:
                time.sleep(1)
                pass
            else:
                self.db.sadd(self.redis_db, link)
def run():
    try:
        p = Producer('GdGuangzhou:Detail')
        p.run()
        c = Consumer('GdGuangzhou:Detail')
        c.run()
    except Exception as e:
        file_path=os.path.join(path,file)
        with open(file_path,'at',encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')


if __name__ == '__main__':
    run()
