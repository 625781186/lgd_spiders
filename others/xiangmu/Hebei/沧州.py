# -*- coding: utf-8 -*-
from common.spider_class import TongyongSpider
import requests
from lxml import etree
import re
from common.update_mongo import Update
from common.update_mongo import Update2
import time
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'cangzhou'


class Producer(TongyongSpider):
    urls = ['http://www.zjj.cangzhou.gov.cn/hzzfgq/shgk/index.shtml'] + [
        'http://www.zjj.cangzhou.gov.cn/hzzfgq/shgk/index_{}.shtml'.format(i) for i in range(2, 6)]

    def get_links(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('gbk')
                html = etree.HTML(text)
                a_list = html.xpath('//div[@class="rmain"]//li/a')
                for a in a_list:
                    content = ''.join(a.xpath('.//text()'))
                    if ('沧州市住房和城乡建设局行政许可事项公示' in content):
                        href = a.xpath('./@href')[0][5:]
                        link = 'http://www.zjj.cangzhou.gov.cn' + href
                        print(link)
                        self.db.sadd(self.redis_db, link)
            except Exception as e:
                print(e)

    def run(self):
        for url in self.urls:
            self.get_links(url)


class Consumer(TongyongSpider):
    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                print(url)
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('gbk')
                if '无效链接' in text: return 1
                html = etree.HTML(text)
                trs = html.xpath('//table//tr')
                zoom = ''.join(html.xpath('//table//text()'))
                if '商品房预售' not in zoom: return 1
                fang_index = engine_index = company_index = None
                for index, tr in enumerate(trs):
                    content = ''.join(tr.xpath('./td[1]//text()'))
                    if '商品房预售' in content:
                        fang_index = index
                    elif '建筑工程施工' in content:
                        engine_index = index
                    elif '建筑业企业' in content:
                        company_index = index
                first_index = fang_index
                if engine_index and company_index:
                    if first_index < min(engine_index, company_index):
                        last_index = min(engine_index, company_index)
                    elif first_index > max(engine_index, company_index):
                        last_index = None
                    else:
                        last_index = max(engine_index, company_index)
                else:
                    x_index = engine_index if engine_index else company_index
                    if engine_index == None: return 1
                    last_index = x_index if (x_index > first_index) else None
                trs = html.xpath('//table//tr')[first_index:last_index]
                for tr in trs:
                    content = re.sub(r'\s', '', ''.join(tr.xpath('./td[1]//text()')))
                    if ('商品房预售' in content) or (content == ''):
                        ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                        company = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                        pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                        sale_info = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                        area = re.search(r'(\d+\.?\d+)㎡', sale_info)
                        area = area.group(1) if area else ''
                        sale_num = re.search(r'(\d+)套', sale_info)
                        sale_num = sale_num.group(1) if sale_num else ''
                        ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[7]//text()')))
                        ca_time = re.sub(r'[年月]', '/', ca_time)
                        ca_time = re.sub(r'日', '', ca_time)
                        position = '、'.join(re.findall(r'(\d+#.*?楼)', pro_name))
                    else:
                        ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                        company = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                        pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                        sale_info = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                        area = re.search(r'(\d+\.?\d+)㎡', sale_info)
                        area = area.group(1) if area else ''
                        sale_num = re.search(r'(\d+)套', sale_info)
                        sale_num = sale_num.group(1) if sale_num else ''
                        ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                        ca_time = re.sub(r'[年月]', '/', ca_time)
                        ca_time = re.sub(r'日', '', ca_time)
                        position = '、'.join(re.findall(r'([a-zA-Z]{0,3}\d+#.*?楼)', pro_name))
                    ca_time = re.sub(r'-', '/', ca_time)
                    pan_time = ''
                    price = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return 1
            except Exception:
                print(url, '解析异常')
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
                # time.sleep(0.5)
                pass
            else:
                self.db.sadd(self.redis_db, link)


def run():
    p = Producer('HbCangzhou:Detail')
    p.run()
    c = Consumer('HbCangzhou:Detail')
    c.run()


if __name__ == '__main__':
    run()
