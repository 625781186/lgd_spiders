# -*- coding: utf-8 -*-
import requests
import re
import time
import json
from common.update_mongo import Update
from common.update_mongo import Update2
from common.spider_class import TongyongSpider
import datetime

now = datetime.datetime.now().strftime('%Y/%m/%d')
city = 'leshan'


# 不要少提供参数，有频率限制
# 预售套数=上市套数，添加字段项目地址

class LeshanSpider(TongyongSpider):
    first_url = 'http://szjj.leshan.gov.cn/szjj/spf/listspf.shtml'
    url = 'http://szjj.leshan.gov.cn/LSZJJ/commercial/commercialSelectB.do'

    def parse_page(self, data):
        for i in range(1, 5):
            try:
                response = requests.post(self.url, headers=self.headers, data=data,timeout=40)
                text = response.content.decode('utf-8')
                content = json.loads(text)
                print(content)
                datas = content['DATA']
                for data in datas:
                    ca_num = data['LICENCENO']
                    ca_num = '' if ca_num == None else ca_num
                    pro_name = data['PROJECT']
                    pro_name = '' if pro_name == None else pro_name
                    sale_num = data['HOUSENUM']
                    sale_num = '' if sale_num == None else str(sale_num)
                    sale_time = data['REGIDATE']
                    sale_time = '' if sale_time == None else sale_time
                    sale_time = re.sub(r'-', '/', sale_time)
                    company = data['UNITNAME']
                    pan_time = sale_time
                    price = ''
                    area = ''
                    ca_time = ''
                    position = ''
                    url = self.first_url
                    build = (pro_name, ca_num, ca_time, pan_time, sale_num, area, price, position, company, now, url)
                    print(build)
                    Update2(build, city)
                return
            except Exception as e:
                print(data, e)

    def run(self):
        for i in range(1, 99):
            data = {
                'page': '{}'.format(i),
                'project': '',
                'unit': '',
                'cedo': '',
                'redionCode': '511102'
            }
            self.parse_page(data)
            time.sleep(5)


def run():
    obj = LeshanSpider('ScLeshan:Detail')
    obj.run()


if __name__ == '__main__':
    run()
