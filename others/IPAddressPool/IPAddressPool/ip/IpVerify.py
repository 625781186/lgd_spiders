import requests
import re
import traceback, json


def testBaidu(db_ip):
    try:
        ip = {
            "https": "https://%s" % (db_ip),
            "http": "http://%s" % (db_ip),
        }
        r = requests.get('http://www.baidu.comp', proxies=ip, timeout=8)   #验证ip

        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False


