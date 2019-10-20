# coding=utf-8
from common.spider_class import TongyongSpider
from common.update_mongo import Update2
import requests
from lxml import etree
import re
import time
import datetime
import os

path = os.path.dirname(__file__)
file = 'city.txt'

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'quanzhou'


# 少部分预售许可证是图片形式，这部分信息没有抓取
class QuanzhouSpider(TongyongSpider):
    url = 'http://qz.loupan.com/news/list-134-{}.html'

    def parse_detail(self, url):
        for i in range(1, 5):
            try:
                response = requests.get(url, headers=self.headers,timeout=30)
                text = response.text
                html = etree.HTML(text)
                sale_num = re.search(r'(\d+)套', ''.join(html.xpath('//h1//text()')))
                sale_num = sale_num.group(1) if sale_num else ''
                content = re.sub(r'\s', '', ''.join(html.xpath('//div[@class="content_text"]//text()')))
                company = re.search(r'开发商:?：?(.*公司)', content)
                company = company.group(1) if company else ''
                pro_name = re.search(r'项目名称：(.*?)(预售许可证|开发商|预售许可号|预售证号|坐落|预售范围|预售面积|批准时间)', content)
                if pro_name:
                    position = re.search(r'预售范围：(.*?)</p', text, re.S).group(1)
                    position = re.sub(r'<.*?>', '', position)
                    ca_time = re.search(r'<p.*?批准时间：(.*?)</p', text, re.S)
                    if ca_time:
                        ca_time = ca_time.group(1)
                        ca_time = re.sub(r'<.*?>', '', ca_time)
                        ca_time = re.sub(r'&nbsp;', '', ca_time)
                    else:
                        ca_time = re.search(r'(\d+年\d+月\d+日)', content).group(1)
                        ca_time = re.split(r'[年月日]', ca_time)[0] + '/' + re.split(r'[年月日]', ca_time)[1] + '/' + \
                                  re.split(r'[年月日]', ca_time)[2]
                    ca_time = re.sub(r'-', '/', ca_time)
                    pro_name = pro_name.group(1)
                    ca_num = re.search(r'(预售许可号|预售证号|预售许可证).*?：(.*?)(预售许可证|项目名称|开发商|预售许可号|预售证号|坐落|预售范围|预售面积|批准时间)',
                                       content).group(2)
                    ca_num = re.sub(r'&nbsp;', '', ca_num)
                    info = ''.join(html.xpath('//div[@class="content_text"]/p[position()>3]//text()'))
                    area = re.search(r'(预售面积).*?：(.*?)㎡', info)
                    area = area.group(2) if area else ''
                    pan_time = ''
                    price = ''
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                else:
                    print('图片信息')
                    return
            except Exception as e:
                print(url, e)
                if i == 4: return

    def get_links(self, url):
        response = requests.get(url, headers=self.headers,timeout=30)
        text = response.text
        html = etree.HTML(text)
        divs = html.xpath('//div[@class="tit"]')[:-1]
        links = []
        for div in divs:
            href = div.xpath('./a/@href')[0]
            if (href == 'http://qz.loupan.com/html/news/201907/3955189.html') or (
                    href == 'http://qz.loupan.com/html/news/201907/3955167.html'):
                continue
            links.append(href)
        return links

    def run(self):
        for i in range(1, 6):
            url = self.url.format(i)
            links = self.get_links(url)
            for link in links:
                self.parse_detail(link)
                time.sleep(1)


def run():
    try:
        obj = QuanzhouSpider('FjQuanzhou')
        obj.run()
    except Exception as e:
        file_path = os.path.join(path, file)
        with open(file_path, 'at', encoding='utf-8') as fp:
            fp.write(str(e))
            fp.write('\r')


if __name__ == '__main__':
    run()
