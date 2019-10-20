# -*- coding: utf-8 -*-
import redis
db=redis.StrictRedis(host='192.168.1.77',port=6379,decode_responses=True,db=10)
print()