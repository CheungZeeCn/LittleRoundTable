#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
File descriptions in one line

more informations if needed
"""

import os
import random
import string
import datetime
from contextlib import contextmanager
import time
import logging


@contextmanager
def utils_timer(title, print_it=False):
    t0 = time.time()
    begin_str =  "[utils_timer][{}] - begin@[{}]".format(title, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t0)))
    logging.info(begin_str)
    if print_it:
        print(begin_str)
    yield
    t1 = time.time()
    end_str =  "[utils_timer][{}] - end@[{}] last for [{:.2f}]s".format(title, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t1)), t1-t0)
    logging.info(end_str)
    if print_it:
        print(end_str)

@contextmanager
def utils_timer2(title, print_it=False):
    t0 = time.time()
    logging.info(begin_str)
    if print_it:
        print(begin_str)
    yield
    t1 = time.time()
    end_str =  "[utils_timer][{}] - end@[{}] last for [{:.2f}]s".format(title, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t1)), t1-t0)
    logging.info(end_str)
    if print_it:
        print(end_str)

def random_str(length):
    """random but not UNIQ !"""
    return ''.join(random.choice(string.lowercase) for i in range(length))

def make_sure_dir_there(dir_path):
    "check, and create dir if nonexist"
    ret_Val = True

    if not os.path.exists(dir_path):
        try:
            # create directory (recursively)
            os.makedirs(dir_path)
        except OSError:
            ret_val = False
    return ret_val

def now_date_str(format_str="%Y%m%d%H%M%S"):
    return datetime.datetime.strftime(datetime.datetime.now(), format_str)


if __name__ == '__main__':
    pass

