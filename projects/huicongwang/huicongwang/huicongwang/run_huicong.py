# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/13 17:16
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : run_huicong.py
# /***
 

from scrapy import cmdline

name = 'huicong'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
