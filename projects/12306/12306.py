# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 14:52
# @Author  : LGD
# @File    : 12306.py
# @功能    : 爬取12306的车票信息

import json
import requests
import datetime
from colorama import init, Fore
from prettytable import PrettyTable

init(autoreset=False)


# 获取车站的版本信息，进而获取车站的全拼，简拼，代码等信息
def get_station_version(stations):
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9110'
    html_text = requests.get(url).text
    # 去掉文本总最后多余的两个符号，并以@符号进行分割，第一项不是有用的信息
    infos = html_text[:-2].split("@")[1:]
    for info in infos:
        station_list = info.split("|")
        # 将车站的代码作为键,汉字，全拼，简拼作为值
        stations[station_list[2]] = {'cn': station_list[1], 'qp': station_list[3], 'jp': station_list[4]}


# 出发站，到达站的判断
def station_info(stations, input_station):
    while 1:
        index = 0
        results = []
        station_results = []
        for k, v in stations.items():
            if input_station in v.values():
                index += 1
                station_results.append([k, v])
                results.append([index, k, v['cn']])
        if index == 0:
            input_station = input("您输入的车站不存在,请重新输入站点：").strip()
        # 输入的信息唯一
        elif index == 1:
            # print(station_results[0])
            station_code = station_results[0][0]
            return station_code
            break
        # 输入的信息模糊，不能直接判断出你想输入的站点，需要作出一个选择
        else:
            for result in results:
                print(result[0], result[1], result[2])
            select = int(input("请输入你的选择（序号）："))
            for i in range(1, len(results)):
                if select == i:
                    print(results[i - 1])
                    station_code = station_results[i - 1][0]
                    return station_code
            break


# 出发日期的判断
def riqi_info(input_riqi):
    # 用一个列表去存放可以查出车票的日期
    riqi_list = []
    today_riqi = datetime.date.today()
    for i in range(15):
        tianshu = datetime.timedelta(days=i)
        riqi_list.append(str(today_riqi + tianshu))
    # 输入合理的日期则跳出，否则一直输入
    while 1:
        if input_riqi in riqi_list:
            return input_riqi
            break
        else:
            print("您输入的日期有误，请输入未来十五天内的日期进行查询！")
        input_riqi = input("请输入出发的日期（2019-01-01）：").strip()


