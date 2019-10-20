# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/13 14:20
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : run_tiancheng.py
# /***
 
from scrapy import cmdline

name = 'tiancheng'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
