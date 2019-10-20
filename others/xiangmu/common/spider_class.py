# coding=utf-8
import pymongo
import redis
from conf.settings import REDIS_HOST
from conf.settings import REDIS_PORT


class TongyongSpider(object):
    db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def __init__(self, redis_db):
        # self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        # self.client = pymongo.MongoClient('mongodb://root:123456@127.0.0.1:27017')
        self.redis_db = redis_db
