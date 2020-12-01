#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    work 服务, 一个进程，监听一个端口
        当请求到达的时候
            如果是new
                生成一个session/context, 存,
            如果是update
                加载对应session/context, 存(如果不存在)

    todo: 流量分发, redis/file session的支持, 关键节点日志, 路由优化
"""

import kp_setup
import os
import os.path
import logging
import collections
import json

import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import time

from confs import conf
from libs import DialogueManager
from libs import Session

define("port", default=10810, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")
define("worker_name", default="worker_10810", help="worker name is need, and be unique in cluster")


def print_reply(context, reply):
    """
        debug 用
    :param context:
    :param reply:
    :return:
    """
    tmpl = \
"""
=====================
feedback: {}
---------
机器人: {}
tips: {}
now_turn_block_id: {}
next_turn_block_id: {}
now_segment_id: {}
next_segment_id: {}
---------
context:
{}
=====================
"""
    print(tmpl.format(reply['feedback'], reply['reply'], reply['tips'], context['now_turn_block_id'],
                      context['next_turn_block_id'], context['now_segment_id'], context['next_segment_id'], context))

def talk_on_console():
    """
        可以作为一个简单的调试工具来调用
    :return:
    """
    # new 一个 dm
    dm = DialogueManager.DialogueManager()
    script_data_path = os.path.join(kp_setup.data_dir, conf.scripts_file_name)
    # 加载 剧本
    dm.load_scripts(data_format='json', uri=script_data_path)
    # 看看 剧本
    print(dm.scripts)

    # new 一个对话
    context, reply, _ = dm.new(1, 'zhangzhi', 1)
    print_reply(context, reply)

    while True:
        # 输入
        user_answer = input('请回答:')
        # 输出
        print("您输入了:", user_answer)
        context, reply, next_status = dm.do_reply(context, user_answer)
        print_reply(context, reply)
        # 是否结束
        if next_status == 'end':
            logging.info("session:{} user_id:{} END".format(context['session_id'], context['user_id']))
            break


class DialogueHandler(tornado.web.RequestHandler):
    dm = None
    session = None

    @classmethod
    def setup(cls):
        logging.info("in init setup")
        if cls.dm is None:
            logging.info("init dm for worker: {}".format(options.worker_name))
            dm = DialogueManager.DialogueManager()
            script_data_path = os.path.join(kp_setup.data_dir, conf.scripts_file_name)
            # 加载 剧本
            dm.load_scripts(data_format='json', uri=script_data_path)
            cls.dm = dm
            session = Session.LruSession(conf.SESSION_MEM_PER_WORKER, callback=Session.log_drop_session_info)
            cls.session = session
            logging.info("init dm for worker: {} DONE".format(options.worker_name))

    def initialize(self):
        """
            每次请求 initialize 都会默认被调用(每次请求过来, DialogueHandler 的实例都不一样)
            这里面每次用来检查类变量dm是否被初始化, 保证其永远可用
        :return:
        """
        DialogueHandler.setup()
        self.body_data_dict = None

    @staticmethod
    def pack_response(code, msg='', data={}):
        code_msg = conf.STATUS_CODE_MSG[code]
        ret_msg = "{} [{}]".format(code_msg, msg)
        ret = {"code": code, "msg": ret_msg, "data": data}
        return ret

    def get_body_data(self):
        body_data = collections.defaultdict(str)
        try:
            if self.request.body is None or self.request.body == b'':
                return body_data
            body_data.update(json.loads(self.request.body))
        except Exception as e:
            logging.warning("unpack json body error: {}".format(e))
            return None
        return body_data

    def prepare(self):
        # check body
        body_data = self.get_body_data()
        logging.info("got request:{}".format(body_data))
        # simply check
        if body_data is None:
            resp = self.pack_response(3)
            self.write(json.dumps(resp))
            return None
        self.body_data_dict = body_data

    def post(self):
        #time.sleep(10)
        #DialogueHandler.setup()
        action = self.get_query_argument('action')
        session_id = self.get_query_argument('session_id', None)

        if action == 'new':
            user_id = self.body_data_dict.setdefault('openId', 'default_user')
            difficulty = self.body_data_dict.setdefault('difficultyLevel', 0.5)
            difficulty = float(difficulty)
            script_id = self.body_data_dict.setdefault('scriptId', 1)
            script_id = int(script_id)
            if session_id is None or session_id == '':
                context, reply, next_status = self.dm.new(script_id, user_id, difficulty)
            else:
                context, reply, next_status = self.dm.new(script_id, user_id, difficulty, session_id)
            if next_status == 'error':
                resp = self.pack_response(4, reply['error_msg'])
                self.write(json.dumps(resp))
                return None
            self.session.insert_kv(context['session_id'], context)
            self.write(json.dumps(self.pack_response(
                0, data=self.format_reply_data(reply, context, next_status, self.dm.scripts[script_id]))))

        elif action == 'reply':
            user_answer = self.body_data_dict['agentAnswer']
            session_id = self.body_data_dict['sessionId']
            context = self.session.lookup_key(session_id)
            if context is None:
                next_status = "error"
                msg = 'no this session {}'.format(session_id)
                resp = self.pack_response(2, msg)
                self.write(json.dumps(resp))
                return None
            else:
                context, reply, next_status = self.dm.do_reply(context, user_answer)
                if next_status == 'error':
                    resp = self.pack_response(4, reply['error_msg'])
                    self.write(json.dumps(resp))
                    return None
                self.write(json.dumps(self.pack_response(0, data=self.format_reply_data(reply, context, next_status))))

    @classmethod
    def format_reply_data(self, reply, context, next_status, script=None):
        """
            拼凑 回复的 data 部分内容
        :param reply:
        :param context:
        :param next_status:
        :param script:
        :return:
        """
        ret_data = {}

        if context is not None:
            ret_data['openId'] =  context['user_id']
            ret_data['session_id'] = context['session_id']
            ret_data['robotAnswer'] = reply['reply']
            ret_data['tips'] = reply['tips']
            ret_data['segmentId'] = context['next_segment_id']
            ret_data['nodeId'] = context['next_turn_block_id']
            ret_data['nowSegmentId'] = context['now_segment_id']
            ret_data['nowNodeId'] = context['now_turn_block_id']
            ret_data['scoreSituation'] = reply['feedback']
            ret_data['nextStatus'] = next_status

            if script is not None:
                ret_data['scriptContent'] = script

        return ret_data

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", DialogueHandler),
        ],
        # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        # template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # static_path=os.path.join(os.path.dirname(__file__), "static"),
        # xsrf_cookies=True, todo 前端加入这块支持
        debug=options.debug,
    )
    app.listen(options.port)
    logging.info("worker_name: {} Listening port: {}".format(options.worker_name, options.port))
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
