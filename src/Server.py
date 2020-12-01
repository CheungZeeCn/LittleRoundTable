#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   Server.py.py    
@Contact :   zhangz

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
28/8/19 上午11:13   zhangz     1.0         None
"""

import kp_setup

import logging
import os
import sys
import json
import collections
import subprocess
import tornado.ioloop
import tornado.httpclient
import tornado.web
from tornado.options import define, options, parse_command_line
import shlex

from libs import DialogueManager
from confs import conf
from libs import utils


define("port", default=conf.SERVER_PORT, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")
define("worker_num", default=conf.WORKER_NUM, help="how many worker?")
define("worker_port_begin", default=conf.WORKER_PORT_BEGIN, help="worker port begin?")

class MainHandler(tornado.web.RequestHandler):

    @staticmethod
    def gen_session_id():
        raw_session_id = DialogueManager.DialogueContext.gen_session_id()
        return "{}_{:010d}".format(utils.now_date_str(), raw_session_id)

    @staticmethod
    def locate_worker(session_id):
        i = hash(session_id) % options.worker_num
        port = options.worker_port_begin + i
        return i, port

    def get_body_data(self):
        body_data = collections.defaultdict(str)
        try:
            if self.request.body is None or self.request.body == b'':
                return body_data
            body_data.update(tornado.escape.json_decode(self.request.body))
        except Exception as e:
            logging.warning("unpack json body error: {}".format(e))
            return None
        return body_data

    @staticmethod
    def pack_response(code, msg='', data={}):
        code_msg = conf.STATUS_CODE_MSG[code]
        ret_msg = "{} [{}]".format(code_msg, msg)
        ret = {"code": code, "msg": ret_msg, "data": data}
        return ret

    def get_body_data_or_return_error(self):
        body_data = self.get_body_data()
        logging.info("got request:{}".format(body_data))
        # simply check
        if body_data is None:
            resp = self.pack_response(3)
            self.write(json.dumps(resp))
            return None
        return body_data

    async def post(self):
        action = self.get_query_argument('action')
        if action == 'new':
            session_id = MainHandler.gen_session_id()
            i_worker, i_port = MainHandler.locate_worker(session_id)
            logging.info("redirect the request to worker:{} | port:{}, with session id:{}".
                         format(i_worker, i_port, session_id))
            # async http request
            http = tornado.httpclient.AsyncHTTPClient()
            logging.info("http://localhost:{}/?action=new&session_id={}".format(i_port, session_id))
            response = await http.fetch("http://localhost:{}/?action=new&session_id={}".format(i_port, session_id),
                                        method='POST', body=self.request.body
                                        )
            self.write(response.body)

        elif action == 'reply':
            body_data = self.get_body_data_or_return_error()
            session_id = body_data['sessionId']
            i_worker, i_port = MainHandler.locate_worker(session_id)
            logging.info("redirect the request to worker:{} | port:{}, with session id:{}".
                         format(i_worker, i_port, session_id))
            # async http request
            http = tornado.httpclient.AsyncHTTPClient()
            response = await http.fetch("http://localhost:{}/?action=reply".format(i_port),
                                        method='POST', body=self.request.body
                                        )
            self.write(response.body)

def run_children():
    """
    :return:
    """
    children = []
    for i in range(conf.WORKER_NUM):
        port = options.worker_port_begin + i
        worker_name = "woker_{}".format(port)
        worker_prog_loc = os.path.join(kp_setup.root_dir, 'src', 'WorkerServer.py')
        cmd = "{} {} --port={} --worker_name={}".format(sys.executable, worker_prog_loc, port, worker_name)
        args = shlex.split(cmd)
        logging.info("exec: {}".format(cmd))
        #p = subprocess.Popen(cmd, shell=True)
        p = subprocess.Popen(args)
        children.append(p)
    return children

def main():
    parse_command_line()
    children = run_children()

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        # template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # static_path=os.path.join(os.path.dirname(__file__), "static"),
        # xsrf_cookies=True, todo 前端加入这块支持
        debug=options.debug,
    )
    app.listen(options.port)
    logging.info("master server: Listening port: {}, worker num: {}".format(options.port, options.worker_num))
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()



