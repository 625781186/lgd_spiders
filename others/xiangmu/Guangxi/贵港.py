# -*- coding: utf-8 -*-
import requests
from lxml import etree
from common.spider_class import TongyongSpider
from common.update_mongo import Update
from common.update_mongo import Update2
import datetime
import re

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'guigang'


class Guigang(TongyongSpider):
    url = 'http://www.ggsfcw.com/xsxk.aspx?t=2'

    def parse_detail(self):
        for i in range(1,5):
            try:
                response = requests.get(self.url, headers=self.headers,timeout=40)
                text = response.text
                html = etree.HTML(text)
                divs = html.xpath('//div[@class="post-right"]')
                for div in divs:
                    ca_num = ''.join(div.xpath('./h4//text()'))[5:]
                    pro_info = ''.join(div.xpath('./p[1]//text()'))
                    if pro_info:
                        pro_name = pro_info.split('幢')[0][5:-1]
                        position = '幢' + pro_info.split('幢')[1]
                    else:
                        pro_name = ''
                        position = ''
                    ca_time = ''.join(div.xpath('./p[2]//text()'))
                    ca_time = ca_time[5:] if ca_time else ''
                    ca_time = re.sub(r'-', '/', ca_time)
                    pan_time = ''
                    price = ''
                    sale_num = ''
                    area = ''
                    company = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, self.url)
                    print(build)
                    Update2(build, city)
            except Exception as e:
                print(e)

def run():
    obj = Guigang('GxGuigang:Detail')
    obj.parse_detail()


if __name__ == '__main__':
    run()
