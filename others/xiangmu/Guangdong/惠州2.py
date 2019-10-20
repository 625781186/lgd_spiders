# -*- coding: utf-8 -*-
from lxml import etree
import re
import time
from common.update_mongo import Update2
import datetime
import requests
from urllib import parse

city = 'huizhou'
now = datetime.datetime.now().strftime('%Y/%m/%d')


# 会检测ip
class Consumer():
    url = 'http://113.106.199.148/web/salepermit.jsp?page={}&projectname=&code=&compname=&&address=&date1=&date2='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    def parse_detail(self, url):
        for i in range(1, 10):
            try:
                response = requests.get(url, headers=self.headers,timeout=40)
                text = response.content.decode('gb18030')
                html = etree.HTML(text)
                table = html.xpath('//table')[0]
                trs = table.xpath('.//tr')[1:]
                for tr in trs:
                    ca_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[2]//text()')))
                    pro_name = re.sub(r'\s', '', ''.join(tr.xpath('./td[3]//text()')))
                    company = re.sub(r'\s', '', ''.join(tr.xpath('./td[4]//text()')))
                    sale_num = re.sub(r'\s', '', ''.join(tr.xpath('./td[5]//text()')))
                    sale_num = re.sub(r'\.0', '', sale_num)
                    area = re.sub(r'\s', '', ''.join(tr.xpath('./td[6]//text()')))
                    ca_time = re.sub(r'\s', '', ''.join(tr.xpath('./td[7]//text()')))
                    pan_time = ''
                    price = ''
                    post_data = parse.quote(ca_num, encoding='gb18030')
                    post_url = 'http://113.106.199.148/web/salepermitinfo.jsp?ctemp='
                    response = requests.get(post_url + post_data, headers=self.headers,timeout=40)
                    text = response.content.decode('gb18030')
                    html = etree.HTML(text)
                    position = re.sub(r'\s', '', ''.join(html.xpath('//table//tr[7]/td[2]//text()')))
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return 1
            except Exception as e:
                print(url, e)
                if i == 9:
                    return 1

    def run(self):
        for i in range(1, 103):
            self.parse_detail(self.url.format(i))


def run():
    c = Consumer()
    c.run()


if __name__ == '__main__':
    run()
