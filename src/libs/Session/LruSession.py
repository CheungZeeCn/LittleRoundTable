#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   QueueSession.py    
@Contact :   zhangz

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
23/8/19 上午11:22   zhangz     1.0         None
'''

#from . import pylru
from . import pylru
import logging


class LruSession(object):
    """
        固定大小的内存session
        LRU 算法来保证高性能的同时限制内存占用, 当会话超过size的时候，丢最老的会话
        todo 对接redis, 针对sesison，可以在set redis的时候设置超时时间自动老化
    """
    def __init__(self, size, callback=None):
        self.session_cache = pylru.lrucache(size, callback)

    def lookup_key(self, key):
        try:
            value = self.session_cache[key]
        except KeyError as e:
            logging.error(e)
            return None
        return value

    def insert_kv(self, key, value):
        self.session_cache[key] = value
        return True

    def del_key(self, key):
        del self.session_cache[key]
        return True

def log_drop_session_info(key, value):
    logging.warning("LRU DELETE session: {} -> {}".format(key, value))

if __name__ == '__main__':
    lru_session = LruSession(2, callback=emit_all_back)
    #print(lru_session.lookup_key("a"))
    print(lru_session.insert_kv("a", 123), list(lru_session.session_cache.items()))
    print(lru_session.insert_kv("a", 123), list(lru_session.session_cache.items()))
    print(lru_session.insert_kv("b", 456), list(lru_session.session_cache.items()))
    print(lru_session.insert_kv("b", 789), list(lru_session.session_cache.items()))
    print(lru_session.insert_kv("c", 111), list(lru_session.session_cache.items()))
    print(lru_session.insert_kv("d", 222), list(lru_session.session_cache.items()))



