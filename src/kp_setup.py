#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2016-11-17 14:20:18 
# Copyright 2016 NONE rights reserved.
"""
一些可能用到的路径的预设置
"""
import os
import os.path
import sys
import logging
import logging.handlers


"""
路径 setup
"""
root_dir = None
dir_name_0 = os.path.basename(os.path.dirname(os.path.abspath(sys.argv[0])))
if dir_name_0 == 'src':
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
else:
    root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


confs_dir = os.path.join(root_dir, 'confs')
data_dir = os.path.join(root_dir, 'data')
model_dir = os.path.join(root_dir, 'models')
output_dir = os.path.join(root_dir, 'output')
logs_dir = os.path.join(root_dir, 'logs')

sys.path.insert(0, root_dir)

from confs import conf
if hasattr(conf, 'log_dir') and conf.log_dir != None:
    logs_dir = conf.log_dir

if hasattr(conf, 'data_dir') and conf.data_dir != None:
    data_dir = conf.data_dir

if hasattr(conf, 'model_dir') and conf.model_dir != None:
    model_dir = conf.model_dir

from libs import logger
logger.initRootLogger(logDir=logs_dir)


def main():
    print("hello world")
    logging.info("test")

logging.info("KP Setup Done, root_dir:[{}]".format(root_dir))

if __name__ == '__main__':
    main()

