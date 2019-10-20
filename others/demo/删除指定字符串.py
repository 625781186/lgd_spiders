# -*- coding: utf-8 -*-
# @Time    : 2019/10/16 15:25
# @Author  : LGD
# @File    : 删除指定字符串.py
# @功能    :

import re


str1 = """jads
fha
* dafjhkjghakfjghadkf
akjdshfkjsd
* dsfkjasdhkfjhs
jjjkj
"""

res = re.sub(r'\*(.*)\n', '', str1)
print(res)


