# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 16:19
# @Author  : LGD
# @File    : trains_infos.py
# @功能    : 获取指定车站间，指定时间段的车次信息

import requests
url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-09-21&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'

headers = {
    'Cookie': 'JSESSIONID=7BA03CA586C52BEC5797683D0BC3715E; BIGipServerotn=921698826.38945.0000; RAIL_EXPIRATION=1569366681588; RAIL_DEVICEID=BewwRve1ByzOssNRzZnQ_6OtinbVxZvA8xvWZdY5kYOT6_AuiWym3TONFIoJGpuye9NEWSjFEFMYqlSIRu0dyay2JFJCBuOb_pUkux0o-dshHwrbKWk4ZqhR3vJC_ezURqsIsn6vEj0pZeiTYMRZz8aw6tF-P2Hb; BIGipServerpool_passport=200081930.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2019-09-21; _jc_save_toDate=2019-09-21; _jc_save_wfdc_flag=dc',
    'Host': 'kyfw.12306.cn',
    'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# 处理json格式的文件
web_data = requests.get(url, headers=headers)
print(web_data.json())