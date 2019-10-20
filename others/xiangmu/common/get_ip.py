# -*- coding: utf-8 -*-
import redis
from conf.settings import REDIS_HOST
from conf.settings import REDIS_PORT


def get_proxy():
    db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    ip = db.srandmember('ProxiesIP')
    proxy = {
        'http': '%s' % ip,
        'https': '%s' % ip
    }
    return proxy

get_proxy()
