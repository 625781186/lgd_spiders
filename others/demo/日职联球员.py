import requests
from lxml import etree
import re,os,time

# from japan_basketball import BleaguejpBasketballPlayer
# from orm_session import MysqlSvr
# MysqlSvr.set_env('local')
# spx_dev_session = MysqlSvr.get('local')
# from change_time import *

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'counts=1; LUCBLEAGUE_SLANG=ja; LUCBLEAGUE_TLANG=en; LUCBLEAGUE_XMODE=0; LUCBLEAGUE_XJSID=0; LUCBLEAGUE_KEY1=3vccyRicTUh/FlX4lJkywEHrydDbA+JmeA8ao7SX2LE5N9LLkhEbCLDvGwk3UYJKXM8Q5W3Ed2krvNlbLy0abeMMHDkogb1YcUYE1NWQLxg=; LUCBLEAGUE_KEY2=3vccyRicTUh/FlX4lJkywEHrydDbA+JmeA8ao7SX2LE5N9LLkhEbCLDvGwk3UYJKXM8Q5W3Ed2krvNlbLy0abeMMHDkogb1YcUYE1NWQLxg=; _gcl_au=1.1.1162332093.1570685325; _ga=GA1.2.1517002990.1570685325; _gid=GA1.2.98352727.1570685325; _fbp=fb.1.1570685996040.261506657; refresh=manual',
'Host': 'translation2.j-server.com',
'Referer': 'https://translation2.j-server.com/LUCBLEAGUE/ns/tl.cgi/https://www.bleague.jp/club/?SLANG=ja&TLANG=en&XMODE=0&XCHARSET=utf-8&XJSID=0',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}
url='https://translation2.j-server.com/LUCBLEAGUE/ns/tl.cgi/https://www.bleague.jp/club/?SLANG=ja&TLANG=en&XMODE=0&XCHARSET=utf-8&XJSID=0'

'mysql+pymysql://root:wuqing6691878A@192.168.1.166/leisu_dev?charset=utf8mb4&autocommit=true'

def down_url(url):
    response=requests.get(url,headers=headers).text
    selector = etree.HTML(response)
    return selector

def get_list(selector):
    ls=selector.xpath('//ul[@class="club-circle-list"]/li')
    print(len(ls))
    return ls
#球员的具体信息---
def get_realinfos(href,id,qiudui_id,player_weizhi):
    se = down_url(href)
    player_touxiang = se.xpath('//*[@id="contents_inner"]/div/section[2]/div[1]/img/@src')[0]
    player_number = se.xpath('//*[@id="contents_inner"]/div/article/header/div/h1/text()')[0]
    player_name = se.xpath('//*[@id="contents_inner"]/div/article/header/div/p[1]/text()')[0]

    player_mater = se.xpath('//*[@id="contents_inner"]/div/article/section[1]/div/table/tbody/tr[1]/td/text()')[0]
    player_Hometown = se.xpath('//*[@id="contents_inner"]/div/article/section[1]/div/table/tbody/tr[2]/td/text()')[0]
    player_birthday = se.xpath('//*[@id="contents_inner"]/div/article/section[1]/div/table/tbody/tr[3]/td/text()')[0]

    palyer_high = se.xpath('//*[@id="contents_inner"]/div/article/section[1]/div/table/tbody/tr[4]/td/text()')[0].replace('cm','')
    palyer_weight = se.xpath('//*[@id="contents_inner"]/div/article/section[1]/div/table/tbody/tr[5]/td/text()')[0].replace('kg','')

    palyer_Nationality = se.xpath('//*[@id="contents_inner"]/div/article/section[1]/div/table/tbody/tr[6]/td/text()')[0]
    #头像下载
    # print(player_touxiang)
    # player_birthday = get_birthday(player_birthday)
    res = requests.get(player_touxiang).content
    with open('./qiudui_qiuyuan_touxiang/' + id + '.webp', 'wb') as f_w:
        f_w.write(res)
    data_dict = {
        # '球员图片': player_touxiang,
        'id': int(id),              #int
        'key':id,                   #str
        'sport_id':2,               #int
        'shirt_number': int(player_number),     #int
        'name_en': player_name,                 #str
        'detailed_positions': player_weizhi,    #str
        'school': player_mater,                 #str
        'city': player_Hometown,                #str
        # 'birthday': int(player_birthday),            #int
        'height': int(palyer_high),             #int
        'weight': int(palyer_weight),           #int
        'nationality': palyer_Nationality,      #str
        'team_id': int(qiudui_id),              #int
        # '球队名称': qiuduiname,
    }
    # BleaguejpBasketballPlayer.upsert(
    #     spx_dev_session,
    #     'id',
    #     data_dict
    # )
    print(data_dict)

    # data_dict = {
    #     'id': int(player_id),        球员id
    #     'key': player_id,            球员id
    #     'sport_id': 2,               球类id
    #     'team_id': team_id_dict[team_href],   球队id
    #     'name_zh': player_name_zh,           球员名称
    #     'logo': logo,                    球员头像
    #     'birthday': player_dob,          球员生日
    #     'weight': player_weight,          体重
    #     'height': player_height,          身高
    #     'league_career_age': player_experience,
    #     'shirt_number': player_jerseyno,
    # }
    # print(data_dict)



#每个球队球员的具体url以及球员id
def get_paylerinfo(href,qiudui_id):
    #每一页球队的值
    ss = down_url(href)
    qiudui_name = ss.xpath('//*[@id="contents_inner"]/div/article/div[1]/section[1]/div/h1/text()')[0]
    # print(qiudui_name)
    list = ss.xpath('//ul[@class="player-list"]/li')
    for i in list:
        ever_player_href=i.xpath('./a/@href')[0]
        pat = re.compile(r'PlayerID=(.*?)&SLANG', re.M | re.S)
        player_id = pat.findall(ever_player_href)[0]
        # palyer_weizhi = i.xpath('.//p[@class="position-name"]/text()')[0]
        try:
            player_weizhi = i.xpath('.//p[@class="position-name"]/text()')[0]
            player_weizhi = player_weizhi.split('/')[-1]
        except:
            player_weizhi = i.xpath('.//p[@class="position-name"]/text()')[0]

        get_realinfos(ever_player_href,player_id,qiudui_id,player_weizhi)

#获取球队的id和url
def get_info(ls):
    for i in ls:
        href=i.xpath('./a/@href')[0]
        pat = re.compile(r'TeamID=(.*?)&SLANG', re.M | re.S)
        qiudui_id = pat.findall(href)[0]
        print('='*50)
        print(href)
        print(qiudui_id)
        get_paylerinfo(href,qiudui_id)
#主方法
if __name__ == '__main__':
    se=down_url(url)
    ls=get_list(se)
    get_info(ls)
    # spx_dev_session.close()