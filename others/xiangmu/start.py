# -*- coding: utf-8 -*-
from Beijing.北京 import run as beijing_run
from Fujian.南安 import run as nanan_run
from Fujian.建阳 import run as jianyang_run
from Fujian.泉州 import run as qquanzhou_run
from Fujian.漳州 import run as zhangzhou_run
from Fujian.龙岩 import run as longyan_run
from Fujian.福安 import run as fuan_run
from Guangdong.广州 import run as guangzhou_run
from Guangdong.汕头 import run as shantou_run
from Guangdong.江门 import run as jiangmen_run
from Guangdong.河源 import run as heyuan_run
from Guangdong.珠海2 import run as zhuhai_run
from Guangdong.肇庆 import run as zhaoqing_run
from Guangdong.惠州2 import run as huizhou_run
from Guangxi.南宁 import run as naning_run
from Guangxi.桂林 import run as guiling_run
from Guangxi.贵港 import run as guigang_run
from Hebei.唐山 import run as tangshan_run
from Hebei.张家口 import run as zhangjiakou_run
from Hebei.沧州 import run as cangzhou_run
from Hebei.石家庄 import run as shijiazhuang_run
from Hebei.邯郸 import run as handan_run
from Heilongjiang.哈尔滨 import run as haerbin_run
from Henan.周口 import run as zhoukou_run
from Henan.安阳 import run as anyang_run
from Henan.开封 import run as kaifeng_run
from Henan.新郑 import run as xinzheng_run
from Henan.洛阳 import run as luoyang_run
from Henan.驻马店 import run as zhumadian_run
from Henan.郑州 import run as zhengzhou_run
from Liaoning.沈阳 import run as shenyang_run
from Liaoning.营口 import run as yingkou_run
from Neimenggu.包头 import run as baotou_run
from Shandong.临沂 import run as linyi_run
from Shandong.威海 import run as weihai_run
from Shandong.寿光 import run as shouguang_run
from Shandong.山东青州 import run as qingzhou_run
from Shandong.枣庄 import run as zaozhuang_run
from Shandong.济南 import run as jinan_run
from Shandong.济宁 import run as jining_run
from Shandong.淄博 import run as zibo_run
from Shandong.烟台 import run as yantan_run
from Shandong.邢台 import run as xingtai_run
from Shanxi.晋中 import run as jinzhong_run
from Tianjing.天津2 import run as tianjing_run
from Yunnan.昆明 import run as kunming_run
from Sichuan.乐山 import run as leshan_run
from Sichuan.泸州 import run as luzhou_run
from multiprocessing import Process

if __name__ == '__main__':
    p = Process(target=anyang_run)
    p.start()
    p = Process(target=huizhou_run)
    p.start()
    p = Process(target=baotou_run)
    p.start()
    p = Process(target=jiangmen_run)
    p.start()
    p = Process(target=beijing_run)
    p.start()
    p = Process(target=cangzhou_run)
    p.start()
    p = Process(target=fuan_run)
    p.start()
    p = Process(target=guangzhou_run)
    p.start()
    p = Process(target=guigang_run)
    p.start()
    p = Process(target=guiling_run)
    p.start()
    p = Process(target=haerbin_run)
    p.start()
    p = Process(target=handan_run)
    p.start()
    p = Process(target=heyuan_run)
    p.start()
    p = Process(target=jianyang_run)
    p.start()
    p = Process(target=jinan_run)
    p.start()
    p = Process(target=jining_run)
    p.start()
    p = Process(target=jinzhong_run)
    p.start()
    p = Process(target=kaifeng_run)
    p.start()
    p = Process(target=kunming_run)
    p.start()
    p = Process(target=leshan_run)
    p.start()
    p = Process(target=linyi_run)
    p.start()
    p = Process(target=longyan_run)
    p.start()
    p = Process(target=luoyang_run)
    p.start()
    p = Process(target=luzhou_run)
    p.start()
    p = Process(target=nanan_run)
    p.start()
    p = Process(target=naning_run)
    p.start()
    p = Process(target=qingzhou_run)
    p.start()
    p = Process(target=qquanzhou_run)
    p.start()
    p = Process(target=shantou_run)
    p.start()
    p = Process(target=shenyang_run)
    p.start()
    p = Process(target=shijiazhuang_run)
    p.start()
    p = Process(target=shouguang_run)
    p.start()
    p = Process(target=weihai_run)
    p.start()
    p = Process(target=xingtai_run)
    p.start()
    p = Process(target=xinzheng_run)
    p.start()
    p = Process(target=yantan_run)
    p.start()
    p = Process(target=yingkou_run)
    p.start()
    p = Process(target=zaozhuang_run)
    p.start()
    p = Process(target=zhangjiakou_run)
    p.start()
    p = Process(target=zhangzhou_run)
    p.start()
    p = Process(target=zhaoqing_run)
    p.start()
    p = Process(target=zhengzhou_run)
    p.start()
    p = Process(target=zhoukou_run)
    p.start()
    p = Process(target=zhuhai_run)
    p.start()
    p = Process(target=zhumadian_run)
    p.start()
    p = Process(target=zibo_run)
    p.start()
    p = Process(target=tianjing_run)
    p.start()
    p = Process(target=tangshan_run)
    p.start()