# 对链接进行解析，获取需要的信息的位置
def get_station_list(stations, chufa_riqi, chufa_code, daoda_code, tickets):
    train_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(chufa_riqi, chufa_code, daoda_code)
    headers = {
        'Cookie': 'JSESSIONID=7BA03CA586C52BEC5797683D0BC3715E; BIGipServerotn=921698826.38945.0000; RAIL_EXPIRATION=1569366681588; RAIL_DEVICEID=BewwRve1ByzOssNRzZnQ_6OtinbVxZvA8xvWZdY5kYOT6_AuiWym3TONFIoJGpuye9NEWSjFEFMYqlSIRu0dyay2JFJCBuOb_pUkux0o-dshHwrbKWk4ZqhR3vJC_ezURqsIsn6vEj0pZeiTYMRZz8aw6tF-P2Hb; BIGipServerpool_passport=200081930.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2019-09-21; _jc_save_toDate=2019-09-21; _jc_save_wfdc_flag=dc',
        'Host': 'kyfw.12306.cn',
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # 处理json格式的文件
    web_data = requests.get(train_url, headers=headers)
    print(web_data.json())
    # 获取data
    json_data = web_data.json()['data']
    # 获取result
    json_result = json_data['result']

    # 针对每个链接，我们进行处理
    for ticket in json_result:
        # 通过|对每个链接进行分割，分别获取我们所需信息对应的索引
        ticket_list = ticket.split("|")
        yuding = ticket_list[1]
        # 车次在索引为3的位置，以下类似
        checi = ticket_list[3]
        shifa_codes = ticket_list[4]
        zhongdian_codes = ticket_list[5]
        from_code = ticket_list[6]
        to_code = ticket_list[7]
        chufa_time = ticket_list[8]
        daoda_time = ticket_list[9]
        total_time = ticket_list[10]
        vip = ticket_list[32]
        yideng = ticket_list[31]
        erdeng = ticket_list[30]
        gaoji_ruanwo = ticket_list[21]
        yideng_ruanwo = ticket_list[23]
        erdeng_ruanwo = ticket_list[28]
        dongwo = ticket_list[33]
        yingzuo = ticket_list[29]
        wuzuo = ticket_list[26]
        qita = "--"

        # 链接的部分
        train_no = ticket_list[2]
        from_station_no = ticket_list[16]
        to_station_no = ticket_list[17]
        seat_types = ticket_list[35]

        for s in stations:
            if from_code in s:
                from_station = stations[s]["cn"]
            if to_code in s:
                to_station = stations[s]["cn"]

        get_price_info(tickets, checi, from_station, to_station, chufa_time, daoda_time, total_time, vip, yideng,
                       erdeng, gaoji_ruanwo, yideng_ruanwo, erdeng_ruanwo, dongwo, yingzuo, wuzuo, train_no,
                       from_station_no, to_station_no, seat_types, chufa_riqi, qita, yuding)


# 得到价格信息
def get_price_info(tickets, checi, from_station, to_station, chufa_time, daoda_time, total_time,
                   vip, yideng, erdeng,gaoji_ruanwo, yideng_ruanwo, erdeng_ruanwo, dongwo, yingzuo,
                   wuzuo, train_no, from_station_no,to_station_no, seat_types, chufa_riqi, qita, yuding):
    link = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}'.format(
        train_no, from_station_no, to_station_no, seat_types, chufa_riqi)
    try:

        headers = {
            'Cookie': 'JSESSIONID=97E3C353B9841B85453AEFBCAC296709; BIGipServerotn=217055754.64545.0000; RAIL_EXPIRATION=1571648265065; RAIL_DEVICEID=tntDyjgtOiBjVsFge7BzxfbhuA6U6j-1S8g7ztW3Yce_w3NHLxUZGFTn-uLd0rKsNuFqgodHbb_CvCwvEWl-mMe5_x0ND3nGGJD4CgZM6W2r0U70FNg8B13NVTqEwXZT1Nn7DfdMKJ0wf--wHNaH6ABvvt-JpMtw; BIGipServerpool_passport=183304714.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_toDate=2019-10-17; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2019-10-18',
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        link_text = requests.get(link, headers=headers)
        # print(link_text.text)
        link_json = link_text.json()['data']
        # 解析是什么座位，并加上颜色
        # print(link_json)

        for j in link_json:
            if j == 'A9':
                vip = vip + "\n" + (Fore.LIGHTBLUE_EX + link_json['A9'] + Fore.RESET)
            if j == 'P':
                vip = vip + "\n" + (Fore.LIGHTBLUE_EX + link_json['P'] + Fore.RESET)
            if j == 'M':
                yideng = yideng + "\n" + (Fore.LIGHTBLUE_EX + link_json['M'] + Fore.RESET)
            if j == 'O':
                erdeng = erdeng + "\n" + (Fore.LIGHTBLUE_EX + link_json['O'] + Fore.RESET)
            if j == 'A6':
                gaoji_ruanwo = gaoji_ruanwo + "\n" + (Fore.LIGHTBLUE_EX + link_json['A6'] + Fore.RESET)
            if j == 'A4':
                yideng_ruanwo = yideng_ruanwo + "\n" + (Fore.LIGHTBLUE_EX + link_json['A4'] + Fore.RESET)
            if j == 'F':
                dongwo = dongwo + "\n" + (Fore.LIGHTBLUE_EX + link_json['F'] + Fore.RESET)
            if j == 'A3':
                erdeng_ruanwo = erdeng_ruanwo + "\n" + (Fore.LIGHTBLUE_EX + link_json['A3'] + Fore.RESET)
            if j == 'A1':
                yingzuo = yingzuo + "\n" + (Fore.LIGHTBLUE_EX + link_json['A1'] + Fore.RESET)
            if j == 'WZ':
                wuzuo = wuzuo + "\n" + (Fore.LIGHTBLUE_EX + link_json['WZ'] + Fore.RESET)
        color_list = get_color_info(checi, from_station, to_station, chufa_time, daoda_time)

        # 为了使出发站和到达站，出发时间和到达时间显示在一行，所以加换行
        tickets.append(
            [color_list[2], color_list[0] + '\n' + color_list[1] + '\n', color_list[3] + '\n' + color_list[4] + '\n',
             total_time, vip, yideng, erdeng, gaoji_ruanwo, yideng_ruanwo, erdeng_ruanwo, dongwo, yingzuo, wuzuo, qita,
             yuding])

        # 为了使出发站和到达站，出发时间和到达时间显示在一行，所以加换行
        tickets.append(
            [color_list[2], color_list[0] + '\n' + color_list[1] + '\n', color_list[3] + '\n' + color_list[4] + '\n',
             total_time, vip, yideng, erdeng, gaoji_ruanwo, yideng_ruanwo, erdeng_ruanwo, dongwo, yingzuo, wuzuo, qita,
             yuding])

    except:
        # print('车票信息获取失败！')
        pass


# 将车次，出发站，到达站，出发时间，到达时间的颜色做改变
def get_color_info(checi, from_station, to_station, chufa_time, daoda_time):
    # 更改颜色，车次，出发站，到达站，出发时间，到达时间
    from_station = Fore.LIGHTRED_EX + from_station + Fore.RESET
    to_station = Fore.LIGHTGREEN_EX + to_station + Fore.RESET
    checi = Fore.LIGHTYELLOW_EX + checi + Fore.RESET
    chufa_time = Fore.LIGHTRED_EX + chufa_time + Fore.RESET
    daoda_time = Fore.LIGHTGREEN_EX + daoda_time + Fore.RESET
    color_list = [from_station, to_station, checi, chufa_time, daoda_time]
    return color_list


# 使用prettytable模块表格化的输出信息
def print_station_infos(tickets):
    # 加个表头信息，并以空格进行分割
    ptable = PrettyTable('车次 出发站/到达站 出发时间/到达时间 历时 商务座 一等座 二等座 高级软卧 软卧一等座 硬卧二等座 动卧 硬座 无座 其他 预定'.split())

    # 如果没有车票信息，则打印出‘--’
    for t_info in tickets:
        for i in range(len(t_info)):
            if t_info[i] == '':
                t_info[i] = '--'
        # 将每个车次的信息加入到表中，即表的一行
        ptable.add_row(t_info)
    print(ptable)


# 主函数，程序的入口
if __name__ == '__main__':
    stations = {}
    tickets = []
    get_station_version(stations)  ##获取车站的版本信息，进而获取车站的全拼，简拼，代码等信息

    chufa_station = input("请输入出发站：").strip()
    chufa_code = station_info(stations, chufa_station)
    daoda_station = input("请输入到达站：").strip()
    daoda_code = station_info(stations, daoda_station)
    input_riqi = input("请输入出发的日期（2019-01-01）：").strip()
    chufa_riqi = riqi_info(input_riqi)

    get_station_list(stations, chufa_riqi, chufa_code, daoda_code, tickets)  ##对链接进行解析，获取需要的信息的位置
    print_station_infos(tickets)  # 使用prettytable模块表格化的输出信息



